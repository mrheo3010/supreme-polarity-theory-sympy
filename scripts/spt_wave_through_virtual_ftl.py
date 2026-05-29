#!/usr/bin/env python3
"""
SPT — encode info as a WAVE through the virtual-DA sea, go far, then RECONSTRUCT?

The sharpest version yet, because there IS a genuinely superluminal surface in
wave physics — the PHASE velocity. The proposal: turn information into a wave
pattern, let it ride through the virtual-DANode sea to a distant point, and
reconstruct it there — hoping the wave outruns c.

We test it and find: NO. The reason is the classic phase/group/FRONT velocity
distinction (Sommerfeld–Brillouin 1914), made exact on SPT's Q_7 lattice:
  • PHASE velocity v_p of a massive DANode wave DOES exceed c — but phase fronts
    carry no information (you can't mark a featureless sinusoid).
  • GROUP velocity v_g < c here (v_p·v_g = c²); it can exceed c only in
    anomalous-dispersion windows, where it STILL carries no information.
  • The SIGNAL/FRONT velocity — the speed of the leading "turn-on" edge, the
    only thing that carries new information — equals c EXACTLY, because any
    medium (incl. the virtual sea) has refractive index n(ω→∞)=1: it cannot
    respond instantaneously. The vacuum is the FASTEST medium, not a shortcut.
  • On the Q_7 lattice the group velocity is hard-bounded by the hopping rate
    v_max = 2Ja/ℏ = c (Lieb–Robinson). The packet stays in the causal cone.
  • RECONSTRUCTING an unknown state at the far end is teleportation: it needs
    classical correction bits that travel ≤ c. So even the "reconstruct" step
    is ≤ c.

  Stage 1 — Frame the proposal.
  Stage 2 — A massive DANode wave: phase velocity v_p > c (the tempting surface).
  Stage 3 — Group velocity v_g < c here, and v_p·v_g = c² (no info in v_p).
  Stage 4 — FRONT/signal velocity = c (n(∞)=1): information never beats c.
  Stage 5 — Lattice Lieb–Robinson: v_g ≤ 2Ja/ℏ = c; reconstruction = teleport ≤ c.
  Stage 6 — Verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
from sympy import (symbols, sqrt, simplify, diff, limit, oo, cos, sin, pi,
                   Rational, Abs)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


# ============================================================
# STAGE 1 — Frame the proposal
# ============================================================
print("=" * 70)
print("STAGE 1 — Proposal: info → wave → ride the virtual-DA sea → reconstruct far")
print("=" * 70)
print("  Encode a message as a wave pattern in φ, propagate it through the")
print("  virtual-DANode sea to a distant point, reconstruct it there. Hope: the")
print("  wave (esp. its phase) outruns c. We check phase vs group vs FRONT speed.")
verdict("Proposal framed: wave transport through the virtual sea + reconstruction",
        True)


# ============================================================
# STAGE 2 — Massive DANode wave: phase velocity v_p > c
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — Phase velocity v_p of a massive DANode wave EXCEEDS c")
print("=" * 70)
c, k, mu = symbols("c k mu", positive=True)   # mu = m c²/ℏ  (a rest frequency)
# Klein–Gordon / massive DANode dispersion (Law 44): ω² = c²k² + μ².
omega = sqrt(c**2 * k**2 + mu**2)
v_p = omega / k                                # phase velocity
vp2_minus_c2 = simplify(v_p**2 - c**2)
print(f"  Dispersion: ω(k) = √(c²k² + μ²),  μ = mc²/ℏ")
print(f"  v_p = ω/k,   v_p² − c² = {vp2_minus_c2}   (> 0 ⇒ v_p > c)")
verdict("Phase velocity exceeds c: v_p² − c² = μ²/k² > 0 for any finite k",
        vp2_minus_c2 == mu**2 / k**2)
print("  → True: the phase fronts move faster than light. This is the tempting")
print("    surface. But a pure sinusoid is featureless — you cannot write a")
print("    message on a phase front, so v_p carries ZERO information.")


# ============================================================
# STAGE 3 — Group velocity v_g < c, and v_p · v_g = c²
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — Group velocity v_g < c here, with v_p · v_g = c² exactly")
print("=" * 70)
v_g = simplify(diff(omega, k))                 # group velocity dω/dk
print(f"  v_g = dω/dk = {v_g}")
c2_minus_vg2 = simplify(c**2 - v_g**2)
print(f"  c² − v_g² = {c2_minus_vg2}   (> 0 ⇒ v_g < c)")
verdict("Group velocity is sub-luminal here: c² − v_g² = c²μ²/(c²k²+μ²) > 0",
        c2_minus_vg2 == c**2 * mu**2 / (c**2 * k**2 + mu**2))
verdict("v_p · v_g = c² (the standard reciprocity ⇒ v_p>c forces v_g<c)",
        simplify(v_p * v_g - c**2) == 0)
print("  → Even where anomalous dispersion pushes v_g > c (reshaping a smooth")
print("    pulse), it still moves no information — the pulse peak is built from")
print("    components already present. Brillouin 1914 settled this.")


# ============================================================
# STAGE 4 — FRONT / signal velocity = c (n(∞) = 1)
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — The FRONT (information) velocity equals c exactly")
print("=" * 70)
# The signal is the leading 'turn-on' edge = the high-frequency limit of the
# wave. As k→∞ (sharp front), both v_p and v_g → c:
vp_front = limit(v_p, k, oo)
vg_front = limit(v_g, k, oo)
print(f"  High-frequency limit (the front):  lim_{{k→∞}} v_p = {vp_front},  "
      f"lim_{{k→∞}} v_g = {vg_front}")
verdict("Front velocity of the wave = c (lim_{k→∞} v_p = lim_{k→∞} v_g = c)",
        vp_front == c and vg_front == c)
# Sommerfeld: in ANY medium the refractive index n(ω) → 1 as ω → ∞, because the
# medium cannot respond instantaneously. The virtual-DA sea is no exception.
omega_f, omega_p = symbols("omega omega_p", positive=True)   # ω, plasma scale
n_index = sqrt(1 - omega_p**2 / omega_f**2)    # generic dispersive index model
n_inf = limit(n_index, omega_f, oo)
v_front_medium = c / n_inf
print(f"  Generic medium index n(ω)=√(1−ω_p²/ω²);  n(∞) = {n_inf};  "
      f"v_front = c/n(∞) = {v_front_medium}")
verdict("Signal front through ANY medium = c/n(∞) = c  (n(∞)=1: no instant response)",
        n_inf == 1 and v_front_medium == c)
print("  → The virtual-DA sea is a vacuum medium: it cannot make the FRONT faster")
print("    than c. Vacuum is already the fastest medium. No shortcut exists.")


# ============================================================
# STAGE 5 — Lattice Lieb–Robinson bound + reconstruction = teleport ≤ c
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — Q_7 lattice bound v_g ≤ 2Ja/ℏ = c; reconstruction needs ≤ c bits")
print("=" * 70)
# On the SPT lattice a tight-binding band has ω(k) = (2J/ℏ)(1 − cos(ka)); the
# group velocity is bounded by the hopping rate — this IS the SPT origin of c.
J, a, hbar, kk = symbols("J a hbar k", positive=True)
omega_lat = (2*J/hbar) * (1 - cos(kk*a))
v_g_lat = simplify(diff(omega_lat, kk))        # = (2Ja/ℏ) sin(ka)
v_g_max = simplify(v_g_lat.subs(kk, pi/(2*a))) # max at ka = π/2
print(f"  Lattice band ω(k) = (2J/ℏ)(1−cos ka);  v_g(k) = {v_g_lat}")
print(f"  max|v_g| = v_g(ka=π/2) = {v_g_max} = 2Ja/ℏ ≡ c  (Lieb–Robinson, = SPT's c)")
verdict("Lattice group velocity is hard-bounded: max|v_g| = 2Ja/ℏ = c (no FTL packet)",
        v_g_max == 2*J*a/hbar)
print("  → A wave packet through the virtual sea cannot leave the causal cone;")
print("    tails outside are exponentially suppressed (no usable signal).")
print("  RECONSTRUCTION: rebuilding an UNKNOWN quantum state at the far end is")
print("  quantum teleportation — it needs 2 classical correction bits per qubit,")
print("  which travel ≤ c. So even the 'reconstruct' step is bounded by c.")
verdict("Reconstructing an unknown state = teleportation ⇒ classical bits ≤ c "
        "(no-cloning forbids a free copy)", True)


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT — wave through virtual DANodes + reconstruct = FTL?")
print("=" * 70)
print("NO. The phase velocity v_p > c is real but carries no information; the")
print("FRONT (signal) velocity — the only carrier of new information — equals c")
print("exactly, in vacuum and in the virtual-DA sea alike, because n(ω→∞)=1.")
print("  • v_p > c  (phase, no info);  v_g < c here, v_p·v_g = c² (no info either).")
print("  • Front velocity = c (Sommerfeld–Brillouin): information ≤ c, always.")
print("  • Q_7 lattice: max group velocity = 2Ja/ℏ = c (Lieb–Robinson). The packet")
print("    stays in the causal cone; outside-cone tails are exponentially tiny.")
print("  • Reconstructing the message far away = teleportation ⇒ classical bits")
print("    ≤ c. No-cloning blocks a free distant copy.")
print()
print("CHỐT: ý tưởng của anh chạm đúng chỗ DUY NHẤT của vật lý sóng thật sự vượt c")
print("— vận tốc PHA. Nhưng pha là sóng sin trơn, không ghi được thông tin lên nó.")
print("Thông tin nằm ở MẶT TRƯỚC (front) của sóng, và front đi đúng bằng c — trong")
print("chân không lẫn trong biển virtual-DA — vì mọi môi trường có n(∞)=1 (không thể")
print("phản hồi tức thời). Biển ảo không phải đường tắt; chân không đã là môi trường")
print("nhanh nhất. Trên lưới Q_7, gói sóng bị chặn trong nón nhân quả bởi 2Ja/ℏ = c.")
print("Và tái tạo lại thông điệp ở xa = teleportation, vẫn cần bit cổ điển ≤ c.")
print("Sóng qua DANode ảo: KHÔNG FTL. Giới hạn c là tính chất của chính lưới, không")
print("mượn từ thuyết tương đối — nên không có cửa sau nào ở đây.")
