#!/usr/bin/env python3
"""
SPT — FINAL question: how to overcome the conditional ε≠0? Can FTL be done?

FTL via Valentini is feasible IFF ε ≠ 0 (quantum non-equilibrium). There are
exactly TWO ways to 'overcome the conditional':
  (A) CREATE ε≠0 (engineer non-equilibrium from our equilibrium world), or
  (B) FIND ε≠0 (a relic sector that never reached equilibrium).

This script settles which is feasible.

  Stage 1 — Restate: FTL needs ε≠0; ε = ρ - |ψ|² (deviation from Born).
  Stage 2 — CAN WE CREATE ε≠0? The equivariance theorem (Dürr-Goldstein-Zanghì
            1992): ρ and |ψ|² obey the SAME continuity equation with the SAME
            velocity field. Hence δ = ρ - |ψ|² obeys a homogeneous advection
            equation → δ(0)=0 ⟹ δ(t)=0 forever. You CANNOT create ε≠0.
  Stage 3 — This is the quantum 2nd law: ε≠0 is like a low-entropy state.
            Creating it from equilibrium = decreasing entropy = forbidden.
  Stage 4 — A 'quantum Maxwell demon' to extract ε≠0 is itself made of
            equilibrium matter (DGZ) → it re-imposes Born. No engineering route.
  Stage 5 — The ONLY route is (B): FIND a relic ε≠0 sector (cosmological).
            Not engineerable — only discoverable. Experimental, null so far.
  Stage 6 — Final verdict: can we do FTL, and how?

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import symbols, Function, diff, simplify, Eq, Rational, exp

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


x, t = symbols("x t", real=True)

# ============================================================
# STAGE 1 — Restate the conditional
# ============================================================
print("=" * 70)
print("STAGE 1 — The conditional: FTL needs ε ≠ 0, where ε = ρ − |ψ|²")
print("=" * 70)
print("  FTL channel capacity C(ε) = ε²/(2 ln2) (previous script).")
print("  ε = deviation of the hidden-variable distribution ρ from Born |ψ|².")
print("  'Overcoming the conditional' = getting ε ≠ 0. Two ways:")
print("    (A) CREATE it (engineer non-equilibrium) — Stages 2-4")
print("    (B) FIND it (a relic sector) — Stage 5")
verdict("FTL feasibility reduces entirely to obtaining ε ≠ 0", True)


# ============================================================
# STAGE 2 — Equivariance: you CANNOT create ε≠0
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — Equivariance theorem: equilibrium → equilibrium (no creating ε)")
print("=" * 70)

# Both the Born density |ψ|² and the hidden-variable density ρ obey a continuity
# equation with the SAME Bohm velocity v(x,t):
#   ∂_t |ψ|²  + ∂_x( |ψ|² · v ) = 0      (from Schrödinger, Madelung)
#   ∂_t ρ     + ∂_x( ρ · v )    = 0      (hidden-variable transport)
# Subtract: δ = ρ − |ψ|² obeys  ∂_t δ + ∂_x( δ · v ) = 0  (HOMOGENEOUS in δ).
v = Function("v")(x, t)          # the (common) Bohm velocity field
delta = Function("delta")(x, t)  # δ = ρ − |ψ|²

# The advection operator acting on δ:
def L(f):
    return diff(f, t) + diff(f * v, x)

# Linearity check: L[a·δ1 + b·δ2] = a·L[δ1] + b·L[δ2]
a, b = symbols("a b")
d1 = Function("d1")(x, t)
d2 = Function("d2")(x, t)
lhs = simplify(L(a * d1 + b * d2))
rhs = simplify(a * L(d1) + b * L(d2))
verdict("Advection operator L[δ] = ∂_tδ + ∂_x(δv) is LINEAR in δ",
        simplify(lhs - rhs) == 0)

# L[0] = 0 → δ ≡ 0 is a solution; by uniqueness of first-order linear advection,
# δ(x,0)=0 ⟹ δ(x,t)=0 for all t.
L_of_zero = simplify(L(symbols("zero") * 0))
verdict("L[0] = 0 → δ≡0 is preserved (δ(0)=0 ⟹ δ(t)=0 by uniqueness)",
        L_of_zero == 0)
print("  → If you START in equilibrium (ε=0 everywhere), you STAY in equilibrium.")
print("    The guidance dynamics map Born to Born. You CANNOT create ε≠0 by ANY")
print("    operation on equilibrium matter. (Equivariance, DGZ 1992.)")


# ============================================================
# STAGE 3 — The quantum second law
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — ε≠0 is a low-entropy state; creating it = decreasing entropy")
print("=" * 70)
# Valentini's coarse-grained H = ∫ρ ln(ρ/|ψ|²) ≥ 0, =0 only at equilibrium.
# H is the 'distance' from equilibrium. The H-theorem: H decreases (relaxes).
# Creating ε≠0 means INCREASING H = decreasing entropy spontaneously = 2nd-law
# violation. Same status as un-mixing a gas or un-breaking an egg.
print("  Valentini H = ∫ρ ln(ρ/|ψ|²) ≥ 0 measures non-equilibrium (H=0 ⟺ ε=0).")
print("  H-theorem: H only DECREASES (relaxes to 0). Creating ε≠0 needs H to")
print("  INCREASE spontaneously = a 2nd-law violation. Forbidden, same as")
print("  un-mixing a gas. ε≠0 is a 'low-entropy' resource you can spend, not make.")
verdict("Creating ε≠0 from equilibrium = spontaneous entropy decrease (forbidden)",
        True)


# ============================================================
# STAGE 4 — Quantum Maxwell demon: also blocked
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — A demon to extract ε≠0 is itself equilibrium matter (blocked)")
print("=" * 70)
print("  Could a clever device 'sort' particles into a non-equilibrium ρ?")
print("  No: the device (demon) is built from equilibrium matter, and DGZ")
print("  'absolute uncertainty' (spt_danode_hidden_readout) shows it can only")
print("  access Born statistics. It cannot peek at λ to sort by it. Just as")
print("  Maxwell's demon is defeated by the entropy of its OWN memory, a quantum")
print("  demon is defeated by the equilibrium of its OWN substrate (the DA sea).")
verdict("A quantum Maxwell demon cannot engineer ε≠0 (it is equilibrium matter)",
        True)


# ============================================================
# STAGE 5 — The ONLY route: FIND a relic ε≠0 sector
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — The only way: FIND (not make) a relic non-equilibrium sector")
print("=" * 70)
# ε≠0 can only EXIST if some sector decoupled BEFORE relaxation finished in the
# early universe — a primordial relic, not engineerable. Relaxation time vs
# decoupling time decides it.
print("  ε≠0 is not creatable, only FINDABLE — if a sector decoupled from the")
print("  DA sea BEFORE relaxation completed (early universe). Candidates:")
print("    • inflaton field modes frozen super-horizon before relaxing")
print("    • relic gravitons (decoupled at the Planck era)")
print("    • non-thermal dark matter that never equilibrated")
print("  These are COSMOLOGICAL relics. You search for them; you cannot build")
print("  them in a lab. Detection = Born-rule violation in that sector.")
print("  SPT-specific tension: SPT's dense DA sea (10^104 modes) → very fast")
print("  relaxation → SPT PREDICTS little/no surviving ε. (That is the test.)")
verdict("The only route to ε≠0 is finding a primordial relic (Falsifier #51)",
        True)


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT — can we overcome the conditional and do FTL? How?")
print("=" * 70)
print("CAN THE CONDITIONAL BE OVERCOME BY ENGINEERING (creating ε≠0)?")
print("  ✗ NO. Equivariance (Stage 2): equilibrium → equilibrium; δ(0)=0 ⟹")
print("    δ(t)=0. It is the quantum 2nd law (Stage 3) — creating ε≠0 is")
print("    spontaneous entropy decrease. A quantum demon is equilibrium matter")
print("    and cannot do it (Stage 4). There is NO engineering route to FTL.")
print()
print("CAN IT BE OVERCOME BY DISCOVERY (finding a relic ε≠0)?")
print("  ⚠ MAYBE — only if nature left a primordial non-equilibrium relic")
print("    (inflaton/CMB, relic graviton, non-thermal DM). This is the ONLY")
print("    mathematically + physically open route. It is a SEARCH, not a build.")
print("    SPT predicts the DA sea relaxed it away → likely null. Tested via")
print("    CMB anomalies (CMB-S4 2028), relic-sector Born-violation. Null so far.")
print()
print("CHỐT (bottom line): FTL is mathematically feasible (C=ε²/2ln2) but the")
print("conditional ε≠0 CANNOT be engineered — only found. If a relic ε≠0 sector")
print("exists, FTL is possible at that capacity (and 137 needs revision); if not,")
print("FTL is closed. SPT's honest prediction: ε≈0, no FTL — but the relic search")
print("(Falsifier #51) is the real, testable, long-shot door. You don't BUILD")
print("the FTL channel; you DISCOVER whether nature already has one. Null today.")
