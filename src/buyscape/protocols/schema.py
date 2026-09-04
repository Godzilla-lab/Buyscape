"""Evidence protocols are data, not code.

A protocol says which shots to ask for, what each one proves, which claims map
onto which shots, and what the agent must physically check before paying. Adding
a category is a YAML file, never a code change.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Shot(BaseModel):
    id: str
    ask: str = Field(description="Plain language instruction shown to the seller.")
    kind: str = Field("photo", description="photo | screenshot | clip | text")
    required: bool = True
    opens_item: bool = Field(
        False,
        description="True for shots that require removing a panel, cover or lid.",
    )
    checks: list[str] = Field(default_factory=list)
    extract: list[str] = Field(default_factory=list)


class Question(BaseModel):
    """Something only the seller knows, asked so the answer can be checked.

    A photograph cannot say how old a thing is, whether it was dropped, or
    whether it still holds charge. The seller knows. Their answer is not taken
    on trust: it becomes a claim priced at the worst case until proven, and
    where the catalogue knows the truth the answer is checked against it.

    Only ask what changes the price. Every question is one more reason for a
    seller to abandon the form, so a question that cannot move the number or
    cannot be checked does not belong in a protocol.
    """

    id: str
    ask: str = Field(description="Plain language, one sentence, asked of the seller.")
    kind: str = Field("choice", description="choice | number | yesno | text")
    options: list[str] = Field(default_factory=list, description="For kind=choice.")
    unit: str = ""
    claim: str | None = Field(
        None, description="The claim spec this answer fills, so it is priced like any claim."
    )
    checks_attr: str | None = Field(
        None,
        description=(
            "A catalogue attribute this answer must agree with, for example "
            "'year'. A seller who calls a 2011 laptop twenty years old is "
            "either wrong about the item or wrong about the age."
        ),
    )
    tolerance: float = Field(0.35, description="Fractional disagreement allowed against the attribute.")


class ClaimSpec(BaseModel):
    id: str
    kinds: list[str] = Field(default_factory=list)
    evidence_slots: list[str] = Field(default_factory=list)
    worst_case: str | None = None
    pickup_check: str | None = None
    penalty: float = Field(
        0.9,
        description="Multiplier applied to the range while the claim is unproven.",
        gt=0.0,
        le=1.0,
    )


class Protocol(BaseModel):
    category: str
    version: int = 1
    display_name: str = ""
    aliases: list[str] = Field(
        default_factory=list,
        description=(
            "Other names for this kind of item. A model calls the same thing a "
            "generator, a portable generator or a gasoline generator, and all "
            "three must reach this protocol."
        ),
    )
    always_novel: bool = False
    shots: list[Shot] = Field(default_factory=list)
    questions: list[Question] = Field(default_factory=list)
    claims: list[ClaimSpec] = Field(default_factory=list)
    pickup_protocol: list[str] = Field(default_factory=list)

    def claim_for(
        self, attribute: str | None, kind: str, text: str = ""
    ) -> ClaimSpec | None:
        """Find the spec for an extracted claim.

        Exact attribute match first, then a word-level match against the spec id
        using the claim's attribute and text. Falling back on `kind` alone is
        deliberately last and only when exactly one spec claims that kind:
        matching "256gb" to the battery spec because both are of kind "spec"
        would price a storage claim as a battery claim.
        """
        if attribute:
            for spec in self.claims:
                if spec.id == attribute:
                    return spec

        haystack = f"{attribute or ''} {text}".lower()
        best: ClaimSpec | None = None
        best_hits = 0
        for spec in self.claims:
            words = [w for w in spec.id.split("_") if len(w) >= 2]
            hits = sum(1 for w in words if w in haystack)
            if hits > best_hits:
                best, best_hits = spec, hits
        if best is not None and best_hits > 0:
            return best

        of_kind = [spec for spec in self.claims if kind in spec.kinds]
        return of_kind[0] if len(of_kind) == 1 else None

    @property
    def required_shots(self) -> list[Shot]:
        return [s for s in self.shots if s.required]

    @property
    def opening_shots(self) -> list[Shot]:
        return [s for s in self.shots if s.opens_item]


def _words(text: str) -> set[str]:
    return {w for w in re.split(r"[^a-z0-9]+", (text or "").lower()) if w}


def resolve(protocols: dict[str, Protocol], spoken: str | None) -> Protocol:
    """Find the protocol for whatever the model called this item.

    Exact name first, then an alias, then the most specific name whose every
    word appears in what was said: 'portable generator' reaches the generator
    protocol, 'twin tub washing machine' reaches the washing machine one.
    Anything genuinely new falls to the generic protocol, which is the point:
    an unknown item is still weighed, opened and bought, never refused.
    """
    said = _words(spoken)
    if not said:
        return protocols["generic"]

    best: Protocol | None = None
    best_words = 0
    for protocol in protocols.values():
        if protocol.category == "generic":
            continue
        for name in [protocol.category, protocol.display_name, *protocol.aliases]:
            words = _words(name)
            if words and words.issubset(said) and len(words) > best_words:
                best, best_words = protocol, len(words)
    return best or protocols["generic"]


def load_protocols(root: Path) -> dict[str, Protocol]:
    out: dict[str, Protocol] = {}
    for path in sorted(root.glob("*.yaml")):
        protocol = Protocol.model_validate(yaml.safe_load(path.read_text()))
        out[protocol.category] = protocol
    return out
