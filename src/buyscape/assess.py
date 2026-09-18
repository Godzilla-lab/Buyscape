"""Two views of the same uncertainty: one for staff, one for the seller.

The back office needs a number and the reasons behind it, so a reviewer can
tell a confident answer from a coin toss before money moves. The seller needs
none of that. They need the next thing to point their camera at, the way a
face scanner says move closer rather than reporting a match score. Both come
from the same evidence, so they can never disagree with each other.

The score here is a stated strength, not a calibrated probability. It becomes
one when settled pickup prices exist to calibrate against, which is rule 5.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .claims.ledger import Claim, ClaimStatus
from .identify.chain import ChainResult, identification_strength
from .pricing.engine import Quote
from .protocols.schema import Protocol, Shot

# Fields that name the item. A shot that extracts one of these is a shot that
# can end an identification argument, so it is what we ask for first.
IDENTIFYING = {
    "brand", "model", "model_name", "serial", "imei", "rating",
    "kva", "hp", "capacity_kg", "storage_gb", "cpu", "ram_gb",
}

BANDS = ((0.85, "certain"), (0.65, "likely"), (0.40, "unsure"), (0.0, "unknown"))


@dataclass
class Assessment:
    """What the back office sees."""

    confidence: float = 0.0
    band: str = "unknown"
    answer: str | None = None
    alternatives: list[tuple[str, float]] = field(default_factory=list)
    drivers: list[str] = field(default_factory=list)
    price_confidence: float = 0.0

    @property
    def percent(self) -> int:
        return int(round(self.confidence * 100))

    def sentence(self) -> str:
        if self.answer and self.band in ("certain", "likely"):
            return f"{self.percent}% sure this is a {self.answer}."
        if self.alternatives:
            names = " or a ".join(name for name, _ in self.alternatives[:2])
            return (
                f"Not sure enough to price: {self.percent}% on the best answer. "
                f"It is probably a {names}, and the photos cannot separate them."
            )
        return f"{self.percent}%: the photos do not say what this is."


@dataclass
class CaptureRequest:
    """One instruction shown to the seller. No scores, no model names."""

    slot: str
    ask: str
    because: str
    kind: str = "photo"  # photo | video | text, so the app opens the right camera


def video_script(protocol: Protocol) -> str:
    """One guided video instead of five photographs nobody will send.

    A still is one chance at a legible plate. Thirty seconds of video is
    hundreds, from angles the seller would never think to take, and it is far
    harder to substitute someone else's item for. So when two readers cannot
    agree on what the plate says, asking again for the same still is asking
    the same question twice. The script is composed from this protocol's own
    shots, so a new category gets a sensible video by writing YAML.
    """
    steps = [
        "Record one video, up to thirty seconds, in one take.",
        "Start by showing the whole item slowly from every side.",
    ]

    naming = [s for s in protocol.shots if set(s.extract) & IDENTIFYING]
    # A video cannot contain a screenshot, so a shot that lives on the item's
    # own screen becomes an instruction to film that screen while using it.
    printed = next((s for s in naming if s.kind == "photo"), None)
    if printed:
        steps.append(f"Then hold the camera still and close for three seconds: {printed.ask}")
    # An item with a screen carries its identity there rather than on a plate,
    # and a screen can be filmed while it is used, which a still cannot show.
    on_screen = next((s for s in naming if s.kind == "screenshot"), None)
    if on_screen:
        steps.append(
            "Then, still filming, do this on the item's own screen and hold it "
            f"steady so the writing can be read: {_as_filmed(on_screen.ask)}"
        )

    for shot in protocol.shots:
        if shot.opens_item:
            steps.append(f"Then, without stopping the video: {shot.ask}")
            break
    for shot in protocol.shots:
        # Skip a clip that is itself a walkaround: that is step one already.
        if shot.kind == "clip" and not shot.opens_item and "walk" not in shot.ask.lower():
            steps.append(f"Finish with: {shot.ask}")
            break
    steps.append("Keep filming the whole time. Do not cut between clips.")
    return " ".join(steps)


def _band(score: float) -> str:
    for floor, name in BANDS:
        if score >= floor:
            return name
    return "unknown"


def assess(result: ChainResult, quote: Quote, ledger: list[Claim]) -> Assessment:
    """Score the identification and the price from the evidence behind them."""
    out = Assessment()
    ident = result.identification
    ranked = sorted(ident.candidates, key=lambda c: c.score, reverse=True) if ident else []
    out.alternatives = [(f"{c.brand} {c.model}".strip(), round(c.score, 2)) for c in ranked[:3]]

    score, why = identification_strength(result)
    out.drivers.extend(why)
    if not result.abstained and result.model_key:
        out.answer = result.model_key
    else:
        # An abstention is not zero knowledge. The strength of the best guess
        # is what tells a reviewer whether one more photo would settle it.
        score *= 0.6
        out.drivers.insert(0, result.reason or "the chain abstained")
        out.alternatives = out.alternatives[:2]

    out.confidence = round(max(0.0, min(score, 1.0)), 2)
    out.band = _band(out.confidence)

    unproven = sum(1 for c in ledger if c.is_priced_at_worst_case)
    proven = sum(1 for c in ledger if c.status is ClaimStatus.SUPPORTED)
    price = 0.0 if quote.is_failure else min(quote.observation_count / 8.0, 1.0)
    if quote.method == "material_floor":
        price = min(price + 0.35, 0.6)  # a weight and a material, but no identity
    if unproven:
        price *= max(0.4, 1.0 - 0.06 * unproven)
    out.price_confidence = round(max(0.0, min(price, 1.0)), 2)
    if unproven:
        out.drivers.append(f"{unproven} claims are still unproven, {proven} are supported")
    return out


def _as_filmed(ask: str) -> str:
    """Turn a screenshot instruction into something you can film."""
    for prefix in ("Screenshot of ", "A screenshot of ", "Take a screenshot of "):
        if ask.startswith(prefix):
            rest = ask[len(prefix):]
            return "open " + rest[0].lower() + rest[1:]
    return ask


def _readers_disagreed(result: ChainResult) -> bool:
    return any("unread" in note for note in result.corroboration_notes)


def _unmet(protocol: Protocol, slots_present: set[str], only_identifying: bool) -> list[Shot]:
    shots = [s for s in protocol.shots if s.id not in slots_present]
    if only_identifying:
        shots = [s for s in shots if set(s.extract) & IDENTIFYING]
    return shots


def capture_requests(
    result: ChainResult,
    protocol: Protocol,
    slots_present: set[str],
    limit: int = 3,
) -> list[CaptureRequest]:
    """What to ask the seller for next, most useful first.

    A generic checklist teaches sellers to ignore it. So the list is driven by
    what actually went wrong: a picture of two phones asks for one phone, an
    unreadable plate asks for the plate, and an item nobody can name asks for
    the one shot whose whole job is to carry the name.
    """
    asks: list[CaptureRequest] = []
    reading = result.reading

    if reading is not None:
        if reading.multiple_items:
            asks.append(
                CaptureRequest(
                    "single_item",
                    "Photograph one item on its own, with nothing else in the picture.",
                    "the photos show more than one item",
                )
            )
        if reading.screenshot_of_gallery and not reading.serial_text:
            asks.append(
                CaptureRequest(
                    "own_photo",
                    "Take a new photo of the item itself, not a picture of another screen.",
                    "this is a screenshot rather than a photo of the item",
                )
            )
        elif reading.stock_photo_suspected:
            asks.append(
                CaptureRequest(
                    "own_photo",
                    "Take your own photo of the actual item you are selling.",
                    "this looks like a catalogue picture, not the real unit",
                )
            )

    # Anything the reader could not point at, or an answer nobody can trust,
    # is an argument about identity, and identity lives on the label.
    identity_unclear = result.abstained or not result.used_label or bool(result.fraud_flags)

    # When two readers looked at the same photographs and could not agree on
    # what is written on the item, a sharper still of the same angle is not
    # the answer. Escalate to a video, which gives hundreds of frames and
    # cannot be a picture of somebody else's machine.
    if identity_unclear and _readers_disagreed(result):
        asks.append(
            CaptureRequest(
                "guided_video",
                video_script(protocol),
                "two readings of these photos disagreed about what is written on the item",
                kind="video",
            )
        )
    for shot in _unmet(protocol, slots_present, only_identifying=identity_unclear):
        because = (
            "nothing on the item says which model this is"
            if identity_unclear
            else "this is needed before the price can be confirmed"
        )
        asks.append(CaptureRequest(shot.id, shot.ask, because, kind=shot.kind))

    if identity_unclear and not any(a.slot in {s.id for s in protocol.shots} for a in asks):
        asks.append(
            CaptureRequest(
                "closer",
                "Move closer and photograph any label, sticker or plate so the writing is sharp.",
                "no label was legible in the photos sent so far",
            )
        )
    return asks[:limit]
