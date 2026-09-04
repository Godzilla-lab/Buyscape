"""A tenant is a file, not a code path.

Everything specific to a business lives here: what they call their categories,
which protocol collects evidence for each, and what a lot of it is made of
when nobody can say what the item is. Onboarding a second business is another
YAML file. If it ever needs a code change, that is a bug in the engine.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from .protocols.schema import Protocol, resolve


class TenantCategory(BaseModel):
    name: str
    protocol: str
    material: str = "unknown"


class Refusal(BaseModel):
    match: str
    because: str
    url: str | None = None


class Tenant(BaseModel):
    tenant: str
    display_name: str = ""
    currency: str = "NGN"
    scrap_index: str = ""
    categories: list[TenantCategory] = Field(default_factory=list)
    minimums: dict = Field(default_factory=dict)
    refuses: list[Refusal] = Field(default_factory=list)
    grades: dict = Field(default_factory=dict)

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

    def material_for(self, spoken: str | None) -> str | None:
        entry = self.category(spoken)
        return entry.material if entry else None


def load_tenant(path: Path) -> Tenant:
    return Tenant.model_validate(yaml.safe_load(path.read_text()))
