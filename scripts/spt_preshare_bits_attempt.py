#!/usr/bin/env python3
"""
SPT — Can we pre-send the 2 teleportation bits from Earth ahead of time,
so Mars just reconstructs via a FIXED formula? (A clever FTL attempt.)

The idea: in quantum teleportation Bob needs 2 classical bits (Alice's Bell-
measurement outcome). What if Earth does the Bell measurement and sends those
2 bits to Mars IN ADVANCE, so later Mars reconstructs by a fixed equation —
no real-time ≤ c communication needed?

Answer: NO. The 2 bits are the RANDOM OUTCOME of measuring (|ψ⟩ ⊗ Alice's
entangled half). They do not exist until |ψ⟩ exists AND is measured. You
cannot pre-send a number that has not been generated yet, and you cannot
force or predict the outcome (each of 4 results has probability 1/4).

  Stage 1 — The 4 Bell outcomes are equiprobable (1/4) and unpredictable.
  Stage 2 — NO single fixed unitary corrects all 4 Pauli-images to |ψ⟩.
  Stage 3 — Mars applying a FIXED correction (no live bits) → succeeds only
            1/4 of the time = pure guessing = zero information transferred.
  Stage 4 — Temporal logic: bits are POSTERIOR to measuring the target |ψ⟩.
            Pre-shared entanglement: YES (≤ c). Pre-sent outcome bits: NO.
  Stage 5 — Verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import (
    symbols, sqrt, Rational, simplify, eye, Matrix, I, conjugate,
    kronecker_product, zeros, Abs,
)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


def dagger(M):
    return M.conjugate().T


# Single-qubit basis + Pauli gates
ket0 = Matrix([1, 0]); ket1 = Matrix([0, 1])
Igate = eye(2)
X = Matrix([[0, 1], [1, 0]])
Z = Matrix([[1, 0], [0, -1]])
ZX = Z * X

alpha, beta = symbols("alpha beta", complex=True)
psi = alpha * ket0 + beta * ket1     # the unknown state to teleport

# ============================================================
# STAGE 1 — The 4 outcomes are equiprobable and unpredictable
# ============================================================
print("=" * 66)
print("STAGE 1 — Bell-measurement outcome is RANDOM (1/4 each)")
print("=" * 66)

# Full state |ψ⟩_C ⊗ |Φ+⟩_AB, then Alice Bell-measures (C,A).
bell = (kronecker_product(ket0, ket0) + kronecker_product(ket1, ket1)) / sqrt(2)
Psi = kronecker_product(psi, bell)   # 8-dim, index c*4+a*2+b

Phi_p = (kronecker_product(ket0, ket0) + kronecker_product(ket1, ket1)) / sqrt(2)
Phi_m = (kronecker_product(ket0, ket0) - kronecker_product(ket1, ket1)) / sqrt(2)
Psi_p = (kronecker_product(ket0, ket1) + kronecker_product(ket1, ket0)) / sqrt(2)
Psi_m = (kronecker_product(ket0, ket1) - kronecker_product(ket1, ket0)) / sqrt(2)
bell_basis = {"Φ+": Phi_p, "Φ-": Phi_m, "Ψ+": Psi_p, "Ψ-": Psi_m}

# Probability of each outcome = || (⟨B_i|_CA ⊗ I) |Ψ⟩ ||²
norm = alpha * conjugate(alpha) + beta * conjugate(beta)   # = 1
probs = {}
for name, b in bell_basis.items():
    M = kronecker_product(dagger(b), Igate)
    bob = M * Psi
    p = simplify((dagger(bob) * bob)[0])
    probs[name] = p
print("  Outcome probabilities:")
for name, p in probs.items():
    print(f"    P({name}) = {p}   (= 1/4 since |α|²+|β|² = 1)")
verdict("Each Bell outcome probability = (|α|²+|β|²)/4 = 1/4 when normalized",
        all(simplify(p - norm / 4) == 0 for p in probs.values()))
print("  → The outcome is fundamentally RANDOM. Alice cannot predict or force")
print("    it. So the '2 bits' do not exist until she actually measures.")


# ============================================================
# STAGE 2 — No single fixed unitary corrects all 4 branches
# ============================================================
print()
print("=" * 66)
print("STAGE 2 — NO fixed formula corrects all 4 outcomes to |ψ⟩")
print("=" * 66)

# After measurement, Bob holds one of: I|ψ⟩, Z|ψ⟩, X|ψ⟩, ZX|ψ⟩ (the 4 branches).
branches = {"Φ+": Igate * psi, "Φ-": Z * psi, "Ψ+": X * psi, "Ψ-": ZX * psi}

# Suppose Mars applies a FIXED correction U (same for every run, since it has
# no live bits). Could U = I recover |ψ⟩ from all 4? Check each:
print("  If Mars applies a FIXED U = I (no live bits), it gets:")
fixed_ok = {}
for name, state in branches.items():
    out = simplify(Igate * state)
    matches = simplify(out - psi) == zeros(2, 1)
    fixed_ok[name] = matches
    tag = "✓ = |ψ⟩" if matches else "✗ ≠ |ψ⟩ (wrong state)"
    print(f"    {name} branch → {tag}")

# A fixed U recovering BOTH |ψ⟩ and Z|ψ⟩ would require U=I and U·Z=I → Z=I,
# impossible. Prove no fixed U works for all 4:
# U·|ψ⟩ = |ψ⟩ and U·Z|ψ⟩ = |ψ⟩ ⟹ U(I - Z)... contradiction since I≠Z.
no_universal_U = not (Z == Igate)   # Z ≠ I → cannot fix both branches
verdict("No fixed unitary corrects both Φ+ and Φ- branches (would need Z=I)",
        no_universal_U)
verdict("A fixed correction works for ONLY 1 of the 4 branches",
        sum(1 for v in fixed_ok.values() if v) == 1)


# ============================================================
# STAGE 3 — Fixed correction → 1/4 success = zero information
# ============================================================
print()
print("=" * 66)
print("STAGE 3 — Fixed reconstruction succeeds only 1/4 = pure guessing")
print("=" * 66)

# Mars applies fixed U=I to a random branch (each 1/4). Success prob = 1/4.
success_prob = Rational(1, 4) * sum(1 for v in fixed_ok.values() if v)
print(f"  P(Mars reconstructs |ψ⟩ correctly with fixed formula) = {success_prob}")
verdict("Fixed-formula success = 1/4 (same as random guessing → no info)",
        success_prob == Rational(1, 4))

# Mars's averaged output state (mixture over 4 equally-likely branches) = I/2:
rho_mars = zeros(2, 2)
for name, state in branches.items():
    rho_mars += Rational(1, 4) * (Igate * state) * dagger(Igate * state)
rho_mars = simplify(rho_mars)
verdict("Mars's averaged state = (|α|²+|β|²)/2·I = I/2 (no info without bits)",
        simplify(rho_mars - (norm / 2) * eye(2)) == zeros(2, 2))
print("  → Without the LIVE outcome bits, Mars's result is indistinguishable")
print("    from preparing a random state. Zero information arrives. No FTL.")


# ============================================================
# STAGE 4 — Temporal logic: bits are POSTERIOR to the target state
# ============================================================
print()
print("=" * 66)
print("STAGE 4 — Why you cannot pre-send the bits")
print("=" * 66)
print("  The 2 bits = OUTCOME of measuring (|ψ⟩ ⊗ Alice's entangled half).")
print("  Causal order is forced:")
print("    (1) |ψ⟩ must EXIST at Earth.")
print("    (2) Earth performs the Bell measurement → destroys |ψ⟩, emits")
print("        2 RANDOM bits (one of 4, each 1/4).")
print("    (3) Earth sends those 2 bits to Mars at ≤ c.")
print("    (4) Mars applies the matching correction → recovers |ψ⟩.")
print()
print("  You cannot pre-send bits at step (3) before step (2) happens — the")
print("  bits do not exist yet, and they are unpredictable. 'Pre-sending the")
print("  bits' would mean the measurement already happened, i.e. the state")
print("  |ψ⟩ you wanted to teleport already existed at Earth and was consumed.")
print()
print("  What CAN be pre-shared: the ENTANGLED PAIR (sent ahead at ≤ c). That")
print("  saves the entanglement-distribution latency. But each pair is used")
print("  ONCE, and the outcome bits are always generated fresh AFTER you")
print("  measure the specific state you want to send. Net latency ≥ d/c.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 66)
print("FINAL VERDICT")
print("=" * 66)
print("Q: Pre-send the 2 bits from Earth, then Mars reconstructs by a")
print("   fixed formula — no live communication?")
print()
print("  ✗ NO. The 2 bits are the RANDOM result of a measurement that can")
print("    only happen AFTER |ψ⟩ exists. They cannot be pre-sent (they don't")
print("    exist yet) and cannot be predicted or forced (each outcome 1/4).")
print("  ✗ No fixed unitary recovers |ψ⟩ from all 4 branches (would need Z=I).")
print("    A fixed correction works 1/4 of the time = pure guessing = no info.")
print("  ✓ You CAN pre-share the entangled pair (≤ c, once). But the outcome")
print("    bits are always fresh and must travel ≤ c after the measurement.")
print()
print("CONCLUSION: Pre-loading the bits is impossible because of causal order:")
print("the bits are POSTERIOR to measuring the target state. Teleportation")
print("latency is always ≥ d/c. No instantaneous transfer. The deep reason:")
print("measurement outcomes are genuinely NEW random information (Born rule),")
print("not pre-existing data — you cannot send them before they are born.")
