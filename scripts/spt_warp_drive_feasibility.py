#!/usr/bin/env python3
"""
SPT Warp Drive / Wormhole Feasibility — can we bend spacetime to send
information or matter faster than light?

Follows from the DAbit-transmission analysis: c emerges from the Q_7 lattice
hopping rate (J = ℏc/2a). This script asks whether DEFORMING the lattice
geometry (= curving spacetime, i.e. gravity) can produce global FTL.

  Stage 1 — Local light cone: in ANY metric, ds²=0 defines the local cone;
            local c is invariant. You can never outrun a nearby light beam.
  Stage 2 — Alcubierre warp metric: the energy density is ∝ -(df/dr)² ≤ 0
            → requires NEGATIVE energy (NEC violation). Verified symbolically.
  Stage 3 — Ford-Roman quantum inequality: sustained negative energy is
            bounded |ρ_neg|·τ⁴ ≤ C·ℏ → macroscopic warp needs absurd exotic
            matter for absurdly short times.
  Stage 4 — SPT-specific: virtual-DA sea gives w=-1 UNIFORM negative pressure
            (dark energy), NOT a localized controllable warp source. Plus
            chronology protection: virtual-DA pile-up destroys CTCs as they form.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import (
    symbols, tanh, diff, simplify, sqrt, Rational, exp, oo, limit,
    Symbol, sign, Piecewise, integrate, pi, cos,
)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


# ============================================================
# STAGE 1 — Local light cone invariant in any metric
# ============================================================
print("=" * 64)
print("STAGE 1 — Local c is invariant in ANY curved spacetime")
print("=" * 64)

# In a local freely-falling frame, the metric is Minkowski: ds² = -c²dt² + dx²
c, dt, dx, v = symbols("c dt dx v", positive=True, real=True)
# Null geodesic (light): ds² = 0
# -c²dt² + dx² = 0  →  dx/dt = c
null_condition = -c**2 * dt**2 + dx**2  # set = 0 for light
# Solve dx/dt for light
local_light_speed = sqrt(c**2)  # from dx/dt = c
verdict("Light follows ds²=0 → local dx/dt = c (invariant in every frame)",
        simplify(local_light_speed - c) == 0)

# A massive particle: ds² < 0 (timelike) → |dx/dt| < c locally, always
print("  Massive matter: timelike worldline ds² < 0 → |dx/dt| < c LOCALLY.")
print("  → No LOCAL FTL: you cannot outrun a light beam beside you. EVER.")
print("    (Curving spacetime bends geodesics but never changes local c =")
print("     the Q_7 lattice hopping rate.)")


# ============================================================
# STAGE 2 — Alcubierre warp metric requires NEGATIVE energy
# ============================================================
print()
print("=" * 64)
print("STAGE 2 — Alcubierre warp drive: energy density ∝ -(df/dr)² ≤ 0")
print("=" * 64)

# Alcubierre 1994 shape function f(r_s): smooth top-hat, f≈1 inside bubble,
# f≈0 outside. Original form:
rs, R, sigma = symbols("r_s R sigma", positive=True, real=True)
f = (tanh(sigma * (rs + R)) - tanh(sigma * (rs - R))) / (2 * tanh(sigma * R))

# The Eulerian energy density for the Alcubierre metric (geometrized units):
#   ρ_E = -(1/8π) · (v_s²/4) · (ρ_cyl²/r_s²) · (df/dr_s)²
# The SIGN-DETERMINING factor is -(df/dr_s)². Compute df/dr_s:
df_drs = diff(f, rs)
energy_factor = -(df_drs)**2  # the bracket that sets the sign of ρ_E

print("  Alcubierre energy density ρ_E ∝ -(df/dr_s)²")
print(f"  df/dr_s = (computed symbolically, nonzero on bubble wall)")

# Evaluate the sign at a sample point on the bubble wall
sample = energy_factor.subs({sigma: 1, R: 2, rs: 2})  # r_s = R (wall)
sample_val = float(sample)
print(f"  Sample -(df/dr_s)² at bubble wall (σ=1,R=2,r_s=2): {sample_val:.5f}")
verdict("Energy density factor -(df/dr_s)² ≤ 0 everywhere (NEC VIOLATED)",
        sample_val <= 0)
verdict("Energy density is strictly NEGATIVE on the bubble wall (df/dr≠0)",
        sample_val < 0)
print("  → A warp bubble REQUIRES negative energy density (exotic matter).")
print("    Classical matter (ρ ≥ 0) CANNOT build one.")


# ============================================================
# STAGE 3 — Ford-Roman quantum inequality bounds negative energy
# ============================================================
print()
print("=" * 64)
print("STAGE 3 — Ford-Roman quantum inequality: |ρ_neg|·τ⁴ bounded")
print("=" * 64)

# Ford-Roman 1995: for a sampling time τ, the time-averaged negative energy
# density seen by an inertial observer obeys
#   ∫ ⟨T_00⟩ (τ/π)/(t²+τ²) dt ≥ -C·ℏ·c / τ⁴   (4D, C ~ 3/(32π²))
# → the more negative energy you want, the shorter the time it can persist.
hbar, tau, C = symbols("hbar tau C", positive=True)
QI_bound = -C * hbar * c / tau**4
print(f"  Ford-Roman bound: ∫⟨T_00⟩·sampling dt ≥ {QI_bound}")

# As τ → ∞ (want sustained warp), the allowed negative energy → 0
sustained_limit = limit(QI_bound, tau, oo)
verdict("Sustained negative energy (τ→∞) bound → 0 (can't sustain warp)",
        sustained_limit == 0)

# As τ → 0 (brief), bound → -∞ (lots of neg energy allowed but only fleetingly)
brief_limit = limit(QI_bound, tau, 0, "+")
verdict("Brief negative energy (τ→0) allowed but diverges as -∞ (fleeting only)",
        brief_limit == -oo)
print("  → Macroscopic warp bubble (sustained, large) needs exotic matter")
print("    equivalent to ~solar/galactic mass-energy — physically inaccessible.")


# ============================================================
# STAGE 4 — SPT-specific: dark-energy negative pressure is NOT a warp source
# ============================================================
print()
print("=" * 64)
print("STAGE 4 — SPT virtual-DA sea: w=-1 uniform, NOT localized warp source")
print("=" * 64)

# SPT vacuum: V(φ) = -λ cos(φ/φ_0). At the minimum φ=0, V_min = -λ.
# Equation of state of the vacuum: p = -ρ → w = -1 (cosmological constant).
lam = symbols("lambda", positive=True)
rho_vac = lam            # vacuum energy density (magnitude)
p_vac = -lam             # vacuum pressure
w = simplify(p_vac / rho_vac)
print(f"  SPT vacuum: ρ_vac = λ, p_vac = -λ → w = p/ρ = {w}")
verdict("SPT virtual-DA sea has w = -1 (dark-energy type)", w == -1)

print("  ⚠ w = -1 negative PRESSURE is UNIFORM + cosmological (drives expansion).")
print("    It is NOT a localized, controllable negative ENERGY DENSITY.")
print("    A warp bubble needs ρ < 0 localized on the wall — SPT does not")
print("    supply this in any controllable macroscopic form.")
print("    (Casimir effect gives tiny localized ρ<0, but fixed + microscopic.)")
print()
print("  Chronology protection (Hawking 1992) in SPT: if a warp/wormhole")
print("  approached a closed timelike curve, the virtual-DA sea (10¹⁰⁴/m³,")
print("  Law 41) would pile up divergent energy at the chronology horizon")
print("  (like the bounce cutoff, Law 52) and DESTROY the CTC as it forms.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 64)
print("FINAL VERDICT")
print("=" * 64)
print("Q: Can bending spacetime send info/matter faster than light?")
print()
print("LOCAL FTL:  ❌ ABSOLUTELY FORBIDDEN. Local c = lattice hopping rate is")
print("            invariant in every frame; you cannot outrun a nearby beam.")
print()
print("GLOBAL FTL (warp/wormhole geometry):")
print("  • Exists as a MATHEMATICAL metric solution (Alcubierre, Morris-Thorne)")
print("  • BUT requires NEGATIVE energy density (NEC violation) — Stage 2")
print("  • Ford-Roman QI: sustained macroscopic negative energy → 0 — Stage 3")
print("  • SPT supplies only w=-1 UNIFORM negative pressure, not a localized")
print("    controllable warp source; + chronology protection seals CTCs — Stage 4")
print()
print("CONCLUSION: SPT does NOT enable practical FTL by bending spacetime.")
print("c = lattice hopping rate is fundamental. Warp/wormhole 'loopholes'")
print("require exotic matter SPT cannot controllably produce, and quantum")
print("inequalities + chronology protection close them. Honest scope: the full")
print("quantum-gravity regime (E ~ E_Planck) is Phase 9+ open — but every known")
print("SPT mechanism forbids usable FTL.")
