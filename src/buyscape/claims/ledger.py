"""The claims ledger: the reason lying cannot raise the remote price.

Every seller statement becomes a row tied to the evidence that would prove it.
Proven claims are priced. Unproven ones are priced at the worst case and listed
on the quote as conditions, so the pickup price can only hold or improve. This
is the direct answer to the trade-in failure mode where an online quote is cut
by a third at the doorstep.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ..providers.tasks import ClaimDraft
from ..protocols.schema import Protocol


class ClaimStatus(StrEnum):
    SUPPORTED = "supported"
    UNVERIFIED = "unverified"
    CONTRADICTED = "contradicted"
    UNVERIFIABLE_REMOTE = "unverifiable_remote"
    REFUSED_TO_OPEN = "refused_to_open"


@dataclass
class Claim:
    text: str
    kind: str
    attribute: str | None
    value: str | None
    status: ClaimStatus
    required_evidence: list[str] = field(default_factory=list)
    evidence_seen: list[str] = field(default_factory=list)
    worst_case: str | None = None
    pickup_check: str | None = None
    penalty: float = 1.0  # multiplier applied to the range while unproven

    @property
    def is_priced_at_worst_case(self) -> bool:
        return self.status in (
            ClaimStatus.UNVERIFIED,
            ClaimStatus.UNVERIFIABLE_REMOTE,
            ClaimStatus.CONTRADICTED,
            ClaimStatus.REFUSED_TO_OPEN,
        )


def build_ledger(
    drafts: list[ClaimDraft],
    protocol: Protocol,
    slots_present: set[str],
    contradictions: list[str] | None = None,
) -> list[Claim]:
    """Map extracted claims onto protocol evidence and set each status."""
    contradicted = {c.lower() for c in (contradictions or [])}
    ledger: list[Claim] = []

    for draft in drafts:
        spec = protocol.claim_for(draft.attribute, draft.kind)
        required = list(spec.evidence_slots) if spec else []
        seen = [s for s in required if s in slots_present]

        if draft.text.lower() in contradicted:
            status = ClaimStatus.CONTRADICTED
        elif not draft.checkable_remotely or not required:
            status = ClaimStatus.UNVERIFIABLE_REMOTE
        elif required and set(required).issubset(slots_present):
            status = ClaimStatus.SUPPORTED
        else:
            status = ClaimStatus.UNVERIFIED

        ledger.append(
            Claim(
                text=draft.text,
                kind=draft.kind,
                attribute=draft.attribute,
                value=draft.value,
                status=status,
                required_evidence=required,
                evidence_seen=seen,
                worst_case=spec.worst_case if spec else None,
                pickup_check=spec.pickup_check if spec else None,
                penalty=(spec.penalty if spec else 0.9) if status != ClaimStatus.SUPPORTED else 1.0,
            )
        )
    return ledger


def worst_case_multiplier(ledger: list[Claim], floor: float = 0.30) -> float:
    """Combined penalty for everything still unproven, floored so it stays sane."""
    multiplier = 1.0
    for claim in ledger:
        if claim.is_priced_at_worst_case:
            multiplier *= claim.penalty
    return max(round(multiplier, 4), floor)


def conditions(ledger: list[Claim]) -> list[str]:
    """The lines that go on the quote so the seller knows what must hold."""
    out: list[str] = []
    for claim in ledger:
        if not claim.is_priced_at_worst_case:
            continue
        check = claim.pickup_check or "Agent will confirm at pickup"
        out.append(f"{claim.text.strip()} -> not proven remotely. {check}.")
    return out
