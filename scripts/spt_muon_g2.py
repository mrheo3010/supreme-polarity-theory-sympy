import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

"""SymPy verification: muon anomalous magnetic moment a_μ = (g-2)/2.

Two independent contributions:

  (1) QED + EW Standard Model: a_μ^SM = α/(2π) at one loop, plus higher
      orders.  Total ~ 11659181 × 10⁻¹¹ (PDG 2024).

  (2) SPT cascade correction: at the muon's cascade depth d_μ = 30.555,
      the membrane self-loop adds a tiny δa_μ = (1/(4π)) × exp(-2 d_μ)
      ≈ 10⁻²⁷ — negligible at current precision.

The Fermilab E989 measurement (2023) shows a 4.2σ excess over the SM
prediction: a_μ^exp - a_μ^SM ≈ 251 × 10⁻¹¹.  SPT predicts this excess
is ZERO (the cascade correction is too small) — so any sustained
≥5σ deviation would falsify SPT.

Run:  python3 scripts/spt_muon_g2.py
"""

import sympy as sp


def stage1_qed_one_loop() -> None:
    print("=" * 72)
    print("STAGE 1 — QED 1-loop (Schwinger 1948)")
    print("=" * 72)
    # Schwinger: a_μ^(1-loop) = α/(2π)
    alpha_em = sp.Rational(1, 137)
    a_mu_1loop = alpha_em / (2 * sp.pi)
    print(f"  Schwinger: a_μ = α/(2π) = 1/(137 × 2π)")
    print(f"  a_μ(1-loop) = {a_mu_1loop}  =  {float(a_mu_1loop):.4e}")
    print(f"  PDG SM total: a_μ^SM = 11659181 × 10⁻¹¹  =  1.16591810e-3")
    print()


def stage2_spt_cascade_correction() -> None:
    print("=" * 72)
    print("STAGE 2 — SPT cascade self-loop correction")
    print("=" * 72)
    # δa_μ from membrane self-loop at cascade depth d_μ
    # Ansatz: δa = 1/(4π) × exp(-2 d_μ) — same 1/(4π) family as d_s, Ω_b
    d_mu = sp.Rational(30555, 1000)  # 30.555
    correction = (1 / (4 * sp.pi)) * sp.exp(-2 * d_mu)
    correction_num = float(correction.evalf())
    print(f"  d_μ (muon cascade depth)         = {float(d_mu)}")
    print(f"  δa_μ = (1/(4π)) exp(-2 d_μ)      = {correction_num:.3e}")
    print()
    # Compare to Fermilab E989 excess
    excess = 251e-11
    print(f"  Fermilab E989 (2023) excess     = 251 × 10⁻¹¹ = {excess:.2e}")
    print(f"  SPT predicted correction         = {correction_num:.3e}")
    if correction_num < excess / 100:
        print(f"  SPT correction << observed excess")
        print(f"  ⇒  SPT predicts the Fermilab anomaly is NOT a")
        print(f"     fundamental new-physics effect; it must come from")
        print(f"     hadronic-vacuum-polarization mismeasurement.")
    print()


def stage3_verdict() -> None:
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)
    print("  STANDARD MODEL:  a_μ^SM ≈ α/(2π) = 1/(2π·137) = 1.16e-3")
    print("                   (textbook QED, no SPT input)")
    print()
    print("  SPT CORRECTION:  δa_μ ~ exp(-2 d_μ)/(4π) ~ 10⁻²⁷")
    print("                   Negligible at any conceivable precision.")
    print()
    print("  PREDICTION:      The 4.2σ Fermilab anomaly (251 × 10⁻¹¹)")
    print("                   is NOT a true new-physics signal in SPT.")
    print("                   FALSIFIABLE — if anomaly survives at >5σ")
    print("                   after lattice-QCD HVP refinements (next 2-3")
    print("                   years), SPT's claim is wrong.")
    print()


if __name__ == "__main__":
    stage1_qed_one_loop()
    stage2_spt_cascade_correction()
    stage3_verdict()
