#!/usr/bin/env python3
"""
SPT — Valentini quantum non-equilibrium: WHAT it is, and a rigorous calculation
of whether FTL is mathematically feasible along this path.

VALENTINI NON-EQUILIBRIUM (de Broglie-Bohm pilot wave, Valentini 1991-2007):
  • In pilot-wave theory, particles have definite hidden positions λ, guided by
    ψ via dx/dt = (ℏ/m)·Im(∇ψ/ψ).
  • 'Quantum equilibrium' = hidden-variable distribution ρ(λ) = |ψ(λ)|² (Born).
  • Valentini's theorem: ρ = |ψ|² ⟹ standard QM (no-signalling, uncertainty).
    ρ ≠ |ψ|² ('non-equilibrium') ⟹ NEW physics: SIGNALLING (FTL), sub-quantum
    measurement, distinguishing non-orthogonal states.
  • H-theorem (Valentini 1991): coarse-grained H = ∫ρ ln(ρ/|ψ|²) decreases →
    ρ relaxes to |ψ|² (equilibrium is an attractor). Relic particles that
    decoupled before relaxation MIGHT retain non-equilibrium.

This script CALCULATES the FTL channel capacity as a function of the
non-equilibrium deviation ε, and the relaxation that suppresses it.

  Stage 1 — Equilibrium (ε=0): Bob's marginal independent of Alice (no signal).
  Stage 2 — Non-equilibrium (ε≠0): Bob's P(0) DEPENDS on Alice's setting,
            with signal strength ∝ ε. FTL door opens.
  Stage 3 — FTL channel capacity C(ε) = ε²/(2 ln2) bits/use (rigorous, small ε).
            → FTL IS mathematically feasible CONDITIONAL on ε ≠ 0.
  Stage 4 — H-theorem relaxation: ε(t) = ε₀·exp(-t/τ) → 0. SPT DA sea
            (10^104 modes) → τ Planck-fast → ε→0 ~instantly.
  Stage 5 — Experimental bounds + relic scenarios + honest verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
import math
from sympy import (
    symbols, Rational, simplify, log, series, limit, oo, exp, sqrt,
    diff, cos, sin, Abs, nsimplify, pi,
)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


def H2(x):
    """Binary entropy in bits: H2(x) = -x log2(x) - (1-x) log2(1-x)."""
    return -x * log(x) / log(2) - (1 - x) * log(1 - x) / log(2)


# ============================================================
# STAGE 1 — Equilibrium (ε=0): no signal
# ============================================================
print("=" * 70)
print("STAGE 1 — Quantum equilibrium ρ = |ψ|² (ε=0): Bob independent of Alice")
print("=" * 70)
eps = symbols("epsilon", real=True, nonnegative=True)
theta = symbols("theta", real=True)
# Bob's P(0|Alice setting θ) in (non-)equilibrium. Model: the non-equilibrium
# bias couples to Alice's basis as ε·sin²θ on top of the Born 1/2.
P_bob = Rational(1, 2) + eps * sin(theta)**2
P_bob_eq = P_bob.subs(eps, 0)
print(f"  Bob's P(0|θ) = 1/2 + ε·sin²θ")
print(f"  At equilibrium ε=0: P(0|θ) = {P_bob_eq} (independent of Alice's θ)")
verdict("ε=0: Bob's marginal = 1/2 for all Alice settings (no signal, standard QM)",
        P_bob_eq == Rational(1, 2))


# ============================================================
# STAGE 2 — Non-equilibrium (ε≠0): signal appears
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — Non-equilibrium ε≠0: Bob's stats depend on Alice → signal")
print("=" * 70)
# Alice encodes a bit: θ=0 (P=1/2) vs θ=π/2 (P=1/2+ε). Distinguishability:
P_msg0 = simplify(P_bob.subs(theta, 0))           # = 1/2
P_msg1 = simplify(P_bob.subs(theta, pi/2))        # = 1/2 + ε (exact)
signal = simplify(P_msg1 - P_msg0)
print(f"  Alice θ=0   → Bob P(0) = {P_msg0}")
print(f"  Alice θ=π/2 → Bob P(0) = {P_msg1}")
print(f"  Signal (distinguishability) ΔP = {signal}")
verdict("ε≠0: Bob's P(0) shifts by ε between Alice's two messages → FTL signal",
        signal == eps)


# ============================================================
# STAGE 3 — FTL channel capacity C(ε) = ε²/(2 ln2)
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — FTL channel capacity (rigorous): C(ε) ≈ ε²/(2 ln 2) bits/use")
print("=" * 70)
# Binary channel: input bit (Alice θ), output Bob's measurement. With uniform
# input prior, mutual information I = H2(P_out) - avg H2(conditional).
P_out = Rational(1, 2) * P_msg0 + Rational(1, 2) * P_msg1   # = 1/2 + ε/2
I = H2(P_out) - (Rational(1, 2) * H2(P_msg0) + Rational(1, 2) * H2(P_msg1))
# Small-ε expansion:
I_series = series(I, eps, 0, 3).removeO()
I_series = simplify(I_series)
print(f"  Mutual information I(ε) (small-ε expansion) = {I_series}")
# Expected leading term: ε²/(2 ln2)
expected = eps**2 / (2 * log(2))
verdict("Channel capacity I(ε) = ε²/(2 ln2) bits per use (leading order)",
        simplify(I_series - expected) == 0)

# Numerical: bit-rate for sample ε at a measurement rate R
print("  Numerical FTL capacity (bits per measurement use):")
for eps_val in [1e-1, 1e-2, 1e-6, 1e-20]:
    cap = eps_val**2 / (2 * math.log(2))
    print(f"    ε = {eps_val:.0e}  →  C = {cap:.2e} bits/use")
print("  → FTL IS mathematically feasible CONDITIONAL on ε ≠ 0, capacity ∝ ε².")
print("    The whole question collapses to: is ε ≠ 0 anywhere in nature?")


# ============================================================
# STAGE 4 — H-theorem relaxation: ε → 0
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — Valentini H-theorem: ε relaxes to 0 (equilibrium attractor)")
print("=" * 70)
# Coarse-grained H decreases → ρ → |ψ|². Model ε(t) = ε₀ exp(-t/τ).
t, tau, eps0 = symbols("t tau epsilon_0", positive=True)
eps_t = eps0 * exp(-t / tau)
eps_inf = limit(eps_t, t, oo)
verdict("ε(t) = ε₀·exp(-t/τ) → 0 as t→∞ (H-theorem relaxation to Born)",
        eps_inf == 0)
print(f"  SPT-specific: relaxation rate set by DA-sea coarse-graining,")
print(f"  N ~ 10^104 modes (Law 41) → τ ~ Planck-fast → ε→0 almost instantly.")
print(f"  → SPT predicts ε ≈ 0 today (equilibrium). FTL capacity ≈ 0.")
print(f"  → Only relic sectors that DECOUPLED before relaxation could keep ε≠0.")


# ============================================================
# STAGE 5 — Bounds, relic scenarios, honest verdict
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — Experimental bounds + relic scenarios")
print("=" * 70)
print("  Current bounds on ε (Born-rule violation):")
print("    • Triple-slit additivity (Sinha et al. 2010): κ < 10^-2 → ε ≲ 10^-2")
print("    • Atomic / nuclear spectroscopy: Born holds to ~10^-9")
print("    • Loophole-free Bell no-signalling (2015-22): consistent with ε=0")
print("  Relic non-equilibrium candidates (Valentini 2007, Underwood-Valentini):")
print("    • Inflaton perturbations that froze before relaxation → CMB anomalies")
print("    • Relic gravitons / relic neutrinos decoupled at t < τ_relax")
print("    • Some dark-matter that never thermalised with the DA sea")
print("  FTL capacity if ε ~ 10^-2 (max allowed): C ~ 7×10^-5 bits/use →")
print("  at GHz rate ~ 10^5 bits/s FTL — but only IF such an ε-sector exists.")
print("  Status: NULL. No non-equilibrium detected. SPT predicts none survives.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT — is FTL mathematically feasible via Valentini?")
print("=" * 70)
print("MATHEMATICALLY: YES, conditional. If a sector has ε ≠ 0 (non-equilibrium,")
print("ρ ≠ |ψ|²), then FTL signalling is feasible with channel capacity")
print("C(ε) = ε²/(2 ln2) bits per use. This is rigorous (Stage 3, verified).")
print()
print("PHYSICALLY: the door is gated by ONE question — does ε ≠ 0 exist in")
print("nature? Three findings:")
print("  • H-theorem drives ε → 0 (equilibrium attractor).")
print("  • SPT's 10^104-mode DA sea makes relaxation Planck-fast → ε≈0 today.")
print("  • All experiments null; ε ≲ 10^-2 (loose) to ε ≲ 10^-9 (spectroscopy).")
print()
print("THE HONEST FRONTIER: hunt for a relic ε≠0 sector (inflaton/CMB, relic")
print("neutrino, non-thermal dark matter). IF found → FTL becomes feasible at")
print("capacity ε²/(2ln2), AND SPT's Born-based 137 derivation needs revision.")
print("This is SPT Falsifier #51 — a precise, testable, publishable prediction.")
print("It is the ONLY mathematically genuine FTL route, and it is decided by")
print("experiment, not by argument. Null so far. The calculation is honest:")
print("FTL ∝ ε², and finding ε≠0 is the real (long-shot) discovery to chase.")
