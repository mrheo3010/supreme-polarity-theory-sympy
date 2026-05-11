#!/usr/bin/env python3
"""
Build INVENTORY.md + docs/by-batch/*.md + docs/by-law/*.md from the
docstrings of every scripts/spt_*.py file in the repo root.

Run after a sync to keep all index files consistent with the actual
script set. The sync workflow calls this automatically; you can also
run it locally:

    python3 .github/scripts/build_inventory.py
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
INVENTORY_PATH = REPO_ROOT / "INVENTORY.md"
DOCS_DIR = REPO_ROOT / "docs"
BY_BATCH_DIR = DOCS_DIR / "by-batch"
BY_LAW_DIR = DOCS_DIR / "by-law"


@dataclass
class ScriptInfo:
    filename: str
    title: str = ""
    law_id: Optional[int] = None
    dot: Optional[int] = None
    version: str = ""
    date: str = ""
    tier: str = ""
    brief: str = ""
    description: str = ""  # multi-line description, first paragraph after header

    @property
    def name_no_ext(self) -> str:
        return self.filename.replace(".py", "")

    @property
    def tier_label(self) -> str:
        # Normalize tier text like "Tier-B PASS", "B-PASS", "B EXACT", etc.
        t = self.tier.upper().replace("TIER-", "").replace("TIER", "").strip()
        return t if t else "—"

    @property
    def law_label(self) -> str:
        if self.law_id is None:
            return "—"
        return f"Law {self.law_id}"

    @property
    def dot_label(self) -> str:
        if self.dot is None:
            return "Foundation"
        return f"Đợt {self.dot}"


# ──────────────────────────────────────────────────────────────────────
# Docstring parsing
# ──────────────────────────────────────────────────────────────────────

# Match the FIRST triple-quoted docstring anywhere in the file (handles
# scripts that have an `import sys; sys.stdout.reconfigure(...)` preamble
# above the docstring, as well as docstrings at line 1).
DOCSTRING_RE = re.compile(r'"""(.*?)"""', re.S)
LAW_RE = re.compile(r"\bSPT\s+Law\s+(\d+)\b", re.IGNORECASE)
DOT_RE = re.compile(r"\b(?:Đợt|Dot|Dợt)\s+(\d+)\b", re.IGNORECASE)
VERSION_RE = re.compile(r"\bv(\d+\.\d+)\b")
DATE_RE = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
TIER_RE = re.compile(
    r"\bTier[\s\-]*([AB])[\s\-]*(EXACT|PASS|META)?\b",
    re.IGNORECASE,
)


def parse_script(p: Path) -> ScriptInfo:
    info = ScriptInfo(filename=p.name)
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return info
    m = DOCSTRING_RE.search(text)
    if not m:
        return info
    doc = m.group(1).strip()

    # Title = first non-empty line that isn't a divider
    lines = [ln.rstrip() for ln in doc.splitlines()]
    title = ""
    for ln in lines:
        stripped = ln.strip()
        if not stripped:
            continue
        if set(stripped) <= {"=", "-", "_", "─", "═"}:
            continue
        title = stripped
        break
    info.title = title

    # Extract Law/Đợt/version/date/tier from the entire docstring
    m = LAW_RE.search(doc)
    if m:
        info.law_id = int(m.group(1))
    m = DOT_RE.search(doc)
    if m:
        info.dot = int(m.group(1))
    m = VERSION_RE.search(doc)
    if m:
        info.version = "v" + m.group(1)
    m = DATE_RE.search(doc)
    if m:
        info.date = m.group(1)
    m = TIER_RE.search(doc)
    if m:
        tier_letter = m.group(1).upper()
        tier_suffix = (m.group(2) or "").upper()
        info.tier = f"{tier_letter}-{tier_suffix}" if tier_suffix else tier_letter

    # Description = first paragraph (after header/decoration lines) up to first blank line
    body_start = 0
    for i, ln in enumerate(lines):
        if i == 0:
            continue
        if not ln.strip():
            continue
        if set(ln.strip()) <= {"=", "-", "_"}:
            continue
        if ln.strip().startswith("["):
            continue
        body_start = i
        break
    desc_lines: list[str] = []
    for ln in lines[body_start:]:
        if not ln.strip():
            if desc_lines:
                break
            else:
                continue
        desc_lines.append(ln.strip())
    info.description = " ".join(desc_lines).strip()

    # Brief = first sentence (truncated to ~140 chars)
    sentence_split = re.split(r"(?<=[.])\s+", info.description, maxsplit=1)
    brief = sentence_split[0] if sentence_split else info.description
    if len(brief) > 140:
        brief = brief[:137].rstrip() + "..."
    info.brief = brief

    return info


# ──────────────────────────────────────────────────────────────────────
# Output generation
# ──────────────────────────────────────────────────────────────────────


def make_link(script: ScriptInfo, from_path: Path) -> str:
    """Relative link from `from_path` to scripts/<filename>."""
    rel = os.path.relpath(SCRIPTS_DIR / script.filename, start=from_path.parent)
    return rel.replace(os.sep, "/")


def fmt_inventory_row(idx: int, s: ScriptInfo) -> str:
    return (
        f"| {idx} | [`{s.filename}`](scripts/{s.filename}) | "
        f"{s.law_label} | {s.dot_label} | {s.tier_label} | {s.brief} |"
    )


def write_inventory(scripts: list[ScriptInfo]) -> None:
    # Sort by law_id ASC, then by filename
    sorted_by_law = sorted(
        scripts,
        key=lambda s: ((s.law_id is None, s.law_id or 0, s.filename.lower())),
    )

    lines: list[str] = []
    lines.append("# Inventory — all SPT SymPy verification scripts")
    lines.append("")
    lines.append(
        f"Auto-generated by `.github/scripts/build_inventory.py`. "
        f"**{len(scripts)} scripts** total. "
        f"Sort by clicking any column header on GitHub."
    )
    lines.append("")
    lines.append("## Sorted by Law ID")
    lines.append("")
    lines.append("| # | Script | Law | Đợt | Tier | Brief |")
    lines.append("|---|---|---|---|---|---|")
    for i, s in enumerate(sorted_by_law, 1):
        lines.append(fmt_inventory_row(i, s))
    lines.append("")

    # Counts by tier
    by_tier: dict[str, int] = {}
    for s in scripts:
        by_tier[s.tier_label] = by_tier.get(s.tier_label, 0) + 1
    lines.append("## Counts by Tier")
    lines.append("")
    lines.append("| Tier | Count |")
    lines.append("|---|---|")
    for t in sorted(by_tier.keys()):
        lines.append(f"| {t} | {by_tier[t]} |")
    lines.append("")

    # Counts by Đợt
    by_dot: dict[str, int] = {}
    for s in scripts:
        by_dot[s.dot_label] = by_dot.get(s.dot_label, 0) + 1
    lines.append("## Counts by Đợt")
    lines.append("")
    lines.append("| Đợt | Count |")
    lines.append("|---|---|")
    for d in sorted(by_dot.keys(), key=_dot_sort_key):
        lines.append(f"| {d} | {by_dot[d]} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "Run `bash verify_all.sh` to re-verify every script. "
        "Run `python3 .github/scripts/build_inventory.py` to regenerate this file."
    )
    lines.append("")
    INVENTORY_PATH.write_text("\n".join(lines), encoding="utf-8")


def _dot_sort_key(label: str) -> tuple:
    if label == "Foundation":
        return (0, 0)
    m = re.search(r"\d+", label)
    return (1, int(m.group(0)) if m else 0)


def write_by_batch(scripts: list[ScriptInfo]) -> None:
    BY_BATCH_DIR.mkdir(parents=True, exist_ok=True)
    # Group by dot
    groups: dict[str, list[ScriptInfo]] = {}
    for s in scripts:
        groups.setdefault(s.dot_label, []).append(s)

    # Index README
    idx_lines = ["# Browse by Đợt (chronological closure batches)", ""]
    idx_lines.append("Each Đợt is a coherent batch of SPT closures shipped together.")
    idx_lines.append("")
    for d in sorted(groups.keys(), key=_dot_sort_key):
        n = len(groups[d])
        slug = _dot_slug(d)
        idx_lines.append(f"- [{d}](./{slug}.md) — {n} script{'s' if n != 1 else ''}")
    idx_lines.append("")
    (BY_BATCH_DIR / "README.md").write_text("\n".join(idx_lines), encoding="utf-8")

    # Per-dot pages
    for d, items in groups.items():
        slug = _dot_slug(d)
        items_sorted = sorted(items, key=lambda s: (s.law_id or 9999, s.filename))
        page = [f"# {d}", ""]
        if items_sorted and items_sorted[0].version:
            v = items_sorted[0].version
            dt = items_sorted[0].date
            page.append(f"_{v} · {dt} GMT+7_")
            page.append("")
        page.append(f"{len(items_sorted)} script{'s' if len(items_sorted) != 1 else ''} in this batch.")
        page.append("")
        page.append("| Law | Script | Tier | Brief |")
        page.append("|---|---|---|---|")
        for s in items_sorted:
            page.append(
                f"| {s.law_label} | [`{s.filename}`](../../scripts/{s.filename}) | "
                f"{s.tier_label} | {s.brief} |"
            )
        page.append("")
        page.append("[← all batches](README.md) · [main README](../../README.md)")
        page.append("")
        (BY_BATCH_DIR / f"{slug}.md").write_text("\n".join(page), encoding="utf-8")


def _dot_slug(label: str) -> str:
    if label == "Foundation":
        return "00-foundation"
    m = re.search(r"\d+", label)
    if not m:
        return label.lower().replace(" ", "-")
    return f"dot-{int(m.group(0)):02d}"


def write_by_law(scripts: list[ScriptInfo]) -> None:
    BY_LAW_DIR.mkdir(parents=True, exist_ok=True)
    # Group by law_id (may have multiple scripts per Law)
    groups: dict[Optional[int], list[ScriptInfo]] = {}
    for s in scripts:
        groups.setdefault(s.law_id, []).append(s)

    # Index README
    idx_lines = ["# Browse by Law ID (1 → N)", ""]
    idx_lines.append(
        "Each numbered SPT Law has its own page. Foundation laws (no `law_id` in "
        "the docstring) are grouped under `unassigned.md`."
    )
    idx_lines.append("")
    for k in sorted(groups.keys(), key=lambda x: (x is None, x or 0)):
        n = len(groups[k])
        if k is None:
            label = "Unassigned / supporting"
            slug = "unassigned"
        else:
            label = f"Law {k}"
            slug = f"law-{k:02d}"
        idx_lines.append(f"- [{label}](./{slug}.md) — {n} script{'s' if n != 1 else ''}")
    idx_lines.append("")
    (BY_LAW_DIR / "README.md").write_text("\n".join(idx_lines), encoding="utf-8")

    # Per-law pages
    for k, items in groups.items():
        if k is None:
            slug = "unassigned"
            title = "Unassigned / supporting scripts"
        else:
            slug = f"law-{k:02d}"
            title = f"Law {k}"
        items_sorted = sorted(items, key=lambda s: s.filename)
        page = [f"# {title}", ""]
        page.append(f"{len(items_sorted)} script{'s' if len(items_sorted) != 1 else ''} verify this Law.")
        page.append("")
        for s in items_sorted:
            page.append(f"## `{s.filename}`")
            if s.title:
                page.append("")
                page.append(f"_{s.title}_")
            page.append("")
            meta_bits = []
            if s.dot_label:
                meta_bits.append(s.dot_label)
            if s.version:
                meta_bits.append(s.version)
            if s.date:
                meta_bits.append(s.date)
            if s.tier_label:
                meta_bits.append(f"Tier {s.tier_label}")
            if meta_bits:
                page.append(" · ".join(meta_bits))
                page.append("")
            if s.description:
                page.append(s.description)
                page.append("")
            page.append(
                f"**Run**: `python3 scripts/{s.filename}` · "
                f"**Source**: [`scripts/{s.filename}`](../../scripts/{s.filename})"
            )
            page.append("")
        page.append("[← all laws](README.md) · [main README](../../README.md)")
        page.append("")
        (BY_LAW_DIR / f"{slug}.md").write_text("\n".join(page), encoding="utf-8")


def write_docs_index() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    content = """# Documentation

