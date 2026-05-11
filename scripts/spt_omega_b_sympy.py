"""SymPy feasibility test for Omega_b exact derivation.

Question: can Omega_b be brought to PASS via a closed-form expression
verified by SymPy, the way d0 = sqrt(7)/4 was?

Strategy:
  1. Verify the proposed closure identity Omega_b = 6/128 + alpha_em/3.
  2. Search for closed-form alpha_em candidates from Bagua structure
     (7, 8, 64, 128, pi, sqrt, log) - small-integer combinations only.
  3. Cross-validate: which (if any) candidate gives Omega_b matching
     Planck 0.0493 to <0.5% AND alpha_em matching CODATA to <0.1%?

Reports a verdict on whether SymPy alone can close Omega_b.
"""

from __future__ import annotations

import math
from typing import Iterable

import sympy as sp


# ---------------------------------------------------------------------------
# Anchor values
# ---------------------------------------------------------------------------

PLANCK_OMEGA_B = 0.0493
PLANCK_OMEGA_B_ERR = 0.0006
CODATA_ALPHA_EM = 1 / 137.035999084  # 2018 CODATA
CODATA_ALPHA_INV = 137.035999084
PI = sp.pi


# ---------------------------------------------------------------------------
# Step 1: trivial closure identity verification
# ---------------------------------------------------------------------------

def step1_closure_identity() -> None:
    """Plug alpha_em = CODATA into Omega_b = 6/128 + alpha_em/3."""
    print("=" * 72)
    print("STEP 1: closure identity Omega_b = 6/128 + alpha_em/3")
    print("=" * 72)
    alpha = sp.Rational(1, 137) + sp.Rational(0, 1)  # symbolic placeholder
    omega_b_pred = sp.Rational(6, 128) + sp.Rational(1, 137) / 3
    print(f"  Symbolic Omega_b = 6/128 + (1/137)/3 = {omega_b_pred}")
    print(f"  Numeric    = {float(omega_b_pred):.6f}")
    print(f"  Planck     = {PLANCK_OMEGA_B:.6f}  +/- {PLANCK_OMEGA_B_ERR:.6f}")
    delta = abs(float(omega_b_pred) - PLANCK_OMEGA_B) / PLANCK_OMEGA_B
    verdict = "PASS" if delta < 0.005 else "CLOSE"
    print(f"  Delta = {delta * 100:.3f} %  -> {verdict}")
    print()
    # Now using full CODATA alpha
    omega_b_codata = sp.Rational(6, 128) + sp.Rational(CODATA_ALPHA_EM) / 3
    print(f"  With CODATA alpha = 1/{CODATA_ALPHA_INV:.6f}:")
    print(f"  Omega_b = {float(omega_b_codata):.6f}")
    delta = abs(float(omega_b_codata) - PLANCK_OMEGA_B) / PLANCK_OMEGA_B
    verdict = "PASS" if delta < 0.005 else "CLOSE"
    print(f"  Delta = {delta * 100:.3f} %  -> {verdict}")
    print()


# ---------------------------------------------------------------------------
# Step 2: search for closed-form alpha_em from Bagua small integers
# ---------------------------------------------------------------------------

def candidate_expressions() -> Iterable[tuple[str, sp.Expr]]:
    """Generate plausible closed-form alpha_em^{-1} candidates from
    Bagua-related small integers (7, 8, 64, 128) and pi.

    Each yields (label, sympy expression for 1/alpha_em).
    """
    # Pure numerology - the 137 constant
    yield "137", sp.Integer(137)
    # 4*pi* combinations
    yield "4*pi*sqrt(120)", 4 * PI * sp.sqrt(120)
    yield "16*pi*sqrt(7)/sqrt(3)", 16 * PI * sp.sqrt(7) / sp.sqrt(3)
    # Bagua-cube-based
    yield "128 + 8 + 1 = 137", sp.Integer(128) + 8 + 1
    yield "(2^7 + 2^3 + 1) = 137", 2**7 + 2**3 + 1
    yield "Q7 + Q3 + 1", 128 + 8 + 1
    # pi-based identities popularised in numerology
    yield "(4*pi^3 + pi^2 + pi)", 4 * PI**3 + PI**2 + PI
    yield "(2*pi)^4 / (8 * pi)", (2 * PI)**4 / (8 * PI)
    # Wyler / Eddington style
    yield "9/(8*pi^4) * (pi^5 / 5!)^(1/4)  [Wyler]", \
        sp.Rational(9, 1) / (8 * PI**4) * (PI**5 / sp.factorial(5))**sp.Rational(1, 4)
    yield "Wyler corrected: 9/(8*pi^4)*(pi^5/120)^(1/4) inverted", \
        1 / (sp.Rational(9, 1) / (8 * PI**4) * (PI**5 / 120)**sp.Rational(1, 4))
    # 7/8 dilution-flavoured (echoing d0 = sqrt(7)/4)
    yield "16*pi*sqrt(7/8)*sqrt(7)", 16 * PI * sp.sqrt(sp.Rational(7, 8)) * sp.sqrt(7)
    yield "8 * 17 + 1 = 137", 8 * 17 + 1
    # Q7 cosmological-shell flavoured
    yield "C(7,3) + C(7,2) + C(7,1) + C(7,0) = 64", sp.Integer(64)


