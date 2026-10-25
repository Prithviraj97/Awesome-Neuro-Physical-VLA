"""Regenerate the data-driven parts of README.md.

Only text between <!-- BEGIN:x --> and <!-- END:x --> markers is replaced;
everything else in README.md is hand-written and left alone.

    python scripts/build_readme.py                     # verified entries only
    python scripts/build_readme.py --include-unverified  # preview, marks unverified with †
"""
import argparse
import datetime as dt
import re
from collections import defaultdict
from common import ROOT, papers, taxonomy, latency, all_codes

README = ROOT / "README.md"


def anchor(text):
    a = re.sub(r"[^\w\- ]", "", text.lower()).strip().replace(" ", "-")
    return a


def links(p):
    out = []
    if p.get("arxiv"):
        out.append(f"[arXiv](https://arxiv.org/abs/{p['arxiv']})")
    if p.get("url"):
        out.append(f"[page]({p['url']})")
    if p.get("code"):
        out.append(f"[code]({p['code']})")
    return " · ".join(out)


def paper_line(p, show_flag):
    tags = " ".join(f"`{c}`" for c in p["categories"])
    flag = " †" if show_flag and not p.get("verified") else ""
    return (f"- **{p['title']}**{flag}  \n"
            f"  {p['authors']} · *{p['venue']}* · {p['year']} · {links(p)} · {tags}  \n"
            f"  {p['note']}")


def section_overview(tax):
    rows = ["| Axis | Code | Category | Assign a paper here if… |",
            "| :--- | :--- | :--- | :--- |"]
    for axis, a in tax.items():
        if axis in ("T", "S"):
            continue
        for code, c in a["categories"].items():
            rows.append(f"| {axis}. {a['title']} | `{code}` | {c['title']} | {c['rule']} |")
    return "\n".join(rows)


def section_papers(tax, ps, show_unverified):
    by_cat = defaultdict(list)
    for p in ps:
        if p.get("verified") or show_unverified:
            by_cat[p["categories"][0]].append(p)
    out = []
    for axis, a in tax.items():
        head = f"{a['title']}" if axis in ("T", "S") else f"Axis {axis}: {a['title']}"
        out.append(f"### {head}\n\n*{a['blurb']}*\n")
        for code, c in a["categories"].items():
            items = sorted(by_cat.get(code, []), key=lambda p: (-int(p["year"]), p["title"]))
            if not items:
                continue
            out.append(f"#### `{code}` {c['title']}\n")
            out.extend(paper_line(p, show_unverified) for p in items)
            out.append("")
    return "\n".join(out).rstrip()


def section_latency(ps):
    by_id = {p["id"]: p for p in ps}
    rows = [r for r in latency() if r.get("verified")]
    if not rows:
        return ("*No verified timing records yet. Every row needs the device, precision, "
                "what was timed, and a pointer to the source table or log; see "
                "[docs/latency-reporting.md](docs/latency-reporting.md).*")
    out = []
    for kind, label in (("policy", "Policies (per inference call)"),
                        ("controller", "Controllers (per solve)")):
        sub = [r for r in rows if r["kind"] == kind]
        if not sub:
            continue
        out.append(f"**{label}**\n")
        out.append("| Method | Params | Latency (ms) | Statistic | What is timed | Hardware | Precision | Origin | Source |")
        out.append("| :--- | :--- | ---: | :--- | :--- | :--- | :--- | :--- | :--- |")
        for r in sorted(sub, key=lambda r: str(r["latency_ms"])):
            p = by_id[r["paper"]]
            out.append(f"| {p['title'].split(':')[0]} | {r.get('params', '–')} | {r['latency_ms']} | "
                       f"{r['statistic']} | {r['what_is_timed']} | {r['hardware']} | {r['precision']} | "
                       f"{r['origin']} | {r['source']} |")
        out.append("")
    return "\n".join(out).rstrip()


def section_stats(ps, show_unverified):
    n = sum(1 for p in ps if p.get("verified") or show_unverified)
    today = dt.date.today().isoformat()
    note = " † = listed but not yet checked against the paper." if show_unverified else ""
    return f"*{n} papers · last generated {today}.{note}*"


def replace_block(text, name, body):
    pat = re.compile(rf"(<!-- BEGIN:{name} -->)(.*?)(<!-- END:{name} -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"README.md is missing the {name} markers")
    return pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-unverified", action="store_true")
    args = ap.parse_args()
    tax, ps = taxonomy(), papers()
    text = README.read_text(encoding="utf-8")
    text = replace_block(text, "stats", section_stats(ps, args.include_unverified))
    text = replace_block(text, "overview", section_overview(tax))
    text = replace_block(text, "latency", section_latency(ps))
    text = replace_block(text, "papers", section_papers(tax, ps, args.include_unverified))
    README.write_text(text, encoding="utf-8")
    print("README.md updated")


if __name__ == "__main__":
    main()
