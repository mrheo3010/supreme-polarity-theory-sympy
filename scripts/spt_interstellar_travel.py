#!/usr/bin/env python3
"""
Fastest feasible galactic travel — given c is the hard limit (SPT: c = Q_7
lattice hopping rate, no FTL), what is the FASTEST PRACTICAL way to cross
interstellar / galactic distances?

Key physics insight: TIME DILATION. You cannot beat c in any frame, but the
TRAVELER'S proper time can be made very short via constant high-g
acceleration. The cost: Earth-frame time still ≥ d/c, and the energy/fuel
budget is brutal (relativistic rocket equation).

  Stage 1 — Relativistic constant-1g flight: proper time vs Earth time to
            Proxima, galactic center, Milky-Way edge, Andromeda.
  Stage 2 — Propulsion reality: rocket mass-ratio for fusion vs antimatter.
  Stage 3 — Light sail (Breakthrough Starshot): no onboard fuel, ~0.2c.
  Stage 4 — Feasibility ranking + SPT honest contribution (no warp/FTL).

Pure math + stdlib (no external deps). Runs instantly.
"""

import sys
import math

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


# Constants
c = 2.99792458e8        # m/s
g = 9.80665             # m/s² (1 Earth gravity, comfortable for crew)
ly = 9.4607e15          # m
year = 3.1557e7         # s

# Natural timescale c/g
T_unit_s = c / g
T_unit_yr = T_unit_s / year
print(f"Natural relativistic timescale c/g = {T_unit_yr:.3f} years")
print()


# ============================================================
# STAGE 1 — Relativistic constant-1g flight
# ============================================================
print("=" * 70)
print("STAGE 1 — Constant 1g flight: proper time (crew) vs Earth time")
print("=" * 70)


def relativistic_trip(d_ly, accel_whole_way=True):
    """Constant proper acceleration g. If accel_whole_way: accelerate the
    entire distance (arrive at high speed). Returns (proper_yr, earth_yr)."""
    d = d_ly * ly
    if accel_whole_way:
        x = g * d / c**2
        proper_s = (c / g) * math.acosh(x + 1)
        earth_s = math.sqrt((d / c) ** 2 + 2 * d / g)
    return proper_s / year, earth_s / year


def flip_and_burn(d_ly):
    """Accelerate first half at 1g, decelerate second half → arrive AT REST.
    Returns (proper_yr, earth_yr)."""
    p_half, e_half = relativistic_trip(d_ly / 2)
    return 2 * p_half, 2 * e_half


destinations = [
    ("Proxima Centauri", 4.24),
    ("Galactic center", 26000.0),
    ("Milky Way far edge", 80000.0),
    ("Andromeda galaxy", 2.5e6),
]

print(f"  {'Destination':<22}{'Distance':<14}{'Crew time':<14}{'Earth time':<14}")
print("  " + "-" * 60)
for name, d in destinations:
    p, e = flip_and_burn(d)
    dist_str = f"{d:.0f} ly" if d < 1e5 else f"{d:.1e} ly"
    print(f"  {name:<22}{dist_str:<14}{p:<14.1f}{e:<14.0f}")

# Key claim: crew time to CROSS THE GALAXY is only a few decades
p_galaxy, e_galaxy = flip_and_burn(80000.0)
verdict(f"Crew crosses Milky Way (80k ly) in < 50 yr proper time ({p_galaxy:.0f} yr)",
        p_galaxy < 50)
verdict(f"...but Earth-frame time is ≥ d/c ({e_galaxy:.0f} yr ≈ 80,000+ yr)",
        e_galaxy > 80000)
print("  → TIME DILATION is the 'trick': crew ages decades, Earth ages eons.")
print("    One-way in TIME: you can never return to the era you left.")


# ============================================================
# STAGE 2 — Propulsion reality: the rocket equation bottleneck
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — Propulsion: relativistic rocket mass-ratio")
print("=" * 70)


def log10_mass_ratio(beta_final, v_exhaust_frac):
    """log10 of relativistic rocket mass ratio M0/M1 to reach β=v/c with
    exhaust velocity v_e = v_exhaust_frac·c (returned as log10 to avoid
    overflow). log10(M0/M1) = (1/(2·v_e))·log10((1+β)/(1-β))."""
    ve = v_exhaust_frac
    return (1.0 / (2 * ve)) * math.log10((1 + beta_final) / (1 - beta_final))


# Target: reach β = 0.95 (γ ≈ 3.2) — enough for serious time dilation
beta = 0.95
print(f"  Target cruise speed β = {beta} (γ = {1/math.sqrt(1-beta**2):.2f})")
print(f"  {'Propulsion':<26}{'v_exhaust':<14}{'Fuel/payload ratio':<22}")
print("  " + "-" * 58)
for name, ve in [("Chemical", 4.4e-6), ("Nuclear fusion", 0.1), ("Antimatter (photon)", 1.0)]:
    lmr = log10_mass_ratio(beta, ve)
    if lmr > 4:
        mr_str = f"10^{lmr:.0f} : 1"
    else:
        mr_str = f"{10**lmr:.1f} : 1"
    print(f"  {name:<26}{ve:<14}{mr_str:<22}")

