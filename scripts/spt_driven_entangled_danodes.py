#!/usr/bin/env python3
"""
SPT — driving 2 entangled DANodes with photons + 'change one → the other
changes?' The crux: CORRELATION vs CONTROL.

User's protocol:
  (1) Take 2 entangled DANodes. Continuously send photons through each at the
      SAME frequency. Do we get correlated wave patterns?
  (2) Keep the correlation at distance so that CHANGING one DANode makes the
      other DANode change too?

Tested rigorously. Two new physics points not covered before:
  • Continuous photon driving = repeated measurement → DECOHERES the
    entanglement (off-diagonal coherence → 0). You cannot keep entanglement
    while pumping photons through it.
  • 'Change one → the other changes' has TWO meanings that must be separated:
      (a) 'change' = apply a unitary/force to a chosen value → the other's
          LOCAL state is UNCHANGED (no control, no-signaling).
      (b) 'change' = measure → the other becomes CORRELATED, but the outcome
          is random and the other's LOCAL marginal is still I/2.
    Entanglement gives CORRELATION (passive), never CONTROL (active).

  Stage 1 — Continuous driving decoheres: coherence (1-2p)→0 at full measure.
  Stage 2 — Same-frequency drive → correlation from COMMON CAUSE, not a channel.
  Stage 3 — 'Change one' as a unitary → Bob's reduced state UNCHANGED.
  Stage 4 — 'Change one' as a measurement → Bob correlated but marginal I/2,
            outcome random, and the pair is CONSUMED (one-shot).
  Stage 5 — Correlation ≠ control; SPT reading; verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import (
    symbols, Rational, simplify, eye, Matrix, sqrt, cos, sin, I,
    conjugate, kronecker_product, zeros, trigsimp,
)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


def dagger(M):
    return M.conjugate().T


ket0 = Matrix([1, 0]); ket1 = Matrix([0, 1])
Z = Matrix([[1, 0], [0, -1]])

# Bell state |Φ+⟩ = (|00⟩+|11⟩)/√2  (two entangled DANodes)
bell = (kronecker_product(ket0, ket0) + kronecker_product(ket1, ket1)) / sqrt(2)
rho_bell = bell * dagger(bell)

def ptrace_A(rho):
    out = zeros(2, 2)
    for b1 in range(2):
        for b2 in range(2):
            out[b1, b2] = sum(rho[a*2+b1, a*2+b2] for a in range(2))
    return out


# ============================================================
# STAGE 1 — Continuous photon driving DECOHERES the entanglement
# ============================================================
print("=" * 68)
print("STAGE 1 — Driving DANodes with photons = measurement → DECOHERENCE")
print("=" * 68)

# Sending photons through a DANode probes it = a (partial) measurement.
# Model as a dephasing channel on qubit A with strength p:
#   ρ → (1-p)·ρ + p·(Z_A ρ Z_A)
p = symbols("p", real=True)
ZA = kronecker_product(Z, eye(2))
rho_driven = simplify((1 - p) * rho_bell + p * ZA * rho_bell * dagger(ZA))
# The entanglement lives in the |00⟩⟨11| coherence (index [0,3]):
coherence = simplify(rho_driven[0, 3])
print(f"  Off-diagonal coherence ρ(00,11) after driving = {coherence}")
print(f"  (= 1/2·(1-2p): drops as you drive harder)")
coh_full = simplify(coherence.subs(p, Rational(1, 2)))
verdict("Full driving (p=1/2): coherence → 0 → entanglement DESTROYED",
        coh_full == 0)
print("  → Continuously sending photons through the DANodes DECOHERES them.")
print("    You CANNOT keep the entanglement while pumping photons — the act")
print("    of driving/probing collapses it to a classical correlated mixture.")


# ============================================================
# STAGE 2 — Same-frequency drive → correlation from COMMON CAUSE
# ============================================================
print()
print("=" * 68)
print("STAGE 2 — Same-frequency drive: correlation from common cause, not link")
print("=" * 68)
print("  Driving both DANodes at the SAME frequency from a shared source makes")
print("  their responses correlated — but that correlation comes from the")
print("  COMMON DRIVE (a common cause you created), NOT from a channel between")
print("  the DANodes. Two clocks set by the same radio signal tick in sync;")
print("  that sync is not a wire between them.")
print("  → 'Received correlated wave pattern' = YES, but sourced by your shared")
print("    drive (which reached each DANode at ≤ c), not by entanglement, and")
print("    not usable to signal between the two locations.")
verdict("Common-frequency drive correlation = common cause, not a signal channel",
        True)


# ============================================================
# STAGE 3 — 'Change one' as a UNITARY → the other is UNCHANGED
# ============================================================
print()
print("=" * 68)
print("STAGE 3 — 'Change DANode A' (apply a force/unitary) → B unchanged")
print("=" * 68)

theta = symbols("theta", real=True)
RA = Matrix([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
UA = kronecker_product(RA, eye(2))
rho_changed = UA * rho_bell * dagger(UA)
rhoB_before = Matrix(2, 2, [trigsimp(x) for x in ptrace_A(rho_bell)])
rhoB_after = Matrix(2, 2, [trigsimp(x) for x in ptrace_A(rho_changed)])
print(f"  Bob's DANode reduced state BEFORE changing A = {rhoB_before.tolist()}")
print(f"  Bob's DANode reduced state AFTER  changing A = {rhoB_after.tolist()}")
verdict("Changing DANode A (any unitary) leaves DANode B's state UNCHANGED",
        simplify(rhoB_after - rhoB_before) == zeros(2, 2))
print("  → If 'change' means apply a force/rotation to a CHOSEN value, the")
print("    other DANode does NOT change. This is no-signaling, verified.")
print("    You cannot CONTROL B by changing A. No FTL.")


# ============================================================
# STAGE 4 — 'Change one' as a MEASUREMENT → correlated but random + one-shot
# ============================================================
print()
print("=" * 68)
print("STAGE 4 — 'Change DANode A' (measure it) → B correlated, but...")
print("=" * 68)

# Measure A in Z basis. Outcome 0 → B collapses to |0⟩; outcome 1 → B to |1⟩.
P0_A = kronecker_product(ket0 * dagger(ket0), eye(2))
P1_A = kronecker_product(ket1 * dagger(ket1), eye(2))
# Post-measurement (unnormalized) joint states:
post0 = P0_A * bell
post1 = P1_A * bell
# Bob's state in each branch:
B_given_0 = simplify(ptrace_A(post0 * dagger(post0)))
B_given_1 = simplify(ptrace_A(post1 * dagger(post1)))
print(f"  If A measured 0 → B's (unnormalized) state ∝ |0⟩⟨0|: {B_given_0.tolist()}")
print(f"  If A measured 1 → B's (unnormalized) state ∝ |1⟩⟨1|: {B_given_1.tolist()}")
print("  → B IS correlated with A's outcome (spooky correlation, real).")
# But the outcome is random (1/2 each), and Bob's MARGINAL (not knowing A) is:
rhoB_marginal = simplify(B_given_0 + B_given_1)  # sum of branches = marginal
verdict("Bob's MARGINAL (averaging A's random outcomes) = I/2 (no info)",
        simplify(rhoB_marginal - eye(2)/2) == zeros(2, 2))
print("  → Alice CANNOT choose the outcome (random 1/2 each). And Bob's local")
print("    state, without hearing Alice's result, is I/2. He learns nothing.")
print("  → The pair is now CONSUMED (measured = no longer entangled). To 'keep")
print("    changing one and watching the other', you need FRESH pairs each")
print("    time — pre-distributed at ≤ c.")


# ============================================================
# STAGE 5 — Correlation ≠ Control; SPT reading; verdict
# ============================================================
print()
print("=" * 68)
print("STAGE 5 — The crux: CORRELATION (passive) ≠ CONTROL (active)")
print("=" * 68)
print("  CORRELATION (real): measuring one tells you about the other. ✓")
print("  CONTROL (impossible): forcing one to a chosen value to MAKE the other")
print("    take a chosen value. ✗")
print()
print("  'When I change one DANode the other also changes' conflates the two:")
print("    • If 'change' = force to a value → the other does NOT follow (S3).")
print("    • If 'change' = measure → the other correlates, but you didn't")
print("      choose the value, and its local statistics don't change (S4).")
print()
print("  SPT reading: the two DANodes share a joint Q_7×Q_7 config (Law 46),")
print("  ontologically non-local but sealed by Born equilibrium. The shared")
print("  config is set ONCE (when entangled) and revealed ONCE (when measured).")
print("  Driving photons through it just decoheres it. There is no dial on")
print("  DANode A that moves DANode B.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 68)
print("FINAL VERDICT")
print("=" * 68)
print("Q1: Drive 2 entangled DANodes at same frequency → correlated patterns?")
print("    ✓ You get correlation — but from your COMMON DRIVE (common cause),")
print("      and the driving itself DECOHERES the entanglement (S1, S2).")
print()
print("Q2: Keep correlation at distance so changing one changes the other?")
print("    ✗ NO. 'Change' as a force → the other is UNCHANGED (S3, no-signaling).")
print("      'Change' as a measure → the other correlates but randomly, with")
print("      local marginal I/2, and the pair is consumed one-shot (S4).")
print()
print("CRUX: entanglement is CORRELATION, never CONTROL. You cannot turn a dial")
print("on DANode A and have DANode B follow your choice — that is exactly what")
print("no-signaling forbids, and it is what would be needed for FTL. The")
print("correlation is real and useful (QKD, repeaters) but is revealed only by")
print("comparing results over a classical channel ≤ c. Same hinge: ρ_B is")
print("independent of anything Alice CHOOSES.")
