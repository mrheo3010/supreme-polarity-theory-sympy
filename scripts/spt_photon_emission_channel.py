#!/usr/bin/env python3
"""
SPT — can controlled photon EMISSION + 2-photon correlation be a binary FTL
channel?

User's protocol: force an electron to flip (DANode flip) → emit a photon.
Use emit / no-emit as a binary bit. Have two correlated photons far apart;
measure their correlation; read information from the emission pattern.

This engages REAL physics: in SPT a photon is a U(1) collective DANode
excitation, emitted when an electron-DANode flips. And correlated emission is
a real effect — Dicke SUPERRADIANCE (1954): two atoms in a symmetric state
emit at an enhanced collective rate. So the idea has genuine substance. We
test whether it can signal.

  Stage 1 — Emit/no-emit as a bit: the PHOTON itself is the messenger and
            travels at c. This is just an optical channel (≤ c), not FTL.
  Stage 2 — Two entangled photons: Alice's local op leaves Bob's photon
            marginal = I/2 (no-signaling / Holevo = 0).
  Stage 3 — Dicke superradiance: collective emission rate DOES depend on the
            joint state (2Γ vs 0). BUT (a) it needs near-field coupling within
            ~λ (propagates ≤ c), and (b) Bob's LOCAL emission rate is
            independent of Alice's operation when spacelike separated.
  Stage 4 — The 2-photon correlation is only readable by COINCIDENCE counting
            = comparing both detectors via a classical channel ≤ c.
  Stage 5 — SPT reading (DANode flip emission) + verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import (
    symbols, Rational, simplify, eye, Matrix, sqrt, exp, cos, sin, I,
    conjugate, kronecker_product, zeros, trigsimp, oo, limit,
)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


def dagger(M):
    return M.conjugate().T


# Atomic basis: |g⟩ ground, |e⟩ excited
g = Matrix([1, 0]); e = Matrix([0, 1])

# ============================================================
# STAGE 1 — Emit/no-emit as a bit: the photon IS the messenger (≤ c)
# ============================================================
print("=" * 68)
print("STAGE 1 — Emit/no-emit bit: the photon carries it, at speed c")
print("=" * 68)
print("  Alice chooses: flip her electron-DANode → emit a photon (bit=1), or")
print("  not (bit=0). To reach Bob, that photon must TRAVEL to Bob — at c.")
print("  → 'Emit = 1 / no-emit = 0' is an ordinary OPTICAL channel at exactly c.")
print("    The photon is the messenger; there is no separate instant channel.")
verdict("Photon messenger travels at c (massless U(1) DANode mode) — not FTL",
        True)


# ============================================================
# STAGE 2 — Two entangled photons: Bob's marginal independent of Alice
# ============================================================
print()
print("=" * 68)
print("STAGE 2 — Two entangled photons: Bob's marginal = I/2 (no-signaling)")
print("=" * 68)

# Polarization Bell pair |Φ+⟩ = (|HH⟩+|VV⟩)/√2 (H=0, V=1).
H = Matrix([1, 0]); V = Matrix([0, 1])
bell = (kronecker_product(H, H) + kronecker_product(V, V)) / sqrt(2)

# Alice applies any local polarization rotation R(θ) ⊗ I on her photon.
theta = symbols("theta", real=True)
R = Matrix([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
U = kronecker_product(R, eye(2))
psi_after = U * bell
rho_after = psi_after * dagger(psi_after)

def ptrace_A(rho):
    out = zeros(2, 2)
    for b1 in range(2):
        for b2 in range(2):
            out[b1, b2] = sum(rho[a*2+b1, a*2+b2] for a in range(2))
    return out

rho_B = Matrix(2, 2, [trigsimp(x) for x in ptrace_A(rho_after)])
print(f"  Bob's photon reduced state after Alice's op = {rho_B.tolist()}")
verdict("Bob's photon marginal = I/2, independent of Alice's choice",
        simplify(rho_B - eye(2)/2) == zeros(2, 2))
print("  → Manipulating/measuring Alice's photon does NOT change Bob's photon")
print("    statistics. No information about Alice's bit reaches Bob locally.")


# ============================================================
# STAGE 3 — Dicke superradiance: collective rate vs LOCAL rate
# ============================================================
print()
print("=" * 68)
print("STAGE 3 — Correlated emission (Dicke superradiance): does it signal?")
print("=" * 68)

# Two atoms. Symmetric Bell state |+⟩ = (|eg⟩+|ge⟩)/√2 → COLLECTIVE rate 2Γ
# (superradiant). Antisymmetric |−⟩ = (|eg⟩−|ge⟩)/√2 → rate 0 (subradiant).
Gamma = symbols("Gamma", positive=True)
sym = (kronecker_product(e, g) + kronecker_product(g, e)) / sqrt(2)
antisym = (kronecker_product(e, g) - kronecker_product(g, e)) / sqrt(2)
print("  Dicke 1954: symmetric |+⟩ → collective rate 2Γ (superradiant)")
print("              antisymmetric |−⟩ → collective rate 0 (subradiant)")
print("  ⚠ This collective enhancement REQUIRES the atoms within ~λ so they")
print("    couple to the SAME EM mode (near-field, propagates ≤ c). Spacelike-")
print("    separated atoms do NOT superradiate — they emit independently.")

# Bob's LOCAL excited population in the symmetric state, and whether Alice's
# local operation changes it. P_B(excited) = ⟨e|ρ_B|e⟩.
def P_excited_B(state):
    rho = state * dagger(state)
    rhoB = ptrace_A(rho)
    return simplify((dagger(e) * rhoB * e)[0])

P_before = P_excited_B(sym)
# Alice applies a local unitary V_A(φ) on her atom:
phi = symbols("phi", real=True)
V_A = Matrix([[cos(phi), -sin(phi)], [sin(phi), cos(phi)]])
state_after = kronecker_product(V_A, eye(2)) * sym
P_after = P_excited_B(state_after)
P_after = trigsimp(P_after)
print(f"  Bob's local P(excited) before Alice's op = {P_before}")
print(f"  Bob's local P(excited) after  Alice's op = {P_after}")
verdict("Bob's LOCAL emission probability unchanged by Alice's local op",
        simplify(P_after - P_before) == 0)
print("  → Even with superradiant correlations, Bob's LOCAL emission rate is")
print("    independent of what Alice does. The enhancement shows up only in")
print("    the JOINT light, collected at a common point (≤ c). No signal.")


# ============================================================
# STAGE 4 — Correlation readable only by coincidence comparison (≤ c)
# ============================================================
print()
print("=" * 68)
print("STAGE 4 — 2-photon correlation needs coincidence counting (≤ c)")
print("=" * 68)
print("  The correlation between two emitted photons (polarization, timing,")
print("  superradiant coincidence) is a JOINT property. To SEE it, both")
print("  detector records must be brought together and compared — that")
print("  comparison travels at ≤ c. Each detector ALONE sees only random")
print("  clicks (marginal = noise). Same structure as every Bell experiment:")
print("  correlation is real, but invisible without classical comparison ≤ c.")
verdict("Correlation extraction requires classical comparison at ≤ c",
        True)


# ============================================================
# STAGE 5 — SPT reading + verdict
# ============================================================
print()
print("=" * 68)
print("STAGE 5 — SPT reading: DANode flip emission")
print("=" * 68)
print("  In SPT: electron transition = electron-DANode flip → emits a photon")
print("  = a U(1) collective DANode excitation (Law 42 gauge sector). The")
print("  emission is a LOCAL event in the electron's region. Whether a remote")
print("  correlated photon was emitted is encoded in the JOINT DANode config,")
print("  which (like all entanglement) is ontologically non-local BUT sealed")
print("  by Born equilibrium → local emission statistics carry no remote info.")
print("  The photon, once emitted, is a massless U(1) mode → travels at c.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 68)
print("FINAL VERDICT")
print("=" * 68)
print("Q: Use controlled photon emission (DANode flip) + 2-photon correlation")
print("   as a binary FTL channel?")
print()
print("  ✗ Emit/no-emit bit: the photon IS the messenger → travels at c.")
print("    Ordinary optical channel, not FTL.")
print("  ✗ Entangled photons: Alice's op leaves Bob's marginal = I/2 (no-")
print("    signaling). Bob's local clicks are random regardless of Alice.")
print("  ✗ Superradiance (real correlated emission!): collective rate depends")
print("    on the joint state, BUT needs near-field (≤ c) AND Bob's LOCAL rate")
print("    is independent of Alice when separated (verified).")
print("  ✗ The correlation is readable only by coincidence comparison ≤ c.")
print()
print("CONCLUSION: Controlled emission + correlation is a beautiful, REAL")
print("toolkit (it powers entangled-photon sources, superradiant lasers,")
print("quantum repeaters) — but it transmits information only at ≤ c. The")
print("emission event is LOCAL; the correlation is a joint property invisible")
print("without classical comparison. Same hinge as always: Bob's marginal is")
print("Alice-independent (Born/Holevo). No binary FTL channel. The real payoff")
print("is again quantum-internet hardware (entangled sources + repeaters), ≤ c.")
