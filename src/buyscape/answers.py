"""What the seller says when asked, and whether it holds up.

A photograph cannot say how old a thing is, whether it was dropped, or
whether it still holds charge, and those are exactly the facts that move a
price. Only the seller knows them. So the engine asks, and then does two
things with the answer that a form never does: it prices the answer at its
worst case until an agent proves it, and where the catalogue knows the truth
it checks the answer against it.

A seller calling a 2011 laptop twenty years old is not necessarily lying.
They may be wrong about the age, or the item may not be the model we think it
is. Either way it is a disagreement between two records, and this project
treats those the same way everywhere: say so, price the worst case, and let
the agent settle it in person.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .identify.catalogue import Entry
from .protocols.schema import Protocol, Question
from .providers.tasks import ClaimDraft

YES = {"yes", "y", "true", "yeah", "yep", "correct", "it does", "works"}
NO = {"no", "n", "false", "nope", "not working", "does not", "doesn't"}


@dataclass
class AnswerReview:
    drafts: list[ClaimDraft] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    # The seller said it does not work. That changes the basis of the price,
    # not just a multiplier on it.
    not_working: bool = False


# Answers to "what does not work" that mean nothing is wrong.
NOTHING_WRONG = {"none", "nothing", "no", "nil", "n/a", "na", "all good", "everything works", "works"}


def unanswered(protocol: Protocol, answers: dict[str, str]) -> list[Question]:
    """Questions still worth asking. Answered ones are never asked twice."""
    return [q for q in protocol.questions if not (answers.get(q.id) or "").strip()]


def _number(text: str) -> float | None:
    digits = ""
    for ch in str(text):
        if ch.isdigit() or (ch == "." and digits and "." not in digits):
            digits += ch
        elif digits:
            break
    try:
        return float(digits) if digits else None
    except ValueError:
        return None


def review_answers(
    protocol: Protocol,
    answers: dict[str, str],
    entry: Entry | None = None,
    today: date | None = None,
) -> AnswerReview:
    """Turn answers into claims, and check the checkable ones."""
    out = AnswerReview()
    year_now = (today or date.today()).year

    for question in protocol.questions:
        raw = (answers.get(question.id) or "").strip()
        if not raw:
            continue

        # A no to a working question is the seller telling us the worst case
        # themselves, which is worth more than any photograph.
        lowered = raw.lower()
        said_no = question.kind == "yesno" and lowered in NO
        out.drafts.append(
            ClaimDraft(
                text=f"{question.ask} {raw}",
                kind="condition" if question.kind == "yesno" else "spec",
                attribute=question.claim,
                value=raw,
                checkable_remotely=False,
            )
        )
        if said_no:
            out.notes.append(f"the seller says no to: {question.ask}")
        if question.claim == "works" or question.id.startswith("works"):
            if said_no or (question.kind == "text" and lowered.strip(" .!") not in NOTHING_WRONG):
                out.not_working = True

        if not (question.checks_attr and entry):
            continue
        known = entry.attrs.get(question.checks_attr)
        stated = _number(raw)
        if known is None or stated is None:
            continue
        if question.checks_attr == "year":
            actual = max(year_now - int(float(known)), 0)
            if actual and abs(stated - actual) > question.tolerance * max(actual, 1):
                out.contradictions.append(question.claim or question.id)
                out.notes.append(
                    f"the seller says it is {stated:g} years old, but a {entry.key} "
                    f"shipped in {known}, which makes it about {actual} years old"
                )
            else:
                out.notes.append(f"the stated age agrees with a {entry.key} from {known}")
        else:
            expected = float(known)
            if expected and abs(stated - expected) > question.tolerance * expected:
                out.contradictions.append(question.claim or question.id)
                out.notes.append(
                    f"the seller says {question.checks_attr} is {stated:g}, but a "
                    f"{entry.key} is {known}"
                )
    return out
