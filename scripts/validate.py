"""Validate data files. Exit code 1 on any error (used by CI)."""
import re
import sys
from common import papers, taxonomy, latency, all_codes

REQUIRED_PAPER = ["id", "title", "authors", "year", "venue", "categories", "note", "verified"]
REQUIRED_LAT = ["paper", "kind", "origin", "latency_ms", "what_is_timed",
                "statistic", "hardware", "precision", "source"]
ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}$")


def main():
    errors, warnings = [], []
    codes = all_codes(taxonomy())
    ps = papers()
    ids = set()

    for p in ps:
        pid = p.get("id", "<missing id>")
        for k in REQUIRED_PAPER:
            if p.get(k) in (None, "", []):
                errors.append(f"{pid}: missing '{k}'")
        if pid in ids:
            errors.append(f"{pid}: duplicate id")
        ids.add(pid)
        for c in p.get("categories", []):
            if c not in codes:
                errors.append(f"{pid}: unknown category '{c}'")
        ax = p.get("arxiv")
        if ax and not ARXIV_RE.match(str(ax)):
            errors.append(f"{pid}: arxiv id '{ax}' should look like 2406.09246 (no version)")
        if not ax and not p.get("url"):
            errors.append(f"{pid}: needs either 'arxiv' or 'url'")
        if len(p.get("note", "")) > 220:
            warnings.append(f"{pid}: note longer than 220 characters")
        if not p.get("verified"):
            warnings.append(f"{pid}: not yet verified")

    titles = {}
    for p in ps:
        t = p.get("title", "").lower().strip()
        if t in titles:
            errors.append(f"{p['id']}: same title as {titles[t]}")
        titles[t] = p.get("id")

    for r in latency():
        pid = r.get("paper")
        if pid not in ids:
            errors.append(f"latency: unknown paper '{pid}'")
        if r.get("kind") not in ("policy", "controller"):
            errors.append(f"latency {pid}: kind must be policy or controller")
        if r.get("origin") not in ("reported", "measured"):
            errors.append(f"latency {pid}: origin must be reported or measured")
        if r.get("verified"):
            for k in REQUIRED_LAT:
                if r.get(k) in (None, ""):
                    errors.append(f"latency {pid}: verified row missing '{k}'")

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    n_ver = sum(1 for p in ps if p.get("verified"))
    print(f"\n{len(ps)} papers ({n_ver} verified), {len(latency())} timing records, "
          f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
