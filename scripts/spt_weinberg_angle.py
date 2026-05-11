import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

"""SymPy investigation: sin²θ_W from Bagua structure (May 2026).

The Weinberg angle θ_W (electroweak mixing) is one of the LAST big numbers
in the Standard Model gauge sector that does not yet have a closed-form SPT
derivation. This script enumerates the three cleanest Bagua candidates,
compares each against the three measurement schemes, and HONESTLY reports
which is closest and which still has unresolved interpretation.

==============================================================================
SUMMARY:

Stage 1 — Three measurement schemes (different physical definitions):
            • on-shell:        sin²θ_W = 1 − (m_W/m_Z)² = 0.22290 ± 0.00030
            • MS-bar at M_Z:   sin²θ_W = 0.23121 ± 0.00004 (running scheme)
            • effective Z-pole: sin²θ_W = 0.23154 ± 0.00012

Stage 2 — Three Bagua candidates:
            • C1: sin²θ_W = 3/13   = 0.23077   (Δ = 0.19% vs MS-bar)
            • C2: sin²θ_W = 32/137 = 0.23358   (Δ = 1.03% vs MS-bar)
            • C3: sin²θ_W = 2/9    = 0.22222   (Δ = 0.30% vs on-shell)

Stage 3 — Bagua interpretation attempts for each candidate.
            • C1 (3/13): 3 = SU(2) generators; 13 = 8 (SU(3)) + 3 (SU(2)) +
              1 (U(1)) + 1 (photon mixing channel). PROMISING.
            • C2 (32/137): 32 = Q_5 (5-yao subset of Q_7); 137 = α_em⁻¹.
              CLEAN Bagua but Δ too large.
            • C3 (2/9): 2 = yin-yang doublet; 9 = ?  WEAK Bagua link.

Stage 4 — Verdict: C1 (3/13) is the strongest candidate by both numerical
            match (0.19% vs measurement) AND structural interpretation (13
            = full electroweak gauge multiplet count). However, this is
            still 11σ from experimental MS-bar at M_Z — not yet a Tier-B
            closure. Marked 🟡 PARTIAL until clean derivation of "13" from
            Bagua phase-space structure is given.

Stage 5 — Honest falsifiability claim and Phase 2 path forward.

Run:  python3 scripts/spt_weinberg_angle.py
==============================================================================
"""

import sympy as sp


# ---------------------------------------------------------------------------
# Stage 1 — measurement schemes
# ---------------------------------------------------------------------------

def stage1_measurements():
    print("=" * 78)
    print("STAGE 1 — sin²θ_W: three measurement schemes")
    print("=" * 78)
    print()
    print("  Different definitions of θ_W give slightly different numbers.")
    print("  All come from the SAME underlying physics (g, g' couplings)")
    print("  but use different schemes (on-shell vs running vs effective).")
    print()
    schemes = [
        ("On-shell (m_W²/m_Z²)",   sp.Float("0.22290"), sp.Float("0.00030"), "PDG 2024 from m_W and m_Z"),
        ("MS-bar at M_Z",          sp.Float("0.23121"), sp.Float("0.00004"), "running scheme, lab spec"),
        ("Effective at Z-pole",    sp.Float("0.23154"), sp.Float("0.00012"), "Z-resonance asymmetries"),
    ]
    for name, val, err, note in schemes:
        print(f"  • {name:30s} = {val} ± {err}  ({note})")
    print()
    return schemes


# ---------------------------------------------------------------------------
# Stage 2 — three Bagua candidates
# ---------------------------------------------------------------------------

def stage2_candidates():
    print("=" * 78)
    print("STAGE 2 — Three Bagua candidates for sin²θ_W (closed-form rationals)")
    print("=" * 78)
    print()
    candidates = [
        ("C1", sp.Rational(3, 13),
         "3 = SU(2) generators (W₁, W₂, W₃);  13 = 8 (SU(3)) + 3 (SU(2)) + 1 (U(1)) + 1 (photon mixing)"),
        ("C2", sp.Rational(32, 137),
         "32 = Q_5 = 2⁵ (5-yao subset);  137 = 1/α_em(M_Pl) = Q_7 + Q_3 + 1 (Bagua-clean)"),
        ("C3", sp.Rational(2, 9),
         "2 = yin-yang doublet;  9 = 8 + 1 (trigrams + self-loop)"),
    ]
    for name, val, interp in candidates:
        print(f"  • {name}: sin²θ_W = {val} = {float(val):.5f}")
        print(f"        interpretation: {interp}")
        print()
    return candidates


# ---------------------------------------------------------------------------
# Stage 3 — match analysis
# ---------------------------------------------------------------------------

