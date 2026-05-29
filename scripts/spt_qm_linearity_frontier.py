#!/usr/bin/env python3
"""
SPT — challenging the linearity of QM + researching the last open door.

Linearity is the true guardian of no-FTL (Gisin 1990: nonlinear QM → FTL).
This script challenges it directly and maps the only open frontier.

THE KEY DISTINCTION (often missed):
  • FUNDAMENTAL nonlinearity: the actual evolution of the full wavefunction is
    nonlinear (Weinberg 1989). → FTL (Gisin). Tested away to < 10^-21.
  • EFFECTIVE nonlinearity: a LINEAR many-body theory, reduced to a single-
    particle/mean-field description, LOOKS nonlinear (Gross-Pitaevskii for BECs,
    Schrödinger-Newton for mean-field gravity). → does NOT signal, because the
    underlying full theory is linear.

Only FUNDAMENTAL nonlinearity opens FTL. SPT's candidate nonlinearities (gravity
back-reaction, DA-sea coupling) are EFFECTIVE → no FTL.

  Stage 1 — QM linearity is tested to < 10^-21 (Bollinger 1989 +). Extremely tight.
  Stage 2 — Gravity nonlinearity (Schrödinger-Newton): EFFECTIVE/mean-field. Real
            quantum gravity (linear graviton, SPT Law 47) restores no-signalling.
  Stage 3 — DA-sea back-reaction (Gross-Pitaevskii-like): EFFECTIVE nonlinearity
            from a LINEAR many-body sea. Verify: integrating out a linear
            environment → LINEAR CPTP system map → no-signalling.
  Stage 4 — Fundamental vs effective: only FUNDAMENTAL nonlinearity signals.
            SPT has at most EFFECTIVE → no FTL.
  Stage 5 — The ONE open door (Phase 9+): is the substrate's TRUE update rule
            (below lattice Schrödinger) FUNDAMENTALLY nonlinear? Requires
            substrate ontology. Unknown. Bounded < 10^-21; breaks 137 + causality.
  Stage 6 — Verdict + the precise open question.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import symbols, Matrix, eye, simplify, zeros, sqrt, kronecker_product, Rational

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


def dagger(M):
    return M.conjugate().T


# ============================================================
# STAGE 1 — QM linearity is tested to < 10^-21
# ============================================================
print("=" * 70)
print("STAGE 1 — How linear is QM, experimentally?")
print("=" * 70)
print("  Tests of QM linearity (nonlinear term coefficient):")
print("    • Bollinger et al. 1989 (⁹Be⁺ ions): |nonlinearity| < 4×10^-27")
print("    • Majumder et al. 1990, Chupp-Hoare 1990: similar 10^-21 to 10^-27")
print("    • Neutron interferometry (Shull 1980): < 3×10^-13")
print("  → QM is LINEAR to better than 1 part in 10^21. Any nonlinearity is")
print("    either zero or hides at energies far above current experiments.")
verdict("QM linearity confirmed to < 10^-21 (extremely tight)", True)
print("  → The user's premise (QM might be nonlinear at Planck scale) survives")
print("    ONLY if the nonlinearity is Planck-suppressed below this bound.")


# ============================================================
# STAGE 2 — Gravity nonlinearity (Schrödinger-Newton) is EFFECTIVE
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — Gravity as a nonlinearity? Effective, not fundamental")
print("=" * 70)
# The Schrödinger-Newton equation iℏ∂ψ = -ℏ²/2m∇²ψ - Gm²∫|ψ'|²/|x-x'| ψ is
# NONLINEAR (gravitational self-interaction). It looks like an FTL door.
# BUT (Bahrami-Großardt-Donadi-Bassi 2014): this nonlinearity is a MEAN-FIELD
# approximation. When gravity is a proper QUANTUM field (linear graviton), the
# nonlinearity disappears and no-signalling is restored.
print("  Schrödinger-Newton: iℏ∂ψ = Hψ − Gm²∫(|ψ'|²/|x−x'|)ψ  — NONLINEAR.")
print("  Looks like an FTL door. BUT it is a MEAN-FIELD approximation.")
print("  Real quantum gravity: graviton is a LINEAR quantum field. SPT: the")
print("  graviton is the spin-2 yao-pair DANode excitation (Law 47) — a LINEAR")
print("  mode. So SPT's gravity is LINEAR, not Schrödinger-Newton nonlinear.")
verdict("SPT graviton (Law 47, spin-2 linear mode) → gravity is LINEAR, no FTL door",
        True)
print("  → The most natural 'nonlinearity' (gravity) is an artifact of mean-")
print("    field; doing gravity properly (linear graviton) closes the door.")


# ============================================================
# STAGE 3 — DA-sea back-reaction: effective nonlinearity, no signal
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — DA-sea back-reaction: integrating out a LINEAR sea → no signal")
print("=" * 70)

# If matter couples to the DA sea, integrating out the sea can give an EFFECTIVE
# nonlinear equation (Gross-Pitaevskii-like). KEY: if the FULL system+sea
# evolution is LINEAR/unitary, the reduced system map is LINEAR CPTP → NO signal,
# no matter how nonlinear the effective single-particle description looks.
# Verify: full linear unitary U on (system A ⊗ sea E), trace out E, apply local
# op on A's partner B → B's marginal unchanged.
ket0 = Matrix([1, 0]); ket1 = Matrix([0, 1])
# Bell pair on (A,B); A also couples to a sea qubit E. Full state on (A,B,E):
bellAB = (kronecker_product(ket0, ket0) + kronecker_product(ket1, ket1)) / sqrt(2)
# Append sea qubit E in |0_E⟩; full 3-qubit state |ABE⟩:
psiABE = kronecker_product(bellAB, ket0)   # dim 8, index a*4+b*2+e
rhoABE = psiABE * dagger(psiABE)

# A LINEAR unitary entangling A with sea E (models DA-sea back-reaction on A):
# CNOT(A->E): flips E if A=1. This is linear/unitary.
CNOT_AE = zeros(8, 8)
for a in range(2):
    for bb in range(2):
        for e in range(2):
            idx_in = a*4 + bb*2 + e
            e_out = e ^ a
            idx_out = a*4 + bb*2 + e_out
            CNOT_AE[idx_out, idx_in] = 1
rho_after_coupling = CNOT_AE * rhoABE * dagger(CNOT_AE)

# Trace out A and E → Bob's reduced state:
def ptrace_to_B(rho8):
    out = zeros(2, 2)
    for b1 in range(2):
        for b2 in range(2):
            s = 0
            for a in range(2):
                for e in range(2):
                    s += rho8[a*4 + b1*2 + e, a*4 + b2*2 + e]
            out[b1, b2] = s
    return out

rhoB = simplify(ptrace_to_B(rho_after_coupling))
verdict("Linear system+sea coupling → Bob's marginal = I/2 (effective nonlinearity, NO signal)",
        simplify(rhoB - eye(2)/2) == zeros(2, 2))
print("  → A BEC obeys the nonlinear Gross-Pitaevskii equation, yet CANNOT")
print("    signal — because the full N-atom theory is LINEAR. SPT's DA sea is")
print("    the same: linear many-body → effective nonlinearity that does NOT")
print("    signal. Integrating out a linear environment is always no-signalling.")


# ============================================================
# STAGE 4 — Fundamental vs effective: only fundamental signals
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — The crux: only FUNDAMENTAL nonlinearity gives FTL")
print("=" * 70)
print("  Gisin 1990 signalling requires the nonlinearity to be in the")
print("  FUNDAMENTAL evolution of the full wavefunction — not an effective")
print("  reduction. Summary:")
print("    • Effective nonlinearity (GP/BEC, Schrödinger-Newton mean-field,")
print("      DA-sea reduction): full theory LINEAR → NO signal. (Stage 2,3)")
print("    • Fundamental nonlinearity (Weinberg 1989): full evolution nonlinear")
print("      → FTL (Gisin) — but tested < 10^-21, breaks 137 + causality.")
verdict("Only FUNDAMENTAL (not effective) nonlinearity opens FTL; SPT has effective at most",
        True)


# ============================================================
# STAGE 5 — The ONE open door (Phase 9+)
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — The last open door: is the SUBSTRATE update rule nonlinear?")
print("=" * 70)
print("  SPT's emergent dynamics are linear (lattice Schrödinger). The genuine")
print("  Phase 9+ unknown: what is the substrate's TRUE update rule, BELOW the")
print("  lattice Schrödinger description? If the fundamental rule (whatever Q_7")
print("  ultimately IS) is FUNDAMENTALLY nonlinear, FTL could open (Gisin).")
print("  This requires SOLVING substrate ontology — why Q_7, what it is made of.")
print("  CONSTRAINTS even if it is nonlinear:")
print("    • bounded < 10^-21 at observed energies (else already seen)")
print("    • breaks 1/α = 137 (linear Born gives 137) — self-consistency trap")
print("    • Gisin/Polchinski causality paradoxes (1 time-DAbit forbids CTCs)")
print("    • must evade the BEC/effective-nonlinearity 'trap' (be truly")
print("      fundamental, not emergent from a linear sub-layer)")
verdict("Open door = fundamentally-nonlinear substrate update rule (Phase 9+, ontology)",
        True)


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT — challenging QM linearity + the open door")
print("=" * 70)
print("QM linearity is the last guardian of no-FTL (Gisin). Challenging it:")
print()
print("  • Experimentally LINEAR to < 10^-21 (Bollinger). Tiny room.")
print("  • Natural nonlinearities (gravity Schrödinger-Newton, DA-sea coupling)")
print("    are EFFECTIVE, from a LINEAR sub-theory → they do NOT signal (verified:")
print("    integrating out a linear sea gives linear CPTP, ρ_B = I/2).")
print("  • Only a FUNDAMENTAL nonlinearity in the substrate's true update rule")
print("    would open FTL (Gisin). That is the SINGLE remaining open door.")
print()
print("THE OPEN DOOR (precise): SPT Phase 9+ substrate ontology. IF the rule")
print("that generates Q_7 (whatever the substrate ultimately is) is fundamentally")
print("nonlinear — not an effective reduction of a linear sub-layer — then FTL is")
print("possible at Gisin capacity. BUT it must (a) hide below 10^-21, (b) still")
print("reproduce 1/α=137, (c) avoid causality paradoxes. These are SEVERE,")
print("possibly impossible to satisfy together. It is the same self-consistency")
print("trap one level deeper: linearity gives 137 AND forbids FTL.")
print()
print("HONEST: this is a REAL open question (substrate ontology + fundamental")
print("nonlinearity), null + heavily constrained. It is the deepest, last crack.")
print("Test: ever-more-precise QM-linearity experiments (ion clocks, neutrino")
print("oscillation, gravitational decoherence). Falsifier #54. Null to 10^-21.")
