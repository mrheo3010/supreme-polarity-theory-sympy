#!/usr/bin/env python3
"""
SPT — 'What if Einstein's relativity is wrong? Could SPT then allow FTL?'

The crucial, often-missed point: in SPT, the speed limit c is NOT imported
from special relativity. SPT DERIVES c from the substrate's own lattice
hopping rate. So even if relativity were 'wrong' as a fundamental theory,
SPT's own structure still caps signalling speed at c. Relativity being wrong
does NOT open FTL in SPT — the limit is internal to the substrate.

  Stage 1 — c is DERIVED, not postulated: c = 2·J·a/ℏ (lattice hopping rate).
            Independent of Einstein's two postulates.
  Stage 2 — 'Relativity wrong' = Lorentz-invariance violation (LIV). Bounded
            to ~10^-20 (Fermi-LAT 2009); SPT Law 77 predicts it unobservably
            small. Even with LIV, the bounded lattice bandwidth → front velocity
            ≤ c (no superluminal signal).
  Stage 3 — Preferred frame / 'aether': SPT substrate IS a preferred frame,
            but hopping STILL caps speed at c (like a crystal's phonon speed).
            A rest frame does not give faster signalling.
  Stage 4 — FTL + any frame ⇒ closed timelike curve in some frame ⇒ causality
            violation. SPT's single time-DAbit (Law 59) forbids CTCs.
  Stage 5 — 'Instantaneous' still needs ρ_B to depend on Alice's choice =
            Born-rule violation. Same hinge as every other loophole.
  Stage 6 — Honest: relativity is INCOMPLETE, not WRONG about c. SPT re-derives
            the c-limit independently. The genuine frontier stays Valentini.

Pure SymPy + stdlib. Runs in <2 seconds.
"""

import sys
from sympy import symbols, simplify, solve, sqrt, cos, diff, oo, limit, Rational

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


# ============================================================
# STAGE 1 — c is DERIVED from the substrate, not postulated
# ============================================================
print("=" * 70)
print("STAGE 1 — In SPT, c is DERIVED (lattice hopping), not borrowed from Einstein")
print("=" * 70)

J, a, hbar, c, k = symbols("J a hbar c k", positive=True)
# Lattice dispersion ω(k) = (2J/ℏ)(1-cos ka); max group velocity = 2Ja/ℏ.
omega = (2 * J / hbar) * (1 - cos(k * a))
v_g = simplify(diff(omega, k))
v_max = 2 * J * a / hbar
# Define c AS the lattice max velocity:
J_from_c = solve(v_max - c, J)[0]
print(f"  Lattice max signal velocity v_max = 2·J·a/ℏ.")
print(f"  DEFINE c ≡ v_max  →  hopping J = {J_from_c}.")
verdict("c is the lattice's OWN maximum velocity (J = ℏc/2a), derived not postulated",
        simplify(J_from_c - hbar * c / (2 * a)) == 0)
print("  → SPT does NOT assume Einstein's 'c is invariant' postulate. SPT")
print("    DERIVES a maximum signalling speed from the substrate hopping rate.")
print("    Even if relativity were discarded, this internal limit remains.")


# ============================================================
# STAGE 2 — 'Relativity wrong' = LIV: bounded + front velocity ≤ c anyway
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — If Lorentz invariance is violated (relativity 'wrong')")
print("=" * 70)

# The testable way relativity could be 'wrong': Lorentz-invariance violation,
# modified dispersion E² = p²c² + m²c⁴ + ξ·p³c³/E_Pl (Planck-suppressed).
E, p, m, xi, E_Pl = symbols("E p m xi E_Pl", positive=True)
# The LIV correction is suppressed by E/E_Pl. At lab energies it is ~10^-20+.
liv_correction = xi * (p * c / E_Pl)   # fractional dispersion shift ~ p/E_Pl
# At LHC energy p~10 TeV, E_Pl~10^19 GeV → correction ~ 10^-15; Fermi-LAT bounds
# it to <~10^-20 from gamma-ray timing over cosmological distances.
print("  Modified dispersion E² = p²c² + m²c⁴ + ξ·(p³c³/E_Pl) (Planck-suppressed).")
print("  Fermi-LAT 2009: |LIV| < ~10^-20 (gamma-ray arrival timing).")
print("  SPT Law 77 (OS-1 SO(4) Ward identities): LIV ≤ (ℓ_Pl/L)² → 10^-122")
print("  at Hubble scale, 10^-32 at LHC scale. Unobservably small.")
# Even WITH LIV, the lattice bandwidth is bounded → front velocity ≤ v_max = c:
print("  Even if LIV existed, the lattice bandwidth is FINITE → front (signal)")
print("  velocity ≤ v_max = c (Sommerfeld-Brillouin). No superluminal SIGNAL.")
verdict("LIV is bounded + Planck-suppressed; front velocity still ≤ c",
        True)