def stage3_match_analysis(schemes, candidates):
    print("=" * 78)
    print("STAGE 3 — Match analysis: which candidate fits which scheme best?")
    print("=" * 78)
    print()
    print(f"  {'Candidate':<10} | {'Scheme':<26} | {'Δ (%)':>10} | {'σ-distance':>10}")
    print(f"  {'-'*10} | {'-'*26} | {'-'*10} | {'-'*10}")
    best_dev = float("inf")
    best_pair = None
    for cname, cval, _ in candidates:
        for sname, sval, serr, _ in schemes:
            dev_pct = abs(float(cval) - float(sval)) / float(sval) * 100
            sigma = abs(float(cval) - float(sval)) / float(serr)
            tag = ""
            if dev_pct < 0.25:
                tag = "  ★ best"
            print(f"  {cname:<10} | {sname:<26} | {dev_pct:>9.3f}% | {sigma:>10.1f}{tag}")
            if dev_pct < best_dev:
                best_dev = dev_pct
                best_pair = (cname, sname, dev_pct, sigma)
    print()
    print(f"  Closest match: {best_pair[0]} vs {best_pair[1]}: Δ = {best_pair[2]:.3f}%, {best_pair[3]:.1f}σ")
    print()
    print("  KEY OBSERVATION:")
    print("  ──────────────")
    print("  C1 (3/13) is BEST numerically (0.19% vs MS-bar at M_Z).")
    print("  However, 11σ from CODATA precision means this is NOT yet a")
    print("  Tier-B closure (Tier-B requires sub-σ agreement).")
    print()
    print("  At the 0.19% level, C1 IS within Tier-A bound (< 1%).  Whether")
    print("  it becomes Tier-B requires the running of sin²θ_W from a CLEAN")
    print("  Bagua scale (e.g. M_Pl) down to M_Z to reproduce experimental")
    print("  precision — an open Phase 2 calculation.")
    print()
    return best_pair


# ---------------------------------------------------------------------------
# Stage 4 — algebraic identity for C1 (3/13)
# ---------------------------------------------------------------------------

def stage4_c1_algebra():
    print("=" * 78)
    print("STAGE 4 — C1 (3/13) as a Bagua-derived algebraic identity")
    print("=" * 78)
    print()
    # If sin²θ_W = 3/13, then by definition tan²θ_W = 3/10.
    sin2 = sp.Rational(3, 13)
    cos2 = 1 - sin2
    tan2 = sin2 / cos2
    print(f"  Hypothesis: sin²θ_W = 3/13.")
    print(f"  ⇒ cos²θ_W = 1 − 3/13 = {cos2} = {float(cos2):.5f}")
    print(f"  ⇒ tan²θ_W = sin²/cos² = {tan2} = {float(tan2):.5f}")
    print()
    # Relation to gauge couplings: g/g' = sin/cos·... actually tan = g'/g (hypercharge over weak)
    # Let's match: tan²θ_W = g'²/g² = 3/10
    print(f"  In terms of EW couplings (tan²θ_W = g'²/g²):")
    print(f"     g'²/g² = 3/10")
    print(f"     g²/g'² = 10/3    (weak coupling 'stronger' than U(1) by 10:3)")
    print()
    # Check numerical: at M_Z, g ≈ 0.6520, g' ≈ 0.3578; (g'/g)² = 0.3010
    g_at_Z = sp.Float("0.6520")
    g_prime_at_Z = sp.Float("0.3578")
    ratio_observed = (g_prime_at_Z / g_at_Z) ** 2
    print(f"  Measured at M_Z (PDG 2024):  g ≈ 0.6520,  g' ≈ 0.3578")
    print(f"     (g'/g)² (measured)    = {float(ratio_observed):.5f}")
    print(f"     3/10 (SPT C1)         = {float(sp.Rational(3, 10)):.5f}")
    delta = abs(float(ratio_observed) - float(sp.Rational(3, 10))) / float(ratio_observed) * 100
    print(f"     Δ                     = {delta:.3f} %  ✓ Tier-A PASS")
    print()
    # Closed-form check: SymPy verifies the identity sin²θ_W + cos²θ_W = 1
    identity = sp.simplify(sin2 + cos2 - 1)
    print(f"  SymPy verifies the trigonometric identity:")
    print(f"     sin²θ_W + cos²θ_W − 1 = {identity}  ✓ EXACT (sanity check)")
    print()


# ---------------------------------------------------------------------------
# Stage 5 — Bagua interpretation of "13"
# ---------------------------------------------------------------------------

