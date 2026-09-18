"""One seller, one item, one folder.

A session is what the capture page produces and the back office reads. It is
a directory under `sessions/` holding the photos the seller took, one JSON
file with everything they said, and the engine's result once it has run. No
database: the folder is the record, and it is the same shape `buyscape assess`
reads, so anything in here can be replayed from the command line.

Two audiences read the same result. The seller sees an offer, the conditions
on it and what to send next, in plain words. The back office sees the model
names, the confidence, the claims ledger and the fraud flags. `seller_view`
and `office_view` are the only two ways out of here, and a test holds the line
between them.
"""

from __future__ import annotations

import base64
import json
import re
import secrets
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from PIL import Image

from ..protocols.schema import Protocol
from ..runner import Case, CaseResult
from ..tenant import Tenant

# No 0, O, 1 or I: the code is handwritten and then read off a photo.
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
SAFE = re.compile(r"[^A-Za-z0-9._-]+")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
HEIC_SUFFIXES = {".heic", ".heif"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".webm", ".3gp"}
# Two photos closer than this in perceptual hash are the same picture.
DUPLICATE_DISTANCE = 6

Valuer = Callable[[Case, str], tuple[CaseResult, str]]
"""(case, tenant name) -> (result, report markdown). The server supplies it."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _phash(path: Path) -> str | None:
    try:
        import imagehash

        with Image.open(path) as im:
            return str(imagehash.phash(im))
    except Exception:
        return None


def _hamming(a: str, b: str) -> int:
    return bin(int(a, 16) ^ int(b, 16)).count("1")


@dataclass
class Shape:
    """What the page needs to know about a protocol, with the code filled in."""

    protocol: Protocol
    code: str

    def shots(self) -> list[dict]:
        return [
            {
                "slot": s.id,
                "ask": s.ask.replace("{code}", self.code),
                "kind": s.kind,
                "required": s.required,
                "opens_item": s.opens_item,
            }
            for s in self.protocol.shots
        ]

    def questions(self) -> list[dict]:
        return [
            {"id": q.id, "ask": q.ask, "kind": q.kind, "options": list(q.options), "unit": q.unit}
            for q in self.protocol.questions
        ]


class Store:
    def __init__(
        self,
        root: Path,
        tenant: Tenant,
        protocols: dict[str, Protocol],
        catalogue_categories: set[str],
        valuer: Valuer,
    ) -> None:
        self.root = root
        self.dir = root / "sessions"
        self.tenant = tenant
        self.protocols = protocols
        self.catalogue_categories = catalogue_categories
        self.valuer = valuer
        self.lock = threading.Lock()

    # ----- tenant facing -----

    def tenant_view(self) -> dict:
        return {
            "tenant": self.tenant.tenant,
            "display_name": self.tenant.display_name or self.tenant.tenant,
            "currency": self.tenant.currency,
            "categories": [c.name for c in self.tenant.categories],
        }

    def protocol_for(self, category: str | None) -> Protocol:
        if not category:
            return self.protocols["generic"]
        return self.tenant.protocol_for(self.protocols, category)

    # ----- lifecycle -----

    def create(self, body: dict) -> dict:
        category = (body.get("category") or "").strip() or None
        if category and category not in {c.name for c in self.tenant.categories}:
            raise ValueError(f"{category!r} is not one of this business's categories")
        sid = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
        code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(4))
        folder = self.dir / sid
        folder.mkdir(parents=True, exist_ok=False)
        session = {
            "id": sid,
            "tenant": self.tenant.tenant,
            "created_at": _now(),
            "updated_at": _now(),
            "code": code,
            "category": category,
            "protocol": self.protocol_for(category).category,
            "text": (body.get("text") or "").strip(),
            "asking": float(body.get("asking") or 0) or None,
            "contact": (body.get("contact") or "").strip(),
            "answers": {},
            "refused": [],
            "photos": [],
            "status": "open",
            "result": None,
            "duplicates": [],
            "settlement": None,
        }
        self._save(session)
        return self.seller_view(session)

    def load(self, sid: str) -> dict:
        path = self.dir / SAFE.sub("", sid) / "session.json"
        if sid != SAFE.sub("", sid) or not path.exists():
            raise KeyError(sid)
        return json.loads(path.read_text())

    def _save(self, session: dict) -> None:
        session["updated_at"] = _now()
        path = self.dir / session["id"] / "session.json"
        path.write_text(json.dumps(session, indent=1, default=str))

    def list(self) -> list[dict]:
        rows: list[dict] = []
        if not self.dir.exists():
            return rows
        for path in sorted(self.dir.glob("*/session.json"), reverse=True):
            s = json.loads(path.read_text())
            r = s.get("result") or {}
            q = r.get("quote") or {}
            rows.append(
                {
                    "id": s["id"],
                    "created_at": s["created_at"],
                    "updated_at": s["updated_at"],
                    "status": s["status"],
                    "category": s.get("category"),
                    "protocol": s.get("protocol"),
                    "contact": s.get("contact"),
                    "asking": s.get("asking"),
                    "photos": len(s.get("photos") or []),
                    "low": q.get("low"),
                    "high": q.get("high"),
                    "failure_code": q.get("failure_code") or r.get("failure_code"),
                    "model_key": r.get("model_key"),
                    "duplicates": len(s.get("duplicates") or []),
                    "settled": (s.get("settlement") or {}).get("price"),
                }
            )
        return rows

    def add_photo(self, sid: str, body: dict) -> dict:
        session = self.load(sid)
        slot = SAFE.sub("", body.get("slot") or "extra") or "extra"
        data = body.get("data") or ""
        if "," in data:
            data = data.split(",", 1)[1]
        raw = base64.b64decode(data)
        if not raw:
            raise ValueError("empty file")
        suffix = Path(body.get("name") or "photo.jpg").suffix.lower() or ".jpg"
        if suffix not in IMAGE_SUFFIXES | HEIC_SUFFIXES | VIDEO_SUFFIXES:
            raise ValueError(f"{suffix} is not a photo or a clip we can read")
        folder = self.dir / session["id"]
        n = sum(1 for p in session["photos"] if p["slot"] == slot) + 1
        path = folder / f"{slot}__{n:02d}{suffix}"
        path.write_bytes(raw)
        if suffix in HEIC_SUFFIXES:
            # iPhones shoot HEIC and the models do not read it.
            import pillow_heif

            pillow_heif.register_heif_opener()
            jpeg = path.with_suffix(".jpg")
            with Image.open(path) as im:
                im.convert("RGB").save(jpeg, format="JPEG", quality=92)
            path.unlink()
            path = jpeg
        kind = "clip" if suffix in VIDEO_SUFFIXES else "photo"
        record = {
            "slot": slot,
            "file": path.name,
            "kind": kind,
            "phash": _phash(path) if kind == "photo" else None,
            "at": _now(),
        }
        session["photos"].append(record)
        if kind == "clip":
            # The readers look at stills, so the clip becomes its sharpest
            # frames, one per stretch of the walk. They belong to the clip:
            # the seller never sees them and they go when it goes.
            for frame in sample_frames(path, folder, path.stem):
                session["photos"].append(
                    {
                        "slot": slot,
                        "file": frame.name,
                        "kind": "frame",
                        "from": path.name,
                        "phash": _phash(frame),
                        "at": record["at"],
                    }
                )
        self._save(session)
        return self.seller_view(session)

    def remove_photo(self, sid: str, file: str) -> dict:
        session = self.load(sid)
        gone = [p for p in session["photos"] if p["file"] == file or p.get("from") == file]
        if gone:
            for p in gone:
                target = self.dir / session["id"] / SAFE.sub("", p["file"])
                if target.exists():
                    target.unlink()
            session["photos"] = [p for p in session["photos"] if p not in gone]
            self._save(session)
        return self.seller_view(session)

    def submit(self, sid: str, body: dict) -> dict:
        """Run the engine on everything the seller has sent so far."""
        session = self.load(sid)
        if body.get("text") is not None:
            session["text"] = str(body["text"]).strip()
        if body.get("asking") is not None:
            session["asking"] = float(body["asking"] or 0) or None
        if body.get("contact") is not None:
            session["contact"] = str(body["contact"]).strip()
        if body.get("answers") is not None:
            session["answers"] = {
                str(k): str(v) for k, v in dict(body["answers"]).items() if str(v).strip()
            }
        if body.get("refused") is not None:
            session["refused"] = [SAFE.sub("", r) for r in body["refused"] if r]

        images = self._images(session)
        if not images:
            raise ValueError("no photos yet: take at least one photo first")
        session["duplicates"] = self._duplicates(session)

        protocol = self.protocol_for(session.get("category"))
        hint = protocol.category if protocol.category in self.catalogue_categories else None
        case = Case(
            id=session["id"],
            images=images,
            seller_text=session["text"],
            category_hint=hint,
            slots_present={p["slot"] for p in session["photos"]},
            asking_price=session["asking"],
            answers=dict(session["answers"]),
            refused_slots=set(session["refused"]),
        )
        result, report = self.valuer(case, self.tenant.tenant)
        (self.dir / session["id"] / "report.md").write_text(report)
        session["result"] = _result_record(result, report)
        session["result"]["pickup_protocol"] = list(protocol.pickup_protocol)
        session["status"] = self._status(session)
        self._save(session)
        return self.seller_view(session)

    def settle(self, sid: str, body: dict) -> dict:
        """The human final price. Every one is a calibration row."""
        session = self.load(sid)
        price = float(body.get("price") or 0)
        if price <= 0:
            raise ValueError("a settled price must be a positive number")
        r = session.get("result") or {}
        q = r.get("quote") or {}
        row = {
            "session_id": session["id"],
            "tenant": session["tenant"],
            "settled_at": _now(),
            "settled_price": price,
            "currency": self.tenant.currency,
            "note": (body.get("note") or "").strip(),
            "quoted_low": q.get("low"),
            "quoted_high": q.get("high"),
            "basis": q.get("basis"),
            "method": q.get("method"),
            "asking": session.get("asking"),
            "category": session.get("category"),
            "protocol": session.get("protocol"),
            "model_key": r.get("model_key"),
            "identified": r.get("identified"),
            "answers": session.get("answers"),
        }
        self.dir.mkdir(parents=True, exist_ok=True)
        with self.lock, (self.dir / "settlements.jsonl").open("a") as fh:
            fh.write(json.dumps(row) + "\n")
        session["settlement"] = {"price": price, "note": row["note"], "at": row["settled_at"]}
        session["status"] = "settled"
        self._save(session)
        return self.office_view(session)

    # ----- helpers -----

    def _images(self, session: dict) -> list[Path]:
        order = {s.id: i for i, s in enumerate(self.protocol_for(session.get("category")).shots)}
        photos = [p for p in session["photos"] if p["kind"] in ("photo", "frame")]
        # Photos first in protocol order, then the stills cut from clips.
        photos.sort(key=lambda p: (p["kind"] == "frame", order.get(p["slot"], 99), p["file"]))
        folder = self.dir / session["id"]
        return [folder / p["file"] for p in photos if (folder / p["file"]).exists()][:8]

    def _duplicates(self, session: dict) -> list[dict]:
        """Photos that already appeared in another seller's session.

        The same advert photos turning up under a different phone number is
        the oldest trick there is. The same seller sending the same item twice
        is not a trick, so it is noted and not flagged.
        """
        mine = [p for p in session["photos"] if p.get("phash")]
        if not mine:
            return []
        found: list[dict] = []
        for path in self.dir.glob("*/session.json"):
            other = json.loads(path.read_text())
            if other["id"] == session["id"]:
                continue
            for theirs in other.get("photos") or []:
                if not theirs.get("phash"):
                    continue
                for p in mine:
                    if _hamming(p["phash"], theirs["phash"]) <= DUPLICATE_DISTANCE:
                        found.append(
                            {
                                "file": p["file"],
                                "session_id": other["id"],
                                "same_contact": bool(session.get("contact"))
                                and session.get("contact") == other.get("contact"),
                            }
                        )
        return found

    def _status(self, session: dict) -> str:
        r = session["result"]
        if any(not d["same_contact"] for d in session["duplicates"]):
            return "review"
        code = r["quote"]["failure_code"] or ""
        if code == "FRAUD_SUSPECTED":
            return "review"
        if code == "PROVIDER_ERROR":
            return "failed"
        if code:
            return "no_price"
        if r["asks"]:
            return "needs_more"
        return "quoted"

    # ----- the two views -----

    def seller_view(self, session: dict) -> dict:
        """What the seller sees. No model names, no scores, no fraud words."""
        shape = Shape(self.protocol_for(session.get("category")), session["code"])
        by_slot: dict[str, list[dict]] = {}
        for p in session["photos"]:
            if p["kind"] == "frame":
                continue
            by_slot.setdefault(p["slot"], []).append(
                {"file": p["file"], "kind": p["kind"], "url": self._url(session, p["file"])}
            )
        shots = []
        for s in shape.shots():
            s["files"] = by_slot.get(s["slot"], [])
            s["refused"] = s["slot"] in session["refused"]
            shots.append(s)
        questions = shape.questions()
        for q in questions:
            q["answer"] = session["answers"].get(q["id"], "")
        return {
            "id": session["id"],
            "code": session["code"],
            "status": session["status"],
            "business": self.tenant.display_name or self.tenant.tenant,
            "currency": self.tenant.currency,
            "category": session.get("category"),
            "text": session["text"],
            "asking": session["asking"],
            "contact": session["contact"],
            "shots": shots,
            "extra": by_slot.get("extra", []),
            "questions": questions,
            "outcome": self._outcome(session),
        }

    def _outcome(self, session: dict) -> dict | None:
        r = session.get("result")
        if not r:
            return None
        q = r["quote"]
        code = q["failure_code"]
        cur = self.tenant.currency
        business = self.tenant.display_name or self.tenant.tenant
        next_asks = [
            {"slot": a["slot"], "ask": a["ask"].replace("{code}", session["code"]), "kind": a["kind"]}
            for a in r["asks"]
        ]
        out: dict = {"status": session["status"], "next": next_asks, "low": None, "high": None, "currency": cur}
        if session["status"] == "review":
            out["headline"] = "We need to check a few things first."
            out["detail"] = f"{business} will message you on WhatsApp."
            out["next"] = []
            return out
        if code == "NOT_PURCHASED":
            out["headline"] = f"{business} does not buy this."
            out["detail"] = q["reason"] or ""
            out["next"] = []
            return out
        if code == "PROVIDER_ERROR":
            out["headline"] = "Something went wrong on our side."
            out["detail"] = "Nothing was lost. Please press the button again in a minute."
            return out
        if code:
            out["headline"] = "We cannot price this from photos yet."
            out["detail"] = "An agent will look at it and call you."
            return out
        out["low"], out["high"] = q["low"], q["high"]
        low, high = int(q["low"]), int(q["high"])
        out["headline"] = f"{low:,} {cur}" if low == high else f"{low:,} to {high:,} {cur}"
        out["detail"] = (
            "This is the offer before we see it. The final price is agreed at pickup and can only "
            "hold or go up from the low end if what we find matches what you sent."
        )
        if q["weight_conditional"]:
            out["detail"] += " It is weighed on our scale, and the price follows the scale."
        out["conditions"] = _seller_conditions(r)
        out["pickup"] = list(r.get("pickup_protocol") or [])
        return out

    def office_view(self, session: dict) -> dict:
        view = dict(session)
        view["photos"] = [
            {**p, "url": self._url(session, p["file"])} for p in session["photos"]
        ]
        view["seller"] = self.seller_view(session)
        return view

    def _url(self, session: dict, file: str) -> str:
        return f"/files/sessions/{session['id']}/{file}"


def _seller_conditions(r: dict) -> list[str]:
    """The conditions a seller can act on, in their words not the engine's."""
    out: list[str] = []
    for claim in r["claims"]:
        if claim["status"] == "supported" or claim["text"].startswith("Required evidence"):
            continue
        line = f"You said: {claim['text'].strip().rstrip('.')}."
        if claim.get("pickup_check"):
            line += f" At pickup: {claim['pickup_check'].strip().rstrip('.').lower()}."
        out.append(line)
    return out[:8]


