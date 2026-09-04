"""The candidate catalogue and the retrieval that queries it.

Retrieval is the single largest lever on open-world identification: published
work puts fine-grained identity at 13 percent from the image alone, 48.8 with
automatic retrieval and 87 with perfect retrieval. So the model never answers
from the photo alone, it ranks a shortlist this module produces.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

_TOKEN = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "the", "a", "an", "for", "with", "and", "of", "in", "very", "clean",
    "sharp", "good", "new", "used", "original", "quality", "sale", "price",
    "brand", "condition", "tokunbo", "uk", "us", "neat", "perfect", "working",
}


def tokens(text: str) -> list[str]:
    return [t for t in _TOKEN.findall((text or "").lower()) if t not in STOPWORDS]


@dataclass(frozen=True)
class Entry:
    """One catalogue row. `attrs` carries interior facts where they are known."""

    category: str
    brand: str
    model: str
    variant: str | None
    aliases: tuple[str, ...]
    attrs: dict[str, str] = field(default_factory=dict)

    @property
    def key(self) -> str:
        parts = [self.brand, self.model]
        if self.variant:
            parts.append(self.variant)
        return " ".join(parts)

    @property
    def search_text(self) -> str:
        return " ".join([self.brand, self.model, self.variant or "", *self.aliases])


def _parse_attrs(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in (raw or "").split(";"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def load_catalogue(root: Path) -> dict[str, list[Entry]]:
    """Read every <category>.csv under root."""
    catalogue: dict[str, list[Entry]] = {}
    for path in sorted(root.glob("*.csv")):
        category = path.stem
        entries: list[Entry] = []
        with path.open(newline="") as fh:
            for row in csv.DictReader(fh):
                if not (row.get("brand") and row.get("model")):
                    continue
                entries.append(
                    Entry(
                        category=category,
                        brand=row["brand"].strip(),
                        model=row["model"].strip(),
                        variant=(row.get("variant") or "").strip() or None,
                        aliases=tuple(
                            a.strip()
                            for a in (row.get("aliases") or "").split("|")
                            if a.strip()
                        ),
                        attrs=_parse_attrs(row.get("attrs") or ""),
                    )
                )
        catalogue[category] = entries
    return catalogue


def _score(query_tokens: list[str], entry: Entry) -> float:
    """Token overlap weighted so a matching model number beats a matching brand."""
    if not query_tokens:
        return 0.0
    qs = set(query_tokens)
    brand_tokens = set(tokens(entry.brand))
    model_tokens = set(tokens(entry.model))
    alias_tokens = set(tokens(" ".join(entry.aliases)))
    variant_tokens = set(tokens(entry.variant or ""))

    brand_hit = len(qs & brand_tokens) / max(len(brand_tokens), 1)
    model_hit = len(qs & (model_tokens | alias_tokens)) / max(
        len(model_tokens | alias_tokens), 1
    )
    variant_hit = len(qs & variant_tokens) / max(len(variant_tokens), 1) if variant_tokens else 0.0

    # A phrase match on an alias is the strongest single signal.
    phrase = 0.0
    joined = " ".join(query_tokens)
    for alias in (*entry.aliases, entry.model.lower()):
        if alias and alias.lower() in joined:
            phrase = 1.0
            break

    return round(
        0.30 * brand_hit + 0.40 * model_hit + 0.10 * variant_hit + 0.20 * phrase, 4
    )


def search(
    catalogue: dict[str, list[Entry]],
    query: str,
    category: str | None = None,
    limit: int = 5,
    min_score: float = 0.15,
) -> list[tuple[Entry, float]]:
    """Return the best catalogue entries for a free-text query."""
    qt = tokens(query)
    pool: list[Entry] = []
    if category and category in catalogue:
        pool = catalogue[category]
    else:
        for entries in catalogue.values():
            pool.extend(entries)
    scored = [(e, _score(qt, e)) for e in pool]
    scored = [(e, s) for e, s in scored if s >= min_score]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:limit]