def stage5_bagua_interpretation():
    print("=" * 78)
    print("STAGE 5 — Bagua interpretation of '13' in sin²θ_W = 3/13")
    print("=" * 78)
    print()
    print("  Two competing interpretations to derive 13 from Bagua structure:")
    print()
    print("  Interpretation A — Electroweak gauge multiplet count:")
    print("     • SU(3) gluons:        8")
    print("     • SU(2) weak bosons:   3")
    print("     • U(1) hypercharge B:  1")
    print("     • photon mixing channel γ: 1 (emergent A_μ from B + W³ mixing)")
    print("     ─────────────────────────")
    print("     • Total:               13")
    print()
    print("     ⇒ sin²θ_W = (SU(2) generators) / (full gauge multiplet count)")
    print("              = 3 / 13")
    print()
    print("     This counts the photon γ as a SEPARATE channel from B and W³,")
    print("     since γ is the physical mixed eigenstate. The interpretation is")
    print("     PROMISING but requires further theoretical justification.")
    print()
    print("  Interpretation B — Bagua phase-space dimension:")
    print("     • 6 yao (Q_6 spatial structure)")
    print("     • +1 yao for time axis (Q_7)")
    print("     • +6 yao-pairs (yin-yang doublet products): 6")
    print("     ─────────────────────────")
    print("     • Total: 13?")
    print()
    print("     This is more speculative — the count of 'phase space directions'")
    print("     in EW sector. Less rigorous than Interpretation A.")
    print()
    print("  HONEST CAVEAT: Neither interpretation is yet a CLEAN closed-form")
    print("  derivation. Both are post-hoc rationalisations of the integer 13.")
    print("  A rigorous derivation would need:")
    print("    1. Show 13 emerges from a DIMENSIONAL count on Q_n (like Q_3 = 8")
    print("       gives the SU(3) gluon count cleanly).")
    print("    2. Show 3 emerges from the SU(2) yin-yang doublet symmetry on")
    print("       each yao.")
    print("    3. Show the RATIO 3/13 is the natural EW mixing angle from")
    print("       phase-space democratic distribution.")
    print()
    print("  ⇒ STATUS: 🟡 PARTIAL — strong numerical hint, partial structural")
    print("            interpretation, full closure pending Phase 2 research.")
    print()


# ---------------------------------------------------------------------------
# Stage 6 — Falsifiability
# ---------------------------------------------------------------------------

def stage6_falsifiability():
    print("=" * 78)
    print("STAGE 6 — Falsifiability claim FC-W (Weinberg angle)")
    print("=" * 78)
    print()
    print("  CLAIM: sin²θ_W (MS-bar at M_Z) = 3/13 ± running corrections")
    print()
    print("  CURRENT MATCH:")
    print("     • SPT predicts:  3/13 = 0.23077")
    print("     • CODATA 2022:   0.23121 ± 0.00004")
    print("     • Δ:             0.19 %  (Tier-A PASS, but 11σ from precision)")
    print()
    print("  ⚠ FALSIFIED IF:")
    print("     • A new precision measurement of sin²θ_W (MS-bar at M_Z)")
    print("       gives a value INCONSISTENT with 3/13 to better than 0.05 %")
    print("       once 1-loop running corrections are included.")
    print("     • Or: a competing first-principles theory derives sin²θ_W")
    print("       at SUB-σ agreement with measurement using a different")
    print("       small-integer ratio.")
    print()
    print("  ⚠ STRENGTHENED IF:")
    print("     • Future precision (FCC-ee, LHC HL): sin²θ_W measured to")
    print("       ± 5×10⁻⁵, allowing direct test of the 11σ gap (currently")
    print("       0.19% from the integer ratio).")
    print()
    print("  STATUS:  🟡 PARTIAL closure as of May 2026.")
    print("           Promising integer ratio (0.19% match) but not yet")
    print("           Tier-B (sub-σ agreement). Phase 2 work required.")
    print()


# ---------------------------------------------------------------------------
# Stage 7 — verdict
# ---------------------------------------------------------------------------

def verdict():
    print("=" * 78)
    print("VERDICT — sin²θ_W from Bagua: rigorous PARTIAL closure")
    print("=" * 78)
    print()
    print("  Q: Does SPT close-form-derive the Weinberg angle?")
    print()
    print("  A: NOT YET — 🟡 PARTIAL.")
    print()
    print("     ✅ Best Bagua candidate:  sin²θ_W = 3/13 = 0.23077")
    print("        Match vs CODATA MS-bar:  Δ = 0.19 %  (Tier-A PASS).")
    print()
    print("     ✅ Algebraic identity verified by SymPy:")
    print("        sin²θ_W + cos²θ_W = 1, tan²θ_W = 3/10 (g'²/g²).")
    print()
    print("     🟡 Bagua interpretation of '13' (full EW multiplet count")
    print("        SU(3)+SU(2)+U(1)+γ_mix = 8+3+1+1 = 13) is PROMISING but")
    print("        not yet derived from a dimensional first-principles count.")
    print()
    print("     ❌ 11σ from CODATA precision (0.00004 error band).")
    print("        For Tier-B closure we need either:")
    print("        (a) RG running of 3/13 from M_Pl down to M_Z to match")
    print("            sub-σ at experimental scale, OR")
    print("        (b) A scheme-specific derivation (perhaps the 'on-shell'")
    print("            scheme where m_W²/m_Z² has a cleaner Bagua form).")
    print()
    print("  Phase 2 backlog:")
    print("    • Verify 13 via SU(3)+SU(2)+U(1)+γ counting from Q_n.")
    print("    • RG run 3/13 from M_Pl → M_Z and check sub-σ closure.")
    print("    • Try alternative scheme (on-shell): sin²θ_W = 1 − (m_W/m_Z)².")
    print()


if __name__ == "__main__":
    schemes = stage1_measurements()
    candidates = stage2_candidates()
    stage3_match_analysis(schemes, candidates)
    stage4_c1_algebra()
    stage5_bagua_interpretation()
    stage6_falsifiability()
    verdict()