def _result_record(result: CaseResult, report: str) -> dict:
    """The engine's answer, flattened so the back office can read it later."""
    c, q, a = result.chain, result.quote, result.assessment
    return {
        "report": report,
        "reader": result.reader_model,
        "reasoner": result.reasoner_model,
        "category": c.category,
        "identified": result.identified,
        "model_key": c.model_key,
        "failure_code": c.failure_code,
        "reason": c.reason,
        "fraud_flags": list(c.fraud_flags),
        "quote": {
            "failure_code": q.failure_code,
            "reason": q.reason,
            "low": q.low,
            "high": q.high,
            "currency": q.currency,
            "basis": q.basis,
            "method": q.method,
            "floor": q.floor,
            "weight_conditional": q.weight_conditional,
            "observation_count": q.observation_count,
            "explanation": q.explanation,
            "conditions": list(q.conditions),
        },
        "assessment": None
        if a is None
        else {
            "percent": a.percent,
            "band": a.band,
            "sentence": a.sentence(),
            "price_confidence": int(a.price_confidence * 100),
            "drivers": list(a.drivers),
            "alternatives": [{"name": n, "score": s} for n, s in a.alternatives],
        },
        "asks": [{"kind": x.kind, "ask": x.ask, "because": x.because, "slot": x.slot} for x in result.asks],
        "questions": [{"id": x.id, "ask": x.ask, "kind": x.kind} for x in result.questions],
        "answer_notes": list(result.answer_notes),
        "claims": [
            {
                "status": str(getattr(cl.status, "value", cl.status)),
                "text": cl.text,
                "worst_case": cl.worst_case,
                "pickup_check": cl.pickup_check,
            }
            for cl in result.ledger
        ],
        "pickup_protocol": [],
        "cost_usd": result.cost_usd,
        "spent_usd": result.spent_usd,
        "latency_ms": result.latency_ms,
        "error": result.error,
    }
