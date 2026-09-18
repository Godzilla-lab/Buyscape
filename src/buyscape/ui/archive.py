"""Sessions outlive the machine they were valued on.

A free Space is wiped when it restarts, and a session folder is the product's
only record of what a seller sent, what the engine said and what a person
finally paid. So every finished session is copied to a private dataset repo
on the Hub, and on startup whatever is there and not here is copied back.
That dataset is also the training data the business is collecting.

Uploads run on their own thread and a failed upload is logged, never raised:
a seller must never wait on, or lose an offer to, the backup.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path

log = logging.getLogger("buyscape.archive")

IGNORE = ("*.tmp",)


class HubArchive:
    """One private dataset repo, one folder per session."""

    def __init__(self, repo_id: str, token: str) -> None:
        self.repo_id = repo_id
        self._token = token
        self._lock = threading.Lock()

    def _api(self):
        from huggingface_hub import HfApi

        return HfApi(token=self._token)

    def ensure(self) -> None:
        self._api().create_repo(self.repo_id, repo_type="dataset", private=True, exist_ok=True)

    def upload(self, session_dir: Path) -> None:
        """Copy one session folder up, replacing what was there for it."""
        with self._lock:
            self._api().upload_folder(
                folder_path=str(session_dir),
                repo_id=self.repo_id,
                repo_type="dataset",
                path_in_repo=session_dir.name,
                commit_message=f"session {session_dir.name}",
                ignore_patterns=list(IGNORE),
            )

    def upload_file(self, path: Path) -> None:
        with self._lock:
            self._api().upload_file(
                path_or_fileobj=str(path),
                path_in_repo=path.name,
                repo_id=self.repo_id,
                repo_type="dataset",
                commit_message=f"update {path.name}",
            )

    def upload_later(self, session_dir: Path, extra: Path | None = None) -> threading.Thread:
        def work() -> None:
            try:
                self.upload(session_dir)
                if extra is not None and extra.exists():
                    self.upload_file(extra)
            except Exception as exc:  # the backup never costs a seller anything
                log.warning("backup of %s failed: %s", session_dir.name, exc)

        thread = threading.Thread(target=work, daemon=True)
        thread.start()
        return thread

    def restore(self, sessions_dir: Path) -> int:
        """Bring back every session the disk does not have. Returns how many."""
        from huggingface_hub import snapshot_download

        sessions_dir.mkdir(parents=True, exist_ok=True)
        try:
            files = self._api().list_repo_files(self.repo_id, repo_type="dataset")
        except Exception as exc:
            log.warning("restore skipped: %s", exc)
            return 0
        remote = {f.split("/", 1)[0] for f in files if "/" in f}
        missing = sorted(s for s in remote if not (sessions_dir / s / "session.json").exists())
        if not missing and "settlements.jsonl" not in files:
            return 0
        patterns = [f"{s}/*" for s in missing] + (["settlements.jsonl"] if "settlements.jsonl" in files else [])
        snapshot_download(
            self.repo_id, repo_type="dataset", token=self._token, local_dir=str(sessions_dir),
            allow_patterns=patterns,
        )
        return len(missing)


def from_env(env: dict) -> HubArchive | None:
    repo = env.get("BUYSCAPE_ARCHIVE_REPO")
    token = env.get("HF_TOKEN")
    return HubArchive(repo, token) if repo and token else None
