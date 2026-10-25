"""Shared loaders for the data files."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def papers():
    return load("papers.yaml") or []


def taxonomy():
    return load("taxonomy.yaml")["axes"]


def latency():
    return (load("latency.yaml") or {}).get("records", []) or []


def all_codes(tax=None):
    tax = tax or taxonomy()
    return {code: (axis, cat) for axis, a in tax.items() for code, cat in a["categories"].items()}
