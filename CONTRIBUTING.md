# Contributing

Thanks for helping. The README is generated, so all changes go through the files in `data/`.

## Add a paper

1. Check the paper meets the scope rule in [docs/taxonomy.md](docs/taxonomy.md) and is public (peer-reviewed, arXiv, or a technical report with method detail).
2. Add an entry to `data/papers.yaml`. Use the exact title, a one-line note in your own words saying what the paper contributes to this list, and taxonomy codes (primary first).
3. Run:
   ```bash
   pip install pyyaml
   python scripts/validate.py
   python scripts/build_readme.py
   ```
4. Open a pull request. The maintainer sets `verified: true` after checking the entry.

Prefer an issue instead? Use the **Add a paper** issue form.

## Add a timing record

Follow [docs/latency-reporting.md](docs/latency-reporting.md). Rows missing hardware, precision, what was timed, or a source will not be merged.

## Corrections

If an entry is wrong (title, venue, category, or note), open a **Correction** issue or a pull request. Authors correcting descriptions of their own work are especially welcome.

## Self-promotion

Adding your own paper is fine. It goes through the same criteria and the note should describe what the paper does, not how good it is.