def step2_alpha_em_search() -> None:
    print("=" * 72)
    print("STEP 2: search for closed-form alpha_em^{-1} from Bagua integers")
    print("=" * 72)
    print(f"  CODATA: 1/alpha_em = {CODATA_ALPHA_INV:.9f}")
    print()
    print(f"  {'Candidate':<55} {'Numeric':>12} {'Delta %':>9}")
    print(f"  {'-' * 55} {'-' * 12} {'-' * 9}")
    best_label = None
    best_delta = 1.0
    for label, expr in candidate_expressions():
        try:
            num = float(expr.evalf(15))
        except Exception:  # noqa: BLE001
            num = math.nan
        delta = (
            abs(num - CODATA_ALPHA_INV) / CODATA_ALPHA_INV
            if not math.isnan(num) and num > 0
            else math.nan
        )
        flag = "***" if (not math.isnan(delta) and delta < 0.001) else ""
        print(f"  {label:<55} {num:>12.6f} {delta * 100:>8.3f}% {flag}")
        if not math.isnan(delta) and delta < best_delta:
            best_delta = delta
            best_label = label
    print()
    print(f"  Best candidate: {best_label} (Delta {best_delta * 100:.4f}%)")
    print()
    if best_delta < 0.001:
        print("  -> A clean closed-form alpha_em from Bagua integers MAY exist")
        print("     at 0.1% precision. Worth dedicated investigation.")
    elif best_delta < 0.01:
        print("  -> Several candidates are close (within 1%) but none ULTRA PASS.")
        print("     SPT Step 2 needs a Lagrangian-derived value, not numerology.")
    else:
        print("  -> No candidate from this small set hits 1% precision.")
        print("     Bagua small-integer numerology alone is INSUFFICIENT to fix")
        print("     alpha_em - SPT Step 2 (gauge group structure) needs to do")
        print("     real work: derive g, g', sin^2(theta_W), then RG-flow alpha_em.")
    print()


# ---------------------------------------------------------------------------
# Step 3: what would it take for SymPy alone to close Omega_b?
# ---------------------------------------------------------------------------

def step3_verdict() -> None:
    print("=" * 72)
    print("STEP 3: verdict on 'can SymPy alone close Omega_b'?")
    print("=" * 72)
    print("  YES (trivial part):")
    print("    SymPy can verify the IDENTITY Omega_b = 6/128 + alpha_em/3 in")
    print("    1 line if alpha_em is supplied as input. This is what")
    print("    scripts/spt_breakthrough_check.py does in section [Omega].")
    print()
    print("  NO (the hard part):")
    print("    SymPy CANNOT derive alpha_em itself from the SPT Action without")
    print("    a separate Step 2 mechanism (gauge-group structure -> coupling")
    print("    values g, g', sin^2(theta_W) -> alpha_em). Currently Step 2 has")
    print("    only the GENERATOR COUNT (8+3+1=12 ✓), not coupling values.")
    print()
    print("  Path forward (in order of tractability):")
    print("    1. Discrete Lie-algebra construction on the Bagua structure")
    print("       to derive g, g' as closed forms. (Hard but tractable.)")
    print("    2. SymPy script implementing 1-loop SM RG running of")
    print("       alpha_em(M_Planck) -> alpha_em(M_Z). (Routine; ~50 lines.)")
    print("    3. Combine 1+2 to predict CODATA alpha_em(M_e) at <0.1%.")
    print("    4. Plug into Omega_b = 6/128 + alpha_em/3 and watch it PASS.")
    print()
    print("  TL;DR: Omega_b PASS = 80% Step 2 + 20% SymPy plug-in.")
    print("         The bottleneck is NOT computational; it is conceptual.")
    print("         SymPy is ready when Step 2 is.")
    print()


if __name__ == "__main__":
    step1_closure_identity()
    step2_alpha_em_search()
    step3_verdict()
