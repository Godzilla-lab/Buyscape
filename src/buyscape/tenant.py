"""A tenant is a file, not a code path.

Everything specific to a business lives here: what they call their categories,
which protocol collects evidence for each, and what a lot of it is made of
when nobody can say what the item is. Onboarding a second business is another
YAML file. If it ever needs a code change, that is a bug in the engine.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

from .protocols.schema import ClaimSpec, Protocol, Question, resolve

QUESTION_KINDS = ("yesno", "number", "choice", "text")
ANY_CATEGORY = "*"


class TenantCategory(BaseModel):
    name: str
    protocol: str
    material: str = "unknown"


class Refusal(BaseModel):
    match: str
    because: str
    url: str | None = None


class TenantQuestion(BaseModel):
    """A question the business wrote for its sellers, in the back office.

    It is fixed, not generated: the same question to every seller of that
    category, so the answers can be compared, checked and, later, calibrated
    against settled prices. The answer becomes a claim priced at the worst
    case until the agent proves it at pickup, so it can lower the price and
    never raise it. A question with no worst case and no pickup check cannot
    move the price, and is refused here rather than shown to a seller.
    """

    category: str = Field(ANY_CATEGORY, description="A tenant category name, or * for all.")
    id: str = ""
    ask: str
    kind: str = "yesno"
    options: list[str] = Field(default_factory=list)
    unit: str = ""
    worst_case: str
    pickup_check: str
    penalty: float = Field(0.9, gt=0.0, le=1.0)
    checks_attr: str | None = None
    tolerance: float = 0.35

    @field_validator("ask", "worst_case", "pickup_check")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a question needs the words to ask, what is assumed if unproven, and how the agent checks it at pickup")
        return value.strip()

    @model_validator(mode="after")
    def _shape(self) -> "TenantQuestion":
        if self.kind not in QUESTION_KINDS:
            raise ValueError(f"kind must be one of {', '.join(QUESTION_KINDS)}, not {self.kind!r}")
        self.options = [o.strip() for o in self.options if o and o.strip()]
        if self.kind == "choice" and len(self.options) < 2:
            raise ValueError("a choice question needs at least two options")
        if not self.id:
            words = re.findall(r"[a-z0-9]+", self.ask.lower())
            self.id = "_".join(words[:6]) or "question"
        self.id = re.sub(r"[^a-z0-9_]", "", self.id.lower().replace("-", "_").replace(" ", "_"))
        return self

    def as_question(self) -> Question:
        return Question(
            id=self.id, ask=self.ask, kind=self.kind, options=list(self.options), unit=self.unit,
            claim=self.id, checks_attr=self.checks_attr, tolerance=self.tolerance,
        )

    def as_claim(self) -> ClaimSpec:
        return ClaimSpec(
            id=self.id, kinds=["condition" if self.kind == "yesno" else "spec"],
            worst_case=self.worst_case, pickup_check=self.pickup_check, penalty=self.penalty,
        )


def _band(table: dict[str, list[float]], category: str | None) -> tuple[float, float] | None:
    band = table.get((category or "").strip().lower()) or table.get("default")
    if not band or len(band) != 2:
        return None
    low, high = float(band[0]), float(band[1])
    return (min(low, high), max(low, high))


class Tenant(BaseModel):
    tenant: str
    display_name: str = ""
    currency: str = "NGN"
    scrap_index: str = ""
    categories: list[TenantCategory] = Field(default_factory=list)
    minimums: dict = Field(default_factory=dict)
    refuses: list[Refusal] = Field(default_factory=list)
    grades: dict = Field(default_factory=dict)
    # What a unit that does not work fetches against a working one, as a
    # share of the working price, per category. Set by the business, applied
    # only when the seller says it does not work or the photos show it.
    dead_fraction: dict[str, list[float]] = Field(default_factory=dict)
    # What a used one is worth as a share of the new asking price, per
    # category. Used only when the used market is too thin to price from and
    # dealers' new stock of the same thing is listed.
    resale_fraction: dict[str, list[float]] = Field(default_factory=dict)
    # Written by staff in the back office, kept in <tenant>.questions.yaml.
    questions: list[TenantQuestion] = Field(default_factory=list)

    def minimum_for(self, category: str | None) -> float | None:
        """A price this business has published in its own words.

        They wrote that they buy scrap laptops starting from five thousand
        naira. Quoting four thousand for a laptop contradicts the tenant's own
        advertising, so the floor is theirs and the engine honours it.
        """
        per_item = (self.minimums or {}).get("per_item") or {}
        value = per_item.get((category or "").strip().lower())
        return float(value) if value is not None else None

    def refusal(self, *texts: str | None) -> Refusal | None:
        """Whether this business declines the item outright.

        A refusal is an outcome, not a low price. Quoting a small number for
        something nobody will collect wastes an agent's day and the seller's.
        """
        haystack = " ".join(t.lower() for t in texts if t)
        for rule in self.refuses:
            if rule.match.lower() in haystack:
                return rule
        return None

    def category(self, spoken: str | None) -> TenantCategory | None:
        """Match what a model or a seller called it to a tenant category."""
        said = {w for w in (spoken or "").lower().replace("-", " ").split() if w}
        if not said:
            return None
        best: TenantCategory | None = None
        best_words = 0
        for entry in self.categories:
            words = {w for w in entry.name.lower().replace("-", " ").split() if w and w != "and"}
            if words and words.issubset(said) and len(words) > best_words:
                best, best_words = entry, len(words)
        return best

    def protocol_for(
        self, protocols: dict[str, Protocol], spoken: str | None
    ) -> Protocol:
        """The tenant's own mapping first, then the protocols' own aliases.

        A business that calls something Premium means something by it that no
        protocol can guess, so their file wins. Anything they have not named
        still resolves, because people sell things nobody listed.
        """
        entry = self.category(spoken)
        if entry and entry.protocol in protocols:
            return protocols[entry.protocol]
        return resolve(protocols, spoken)

    def dead_fraction_for(self, category: str | None) -> tuple[float, float] | None:
        return _band(self.dead_fraction, category)

    def resale_fraction_for(self, category: str | None) -> tuple[float, float] | None:
        return _band(self.resale_fraction, category)

    def questions_for(self, tenant_category: str | None) -> list[TenantQuestion]:
        want = (tenant_category or "").strip().lower()
        return [
            q for q in self.questions
            if q.category == ANY_CATEGORY or (want and q.category.strip().lower() == want)
        ]

    def with_questions(self, protocol: Protocol, tenant_category: str | None) -> Protocol:
        """The protocol plus what this business asks its sellers.

        A staff question with the same id as a protocol question replaces it,
        so a business can reword what the engine asks without a code change.
        """
        mine = self.questions_for(tenant_category)
        if not mine:
            return protocol
        ids = {q.id for q in mine}
        return protocol.model_copy(
            update={
                "questions": [q for q in protocol.questions if q.id not in ids] + [q.as_question() for q in mine],
                "claims": [c for c in protocol.claims if c.id not in ids] + [q.as_claim() for q in mine],
            }
        )

    def material_for(self, spoken: str | None) -> str | None:
        entry = self.category(spoken)
        return entry.material if entry else None


def questions_path(tenant_file: Path) -> Path:
    return tenant_file.with_name(tenant_file.stem + ".questions.yaml")


def load_questions(path: Path) -> list[TenantQuestion]:
    if not path.exists():
        return []
    return [TenantQuestion.model_validate(row) for row in (yaml.safe_load(path.read_text()) or [])]


def save_questions(path: Path, questions: list[TenantQuestion]) -> None:
    rows = [q.model_dump(exclude_defaults=False) for q in questions]
    path.write_text(
        "# Questions this business asks its sellers, written in the back office.\n"
        "# Each answer is priced at the worst case until the agent checks it.\n"
        + yaml.safe_dump(rows, sort_keys=False, allow_unicode=True)
    )


def load_tenant(path: Path) -> Tenant:
    tenant = Tenant.model_validate(yaml.safe_load(path.read_text()))
    tenant.questions = load_questions(questions_path(path))
    return tenant