Three ways to browse the SymPy verification scripts:

1. **[By Đợt](by-batch/)** — chronological closure batches (Foundation, Đợt 1, Đợt 2, ...)
2. **[By Law](by-law/)** — by Law ID (1 → 52)
3. **[Inventory](../INVENTORY.md)** — complete table of all scripts (sort by clicking columns)

Each script's docstring contains the full proof structure; the markdown pages here
are navigation aids that point you to the right `.py` file.

For full Law derivations (8-section wiki: verify → SymPy → precision → detailed
mechanism → comparison → importance → falsifier → conclusion), see the SPT
webapp.
"""
    (DOCS_DIR / "README.md").write_text(content, encoding="utf-8")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────


def main() -> int:
    if not SCRIPTS_DIR.exists():
        print(f"[build_inventory] scripts/ directory not found at {SCRIPTS_DIR}", file=sys.stderr)
        return 1

    py_files = sorted(SCRIPTS_DIR.glob("spt_*.py"))
    if not py_files:
        print(f"[build_inventory] no spt_*.py files in {SCRIPTS_DIR}", file=sys.stderr)
        return 1

    scripts: list[ScriptInfo] = [parse_script(p) for p in py_files]

    write_inventory(scripts)
    write_by_batch(scripts)
    write_by_law(scripts)
    write_docs_index()

    print(f"[build_inventory] wrote INVENTORY.md ({len(scripts)} scripts)")
    print(f"[build_inventory] wrote docs/by-batch/*.md")
    print(f"[build_inventory] wrote docs/by-law/*.md")
    print(f"[build_inventory] wrote docs/README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
