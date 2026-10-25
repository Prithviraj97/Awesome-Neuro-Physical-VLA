"""Compare each arXiv id in papers.yaml against the title arXiv returns.

Catches wrong ids and title typos. Uses the public arXiv API
(export.arxiv.org); please keep the polite delay.

    python scripts/check_arxiv.py
"""
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from common import papers

API = "http://export.arxiv.org/api/query?id_list={}&max_results=1"
NS = {"a": "http://www.w3.org/2005/Atom"}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def fetch_title(arxiv_id):
    with urllib.request.urlopen(API.format(arxiv_id), timeout=30) as resp:
        root = ET.fromstring(resp.read())
    entry = root.find("a:entry", NS)
    if entry is None:
        return None
    t = entry.find("a:title", NS)
    return " ".join(t.text.split()) if t is not None and t.text else None


def main():
    bad = 0
    for p in papers():
        ax = p.get("arxiv")
        if not ax:
            continue
        try:
            remote = fetch_title(ax)
        except Exception as e:  # network errors should not hide other results
            print(f"?? {p['id']}: request failed ({e})")
            continue
        if not remote:
            print(f"XX {p['id']}: {ax} not found on arXiv")
            bad += 1
        else:
            score = SequenceMatcher(None, norm(p["title"]), norm(remote)).ratio()
            flag = "ok" if score > 0.9 else "XX"
            if flag == "XX":
                bad += 1
            print(f"{flag} {p['id']}: {score:.2f}  local='{p['title']}'  arxiv='{remote}'")
        time.sleep(3)
    print(f"\n{bad} mismatches")


if __name__ == "__main__":
    main()
