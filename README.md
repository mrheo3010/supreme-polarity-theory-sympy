# SPT SymPy Verification Scripts

> Reproducibility artefacts for the **Supreme Polarity Theory** (Thuyết Thái Cực Vạn Vật) framework.
> Every script verifies one SPT Law / closure from first principles using only **SymPy** and the
> Python standard library — zero free parameters, zero external data, < 2 s per script.

![Verify](../../actions/workflows/verify-all.yml/badge.svg)

## Quick start

```bash
git clone https://github.com/REPLACE-WITH-YOUR-USERNAME/supreme-polarity-theory-sympy.git
cd supreme-polarity-theory-sympy
pip install -r requirements.txt
bash verify_all.sh
```

Total verification: ~90 s on a laptop. Each script prints a step-by-step
derivation ending with a `verdict()` and exits 0 on PASS.

## Run one script

```bash
python3 scripts/spt_inflation.py
python3 scripts/spt_wave_particle_duality.py
python3 scripts/spt_alpha_em.py
# ... etc.
```

## What's inside

| Folder | Contents |
|---|---|
| **`scripts/`** | Every `.py` verification script, flat, alphabetical |
| **`INVENTORY.md`** | Complete table sortable by Law / Đợt / Tier (auto-regenerated) |
| **`docs/by-batch/`** | Browse by **Đợt** (chronological closure batches) |
| **`docs/by-law/`** | Browse by **Law ID** (1 → 52) |
| **`verify_all.sh`** | One-command full verification |
| **`requirements.txt`** | Just `sympy>=1.12` |
| **`CITATION.cff`** | Academic citation metadata (renders "Cite this repository" button) |

## How to read a script

Every `spt_*.py` file has the same shape:

1. **Docstring header** — Law number, Đợt, Tier classification, and the question being closed
2. **N stages** (typically 5-6), each ending with `assert` statements that verify the algebraic / numerical claim
3. **Final verdict** — summary table + cross-reference to wiki

The proof is the source code itself. If `python3 spt_<name>.py` exits 0, the
Law's verification chain is sound. If it ever fails, the corresponding Law
must be revised or withdrawn.

## Headline highlights — start here

| Script | Law | What it verifies |
|---|---|---|
| [`spt_breakthrough_check.py`](scripts/spt_breakthrough_check.py) | Foundation | `d₀ = √7/4` from `λ₂ = 16/7` on weighted Q₆ Laplacian — the cascade-slope anchor |
| [`spt_alpha_em.py`](scripts/spt_alpha_em.py) | 5 | `1/α_em = Q₇ + Q₃ + 1 = 137` — closes Sommerfeld's 100-year "magic 137" mystery |
| [`spt_unified_force_mechanism.py`](scripts/spt_unified_force_mechanism.py) | 42 | All 4 fundamental forces unified via DANode rotation |
| [`spt_wave_particle_duality.py`](scripts/spt_wave_particle_duality.py) | 44 | 99-year Davisson-Germer mystery dissolved (Q₃ ⊂ Q₇ regime switch) |
| [`spt_bell_chsh.py`](scripts/spt_entanglement_chsh.py) | 46 | Tsirelson bound `|S| ≤ 2√2` saturated from SU(2) yao-spin algebra |
| [`spt_inflation.py`](scripts/spt_inflation.py) | 50 | Cosmic inflation from SPT Action's OWN V(φ), zero new fields |
| [`spt_bigbang_bounce.py`](scripts/spt_bigbang_bounce.py) | 52 | Big Bang singularity replaced by Planck-density bounce |

See [`INVENTORY.md`](INVENTORY.md) for the complete table of all scripts.

## Wiki / full derivations

Each Law has a dedicated wiki page on the SPT website following an 8-section
template (verify → SymPy → precision → detailed mechanism → comparison → importance
→ falsifier → conclusion). Each script's docstring header links back to its wiki.

## How this repository is maintained

This repository is **auto-synced** from the SPT webapp's `scripts/` directory via
a GitHub Actions workflow. **Do not commit directly here** — the next sync would
overwrite manual edits. To report verification failures or propose changes,
open an issue.

Sync commits look like:

```
sync: mirror scripts/ from webapp@<sha>

Source commit: <link>
Triggered by: <author>
```

`INVENTORY.md` and the `docs/by-batch/` + `docs/by-law/` indexes are also
auto-regenerated on each sync from the script docstrings.

## License

No formal license file is included; the work is presented as-is for academic
reproducibility audit. Verify, fork, port, cite freely — please credit the
SPT framework and the author when reproducing or extending.

## Citation

See [`CITATION.cff`](CITATION.cff) or click the "Cite this repository" button
on the top-right of the GitHub repo page.
