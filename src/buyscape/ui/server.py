"""A local test page for the engine.

Not infrastructure. One page on localhost so a person can drop photos in,
pick a model pair, and read what the engine says before anything is launched.
It runs the same code path as `buyscape assess`, writes the same report.md,
and records and replays the same fixtures. Nothing here is a product surface:
no accounts, no database, no API contract. Kill the process and it is gone.
"""

from __future__ import annotations

import base64
import json
import re
import threading
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

from .. import cli as _cli
from ..evalset import buyscrap, jiji, score
from ..identify.catalogue import load_catalogue
from ..pricing.sources import JijiComps, MaterialsFloor, ScrapIndex
from ..protocols.schema import load_protocols
from ..runner import Case, CaseResult, report_markdown, run_case
from ..tenant import load_tenant

PAGE = Path(__file__).with_name("page.html")
SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


class Engine:
    """Everything a valuation needs, loaded once and shared between requests."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.protocols = load_protocols(root / "protocols")
        self.catalogue = load_catalogue(root / "catalogue")
        prices = root / "eval" / "prices"
        self.pool = prices if prices.exists() else root / "eval" / "raw"
        index = root / "tenants" / "scrap_index_lagos.yaml"
        self.scrap = ScrapIndex(index)
        self.materials = MaterialsFloor(index)
        self.fixtures = root / "eval" / "fixtures"
        self.inbox = root / "eval" / "inbox"
        self.lock = threading.Lock()

    # ----- what the page needs to draw itself -----

    def meta(self) -> dict:
        _cli._load_dotenv(self.root / ".env")
        import os

        return {
            "presets": [
                {"name": name, "reader": r, "reasoner": s} for name, (r, s) in _cli.PRESETS.items()
            ],
            "default_preset": "balanced",
            "corroborator": _cli.DEFAULT_CORROBORATOR,
            "keys": {
                "openrouter": bool(os.environ.get("OPENROUTER_API_KEY")),
                "google": bool(os.environ.get("GOOGLE_API_KEY")),
                "xai": bool(os.environ.get("XAI_API_KEY")),
            },
            "tenants": sorted(
                p.stem for p in (self.root / "tenants").glob("*.yaml") if p.stem != "scrap_index_lagos"
            ),
            "protocols": {
                name: {
                    "questions": [
                        {"id": q.id, "ask": q.ask, "kind": q.kind, "options": q.options, "unit": q.unit}
                        for q in p.questions
                    ]
                }
                for name, p in self.protocols.items()
            },
        }

    def testset(self, which: str) -> list[dict]:
        raw = self.root / "eval" / "raw"
        rows: list[dict] = []
        seen: set[str] = set()
        if which == "buyscrap":
            listings = buyscrap.load(raw / "buyscrap")
            media_root = raw / "buyscrap" / "media"
        else:
            listings = jiji.load(raw)
            media_root = raw / "media"
        for listing in listings:
            if listing.id in seen:
                continue
            seen.add(listing.id)
            images = [media_root / rel for rel in listing.media]
            images = [p for p in images if p.exists()]
            if not images:
                continue
            rows.append(
                {
                    "id": listing.id,
                    "set": which,
                    "category": listing.category,
                    "answer_key": listing.title,
                    "asking_ngn": listing.price_ngn,
                    "text": listing.description,
                    "images": [self._url(p) for p in images[:6]],
                }
            )
        return rows

    def _find_case(self, which: str, case_id: str) -> Case | None:
        raw = self.root / "eval" / "raw"
        if which == "buyscrap":
            cases = _cli._load_buyscrap_cases(raw / "buyscrap", None)
        else:
            cases = _cli._load_cases(raw, None, None)
        for case in cases:
            if case.id == case_id:
                return case
        return None

    def runs(self) -> list[dict]:
        proof = self.root / "docs" / "proof"
        out: list[dict] = []
        for run_dir in sorted(p for p in proof.iterdir() if p.is_dir()):
            summary_file = run_dir / "summary.json"
            summary = json.loads(summary_file.read_text()) if summary_file.exists() else None
            cases_dir = run_dir / "cases"
            cases = sorted(p.stem for p in cases_dir.glob("*.md")) if cases_dir.exists() else []
            gate = (
                [
                    {"metric": n, "measured": m, "needs": t, "passed": p}
                    for n, m, t, p in score.gate_table(summary)
                ]
                if summary
                else []
            )
            out.append({"name": run_dir.name, "summary": summary, "gate": gate, "cases": cases})
        return out

    def report(self, run: str, case_id: str) -> str | None:
        path = self.root / "docs" / "proof" / SAFE_NAME.sub("", run) / "cases" / f"{SAFE_NAME.sub('', case_id)}.md"
        if run != SAFE_NAME.sub("", run) or not path.exists():
            return None
        return path.read_text()

    # ----- running one valuation -----

    def value(self, body: dict) -> dict:
        _cli._load_dotenv(self.root / ".env")
        preset = body.get("preset") or "balanced"
        if preset == "fake":
            pair = ("fake", "fake")  # exercises the pipeline without a model
        elif preset in _cli.PRESETS:
            pair = _cli.PRESETS[preset]
        else:
            raise ValueError(f"unknown preset {preset!r}")
        reader = body.get("reader") or pair[0]
        reasoner = body.get("reasoner") or pair[1]
        corroborator = body.get("corroborator") or _cli.DEFAULT_CORROBORATOR
        if reader == "fake" or reasoner == "fake":
            corroborator = "none"
        mode = body.get("mode") or "auto"
        if mode not in ("record", "replay", "auto"):
            raise ValueError(f"unknown mode {mode!r}")
        tenant_name = body.get("tenant") or "buyscrap_ng"
        tenant_file = self.root / "tenants" / f"{SAFE_NAME.sub('', tenant_name)}.yaml"
        if not tenant_file.exists():
            raise ValueError(f"no tenant file at {tenant_file}")
        tenant = load_tenant(tenant_file)

        text = (body.get("text") or "").strip()
        asking = float(body.get("asking") or 0) or None
        answers = {str(k): str(v) for k, v in (body.get("answers") or {}).items() if str(v).strip()}

        exclude: frozenset[str] = frozenset()
        folder: Path | None = None
        if body.get("case_id"):
            case = self._find_case(body.get("set") or "jiji", body["case_id"])
            if case is None:
                raise ValueError(f"no cached case {body['case_id']!r}")
            # A listing must never be its own comparable price.
            exclude = frozenset({case.id})
            if text:
                case.seller_text = text
            case.asking_price = asking
            case.answers = answers
        else:
            folder = self._write_inbox(body.get("photos") or [], text, answers, body.get("label") or "")
            case = _cli.load_folder_case(folder, asking=asking)

        comps = JijiComps(self.pool, exclude_ids=exclude)
        reader_p = _cli._provider(reader, self.fixtures, mode)
        reasoner_p = _cli._provider(reasoner, self.fixtures, mode)
        corroborator_p = None if corroborator in ("", "none") else _cli._provider(corroborator, self.fixtures, mode)

        result = run_case(
            case, self.protocols, self.catalogue, comps, self.scrap, reader_p, reasoner_p,
            self.materials, corroborator_p, tenant,
        )
        report = report_markdown(case, result)
        if folder is not None:
            (folder / "report.md").write_text(report)
        return self._payload(case, result, report, folder, reader, reasoner)

    def _write_inbox(self, photos: list[dict], text: str, answers: dict, label: str) -> Path:
        if not photos:
            raise ValueError("no photos: drop at least one photo, or pick a cached case")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        slug = SAFE_NAME.sub("-", label).strip("-")[:40]
        folder = self.inbox / (f"{stamp}-{slug}" if slug else stamp)
        folder.mkdir(parents=True, exist_ok=True)
        for i, photo in enumerate(photos, 1):
            name = SAFE_NAME.sub("_", Path(photo.get("name") or f"photo{i}.jpg").name)
            if not name or name.startswith("."):
                name = f"photo{i}.jpg"
            data = photo.get("data") or ""
            if "," in data:  # a data: URL from the browser
                data = data.split(",", 1)[1]
            (folder / name).write_bytes(base64.b64decode(data))
        if text:
            (folder / "seller.txt").write_text(text + "\n")
        if answers:
            (folder / "answers.yaml").write_text(yaml.safe_dump(answers, sort_keys=True))
        return folder

    def _payload(
        self, case: Case, result: CaseResult, report: str, folder: Path | None, reader: str, reasoner: str
    ) -> dict:
        c, q, a = result.chain, result.quote, result.assessment
        return {
            "case_id": case.id,
            "folder": None if folder is None else str(folder.relative_to(self.root) if self.root in folder.parents else folder),
            "images": [self._url(p) for p in case.images],
            "report": report,
            "reader": reader,
            "reasoner": reasoner,
            "category": c.category,
            "identified": result.identified,
            "model_key": c.model_key,
            "failure_code": c.failure_code,
            "reason": c.reason,
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
                "conditions": q.conditions,
            },
            "assessment": None
            if a is None
            else {
                "percent": a.percent,
                "band": a.band,
                "sentence": a.sentence(),
                "price_confidence": int(a.price_confidence * 100),
                "drivers": a.drivers,
                "alternatives": [{"name": n, "score": s} for n, s in a.alternatives],
            },
            "asks": [{"kind": x.kind, "ask": x.ask, "because": x.because, "slot": x.slot} for x in result.asks],
            "questions": [
                {"id": x.id, "ask": x.ask, "kind": x.kind, "options": list(x.options), "unit": x.unit}
                for x in result.questions
            ],
            "answer_notes": result.answer_notes,
            "claims": [
                {"status": str(cl.status), "text": cl.text, "worst_case": cl.worst_case, "pickup_check": cl.pickup_check}
                for cl in result.ledger
            ],
            "cost_usd": result.cost_usd,
            "spent_usd": result.spent_usd,
            "latency_ms": result.latency_ms,
            "cost_by_task": result.cost_by_task,
            "error": result.error,
            "answer_key": case.truth or None,
        }

    def _roots(self) -> dict[str, Path]:
        """The only directories the page may read photos from."""
        return {"inbox": self.inbox.resolve(), "eval": (self.root / "eval").resolve()}

    def _url(self, path: Path) -> str:
        target = path.resolve()
        for name, base in self._roots().items():
            if base in target.parents:
                return f"/files/{name}/" + "/".join(target.relative_to(base).parts)
        raise ValueError(f"{path} is outside the directories the page serves")

    def file(self, url_path: str) -> Path | None:
        name, _, rest = unquote(url_path).partition("/")
        base = self._roots().get(name)
        if base is None:
            return None
        target = (base / rest).resolve()
        if base not in target.parents or not target.is_file():
            return None
        return target


class Handler(BaseHTTPRequestHandler):
    engine: Engine  # set on the server class

    def log_message(self, fmt: str, *args) -> None:  # quiet, the console is for results
        pass

    def _send(self, status: int, body: bytes, ctype: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload) -> None:
        self._send(status, json.dumps(payload, default=str).encode())

    def do_GET(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        eng = self.server.engine  # type: ignore[attr-defined]
        try:
            if not parts:
                self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
            elif parts == ["api", "meta"]:
                self._json(200, eng.meta())
            elif parts == ["api", "runs"]:
                self._json(200, eng.runs())
            elif len(parts) == 5 and parts[:2] == ["api", "runs"] and parts[3] == "cases":
                text = eng.report(unquote(parts[2]), unquote(parts[4]))
                if text is None:
                    self._json(404, {"error": "no such report"})
                else:
                    self._json(200, {"report": text})
            elif parts[:2] == ["api", "testset"] and len(parts) == 3:
                self._json(200, eng.testset(parts[2]))
            elif parts and parts[0] == "files":
                path = eng.file("/".join(parts[1:]))
                if path is None:
                    self._json(404, {"error": "no such file"})
                else:
                    ctype = {"png": "image/png", "webp": "image/webp"}.get(path.suffix.lower().lstrip("."), "image/jpeg")
                    self._send(200, path.read_bytes(), ctype)
            else:
                self._json(404, {"error": "not found"})
        except Exception as exc:  # a test page must say what broke, never hang
            self._json(500, {"error": f"{type(exc).__name__}: {exc}"})

    def do_POST(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        eng = self.server.engine  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError as exc:
            self._json(400, {"error": f"bad json: {exc}"})
            return
        if url.path != "/api/value":
            self._json(404, {"error": "not found"})
            return
        try:
            self._json(200, eng.value(body))
        except ValueError as exc:
            self._json(400, {"error": str(exc)})
        except Exception as exc:
            self._json(500, {"error": f"{type(exc).__name__}: {exc}"})


class UiServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], engine: Engine) -> None:
        super().__init__(address, Handler)
        self.engine = engine


def make_server(root: Path, host: str = "127.0.0.1", port: int = 8765) -> UiServer:
    return UiServer((host, port), Engine(root))


def serve(root: Path, host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> None:
    server = make_server(root, host, port)
    url = f"http://{host}:{server.server_address[1]}/"
    print(f"Buyscape test page at {url}  (Ctrl+C stops it)")
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