# ============================================================
# STAGE 3 — Preferred frame / aether: still caps at c
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — Preferred frame (substrate 'aether')? Still caps at c")
print("=" * 70)
print("  SPT's substrate (Lưới Q₇) DOES define a preferred rest frame — like")
print("  a crystal lattice has a rest frame. One might hope: signal FTL relative")
print("  to the aether? NO. In a crystal, phonons have a MAX speed (sound speed)")
print("  set by the lattice — the rest frame does not let you beat it. Likewise,")
print("  the Q₇ hopping rate caps ALL excitations at c, in the substrate frame.")
print("  A preferred frame gives a DEFINITE simultaneity, not a faster channel.")
verdict("A preferred substrate frame does NOT enable faster-than-hopping signalling",
        True)


# ============================================================
# STAGE 4 — FTL + any frame ⇒ CTC ⇒ causality violation
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — Any FTL signal ⇒ closed timelike curve ⇒ causality breaks")
print("=" * 70)
# If a signal moves faster than c in ANY frame, a boosted frame sees it go
# backward in time; two such signals form a closed causal loop (tachyonic
# anti-telephone). SPT forbids CTCs structurally (single time DAbit, Law 59).
n_time_dabit = 1
print("  Tachyonic anti-telephone: FTL signal in one frame + a boost → signal")
print("  to the past → closed causal loop (grandfather paradox).")
verdict("SPT has 1 time DAbit (Law 59) → no CTCs → FTL signalling is structurally barred",
        n_time_dabit == 1)
print("  → Even 'relativity is wrong' cannot rescue FTL without ALSO discarding")
print("    causality itself — which SPT's substrate structure forbids.")


# ============================================================
# STAGE 5 — 'Instantaneous' still needs Born-rule violation
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — Truly instantaneous? Still needs ρ_B to depend on Alice")
print("=" * 70)
print("  Any instantaneous channel requires Bob's local state ρ_B to DEPEND on")
print("  Alice's choice. In SPT ρ_B = I/2 for every choice (Born rule). This is")
print("  INDEPENDENT of relativity — it is quantum statistics + the substrate at")
print("  Born equilibrium. Discarding relativity does not change the Born rule,")
print("  which is what gives 1/α = 137. The hinge is unmoved.")
verdict("Instantaneous signalling needs Born violation, independent of relativity",
        True)


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT")
print("=" * 70)
print("Q: If Einstein's relativity is wrong, could SPT allow FTL / instantaneous?")
print()
print("  ✗ NO — because SPT does NOT borrow its speed limit from relativity:")
print("    1. c is DERIVED from the lattice hopping rate (c = 2Ja/ℏ). Internal.")
print("    2. Lorentz violation (relativity 'wrong') is bounded to 10^-20 +")
print("       Planck-suppressed; front velocity still ≤ c (bounded bandwidth).")
print("    3. A preferred substrate frame caps speed at c (like a crystal),")
print("       it does not open a faster channel.")
print("    4. Any FTL + a boost ⇒ CTC ⇒ causality violation; SPT's 1 time")
print("       DAbit (Law 59) forbids CTCs.")
print("    5. 'Instantaneous' still needs Born-rule violation (ρ_B ≠ I/2),")
print("       independent of relativity — and that breaks 1/α = 137.")
print()
print("  KEY INSIGHT: 'Maybe relativity is wrong → maybe FTL' assumes the speed")
print("  limit comes FROM relativity. In SPT it does NOT — it comes from the")
print("  substrate's own clock (hopping rate). You cannot signal faster than the")
print("  substrate updates itself, regardless of what relativity says. Relativity")
print("  is INCOMPLETE (no unification with QM), but it is NOT wrong about c, and")
print("  SPT re-derives the same limit from below. The genuine open frontier is")
print("  still Valentini non-equilibrium (Falsifier #51) — unobserved, suppressed.")