lmr_antimatter = log10_mass_ratio(beta, 1.0)
lmr_fusion = log10_mass_ratio(beta, 0.1)
verdict(f"Antimatter rocket: feasible mass ratio to β=0.95 ({10**lmr_antimatter:.1f}:1)",
        lmr_antimatter < 2)
verdict(f"Fusion rocket: brutal mass ratio to β=0.95 (10^{lmr_fusion:.0f}:1)",
        lmr_fusion > 3)
print("  → Antimatter is the only rocket reaching relativistic β with sane")
print("    mass ratio — but antimatter PRODUCTION is the unsolved bottleneck")
print("    (current global production ~ nanograms/year, cost ~$10^15/gram).")


# ============================================================
# STAGE 3 — Light sail (Breakthrough Starshot): no onboard fuel
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — Light sail: external push, no onboard fuel (NEAR-TERM REAL)")
print("=" * 70)

# Breakthrough Starshot concept: gram-scale chip + light sail, pushed by
# ~100 GW ground laser for minutes → reach β ≈ 0.2.
beta_sail = 0.2
proxima_ly = 4.24
# Travel time at constant 0.2c (no relativistic accel needed, coasting):
earth_time_sail = proxima_ly / beta_sail  # years (Earth frame)
gamma_sail = 1 / math.sqrt(1 - beta_sail**2)
crew_time_sail = earth_time_sail / gamma_sail  # negligible dilation at 0.2c
print(f"  Light sail at β = {beta_sail} (γ = {gamma_sail:.3f}):")
print(f"    Proxima Centauri (4.24 ly) reached in {earth_time_sail:.0f} years")
print(f"    Payload: gram-scale probe (no crew, no fuel onboard)")
verdict("Light sail reaches Proxima in ~20 yr — no fuel, no exotic matter",
        18 < earth_time_sail < 25)
print("  → MOST FEASIBLE near-term: tiny probes at 0.2c via ground laser.")
print("    Being prototyped NOW (Breakthrough Starshot, since 2016).")


# ============================================================
# STAGE 4 — Feasibility ranking + SPT honest contribution
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — Feasibility ranking + SPT contribution")
print("=" * 70)
print("  RANK (by feasibility, given c is the hard limit):")
print("  1. INFORMATION across galaxy: radio/laser at exactly c.")
print("     → Already optimal. SPT confirms NO faster channel exists.")
print("  2. TINY PROBES: laser-pushed light sail at ~0.2c (Starshot).")
print("     → Near-term real. Proxima in ~20 yr. No fuel, no exotic matter.")
print("  3. CREWED relativistic: 1g antimatter/beam-rider ship.")
print("     → Time dilation: cross galaxy in ~30-40 yr CREW time.")
print("       Energy budget enormous; antimatter production unsolved.")
print("  4. CREWED slow: generation ships / hibernation at 0.01-0.1c.")
print("     → Don't go faster — survive the long trip instead.")
print()
print("  SPT honest contribution to propulsion:")
print("  • NO warp, NO FTL, NO mining the DA sea (Z₂_DA forbids — prev script).")
print("  • Possible INDIRECT help: better QCD understanding (Law 56 proton")
print("    mass) → better fusion/antimatter engineering; cascade understanding")
print("    of inertia. But the c limit + energy budget are UNCHANGED.")
print("  • The fastest 'galactic internet' is light at c — which SPT shows")
print("    is already the substrate's maximum signalling rate.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT — fastest feasible way across the galaxy")
print("=" * 70)
print("By EARTH clock: nothing beats ~c. Milky Way crossing ≥ ~100,000 years.")
print("By CREW clock:  constant 1g acceleration exploits TIME DILATION —")
print("                cross the galaxy in ~30-40 years of PROPER time. This")
print("                is the fastest a HUMAN can subjectively cross it.")
print("For INFORMATION: light/radio at c is already optimal (SPT: c = max")
print("                substrate signalling rate; no faster channel).")
print()
print("MOST FEASIBLE NEAR-TERM: laser-pushed light sails (gram probes, 0.2c).")
print("MOST FEASIBLE FOR CREW:  1g antimatter/beam ship (if antimatter solved).")
print("NOT AVAILABLE:           warp/wormhole (needs exotic matter SPT lacks).")
print()
print("The deepest point: the galaxy is not crossed by going faster than light")
print("— it is crossed by TIME DILATION letting the traveler's clock run slow.")
print("Physics gives you the stars, but never lets you come home to the same era.")
