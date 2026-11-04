"""A short top-up set: every example the fix changed, plus as many unchanged
ones drawn at random, so the run goes on from run 6 without forgetting.

    python topup_set.py <old sft> <new sft> <out> [--extra 1.0]

Changed: in the new set and not in the old with the same answer (by id and
variant), or in the old and gone from the new (a price step for an advert
that now asks for its label). Gone examples cannot be taught by leaving them
out, so they are counted, not written.
"""
import argparse
import hashlib
import json
from collections import Counter

p = argparse.ArgumentParser()
p.add_argument("old")
p.add_argument("new")
p.add_argument("out")
p.add_argument("--extra", type=float, default=1.0, help="Unchanged examples per changed one.")
a = p.parse_args()


def key(e):
    return (e["id"], e["variant"])


def answer(e):
    return e["messages"][-1]["content"]


old = {}
with open(a.old) as f:
    for line in f:
        e = json.loads(line)
        old[key(e)] = hashlib.md5(answer(e).encode()).hexdigest()

changed, same = [], []
kinds = Counter()
seen = set()
with open(a.new) as f:
    for line in f:
        e = json.loads(line)
        k = key(e)
        seen.add(k)
        h = hashlib.md5(answer(e).encode()).hexdigest()
        if old.get(k) == h:
            same.append(line)
            continue
        changed.append(line)
        try:
            out = json.loads(answer(e))
            kinds[(e["variant"].split("_")[0], out.get("decision"), (out.get("identity") or {}).get("kind"))] += 1
        except Exception:
            kinds[(e["variant"], "not json", None)] += 1
gone = Counter(k[1] for k in old if k not in seen)

# The unchanged ones by a fixed hash of their key, so a rebuild picks the same.
same.sort(key=lambda line: hashlib.md5(line[:200].encode()).hexdigest())
take = same[: int(len(changed) * a.extra)]
rows = changed + take
rows.sort(key=lambda line: hashlib.md5(line[:120].encode()).hexdigest())
with open(a.out, "w") as f:
    f.writelines(rows)
print(f"changed {len(changed)}, unchanged kept {len(take)} of {len(same)}, gone from the new set {sum(gone.values())}"
      f" {dict(gone.most_common(6))}; wrote {len(rows)} to {a.out}")
for (variant, decision, kind), n in kinds.most_common(25):
    print(f"{n:6}  {variant:10} {decision!s:16} {kind}")
