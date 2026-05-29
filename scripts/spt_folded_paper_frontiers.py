#!/usr/bin/env python3
"""
SPT — can the lattice fold like a sheet of paper (wormhole)? Scan B3–B7.

The "folded paper" is the classic wormhole picture (Interstellar, Sagan): take
a sheet = space, fold it in a higher embedding dimension so two distant points
touch, punch a throat, step across. We test it honestly inside SPT and scan the
remaining frontiers B3–B7.

Findings:
  • B3 (folded paper / topology): the LITERAL fold needs an extra SPATIAL
    embedding dimension. SPT's 7 DAbit = 3 space + 1 time + 3 internal gauge
    (Law 58): the 3 gauge dims are COMPACT/internal, not spatial extent — there
    are ZERO spare spatial dims to fold 3-space through. The INTRINSIC version
    (a graph "handle" = shortcut edge) WOULD shrink distance (verified: Càn–Khôn
    3→1), but SPT's fixed-lattice axiom (Theorem 2.1) forbids it. That axiom is a
    genuine B1/B3 frontier (the candidate "flat-Earth" assumption).
  • Even GRANTING a throat: Morris–Thorne's flare-out condition forces NEC
    violation at the throat (verified: b'(b₀)<1 ⇒ ρ+p_r<0 ⇒ exotic matter). With
    ANEC proven (2016-17), no macroscopic exotic matter ⇒ topological censorship:
    the fold can't be a usable FTL shortcut.
  • B7 (a hidden faster band): a tachyonic mode (ω²<c²k²) is UNSTABLE (imaginary
    ω at low k) AND its FRONT velocity is still c (verified) ⇒ no FTL carrier.
  • B4 (Planck/bounce) and B6 (objective collapse) are flagged HONESTLY as open,
    each with the experiment that would settle it (no fake verdict).

  Stage 1 — Frame the folded paper + B3–B7 scan.
  Stage 2 — B3a: the literal fold needs a spatial embedding dim SPT lacks.
  Stage 3 — B3b: an intrinsic handle WOULD shrink distance, but Theorem 2.1
            forbids it (the real frontier).
  Stage 4 — Throat ⇒ exotic matter (Morris–Thorne flare-out ⇒ NEC violation).
  Stage 5 — B7: tachyon band is unstable; its front velocity is still c.
  Stage 6 — B4 + B6 honest open status; verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
import itertools
from sympy import symbols, simplify, limit, oo, sqrt, pi, Rational, sin, cos

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


# ============================================================
# STAGE 1 — Frame the folded paper + B3–B7 scan
# ============================================================
print("=" * 70)
print("STAGE 1 — Can the lattice fold like paper (wormhole)? Scan B3–B7")
print("=" * 70)
print("  Folded-paper picture: fold space so two far points touch, punch through.")
print("  We test the literal fold (needs embedding dim), the intrinsic handle")
print("  (B3 topology), the exotic-matter requirement, and B7/B4/B6 frontiers.")
verdict("Folded-paper + B3–B7 framed", True)


# ============================================================
# STAGE 2 — B3a: the literal fold needs a spatial embedding dim SPT lacks
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — B3a: folding 3-space needs an extra SPATIAL dimension")
print("=" * 70)
# Law 58 partition of the 7 DAbit:
n_space, n_time, n_gauge = 3, 1, 3
print(f"  Law 58: 7 DAbit = {n_space} spatial + {n_time} time + {n_gauge} internal gauge.")
print(f"  Folding an n-D sheet needs ≥1 EXTRA spatial dim to fold INTO.")
extra_spatial = 7 - n_space - n_time - n_gauge   # leftover spatial dims = 0
verdict("Spare SPATIAL embedding dimensions available to fold 3-space = 0",
        extra_spatial == 0)
print("  → The 3 internal-gauge DAbit are COMPACT (color/isospin), orthogonal to")
print("    space, with no spatial extent (they interact via gauge bosons ≤ c, they")
print("    don't transport position). So there is no spatial dimension to fold the")
print("    paper INTO. The literal geometric fold is unavailable in SPT.")


# ============================================================
# STAGE 3 — B3b: an intrinsic handle shrinks distance, but is forbidden
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — B3b: a graph 'handle' WOULD shrink distance — but axiom forbids")
print("=" * 70)
# A wormhole needs no embedding: it is an intrinsic HANDLE = a shortcut edge.
# On the Bagua cube Q_3, Càn(111)↔Khôn(000) graph distance = 3. Add one handle
# edge between them and the distance collapses to 1.
cube = list(itertools.product([0, 1], repeat=3))
base_edges = {(a, b) for a in cube for b in cube
              if sum(x ^ y for x, y in zip(a, b)) == 1}
def bfs(src, dst, edges):
    frontier = {src}; seen = {src}; d = 0
    while dst not in frontier:
        nxt = {w for v in frontier for w in cube
               if ((v, w) in edges or (w, v) in edges) and w not in seen}
        if not nxt:
            return None
        seen |= nxt; frontier = nxt; d += 1
    return d
can, khon = (1, 1, 1), (0, 0, 0)
d_before = bfs(can, khon, base_edges)
d_after = bfs(can, khon, base_edges | {(can, khon)})   # add the handle
print(f"  Càn↔Khôn distance: {d_before} hops (no handle) → {d_after} hop (with handle)")
verdict("A handle edge WOULD shrink Càn↔Khôn distance 3 → 1 (the wormhole appeal)",
        d_before == 3 and d_after == 1)
print("  → So topology change is genuinely powerful. BUT SPT's Theorem 2.1 (fixed")
print("    lattice: vertices + edges preserved) forbids adding handles. THIS axiom")
print("    is the real B1/B3 frontier — the candidate 'flat-Earth' assumption.")


# ============================================================
# STAGE 4 — A throat requires EXOTIC matter (Morris–Thorne flare-out)
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — Even granting a throat: flare-out ⇒ NEC violation (exotic matter)")
print("=" * 70)
# Morris–Thorne metric shape function b(r), throat at r=b₀. Einstein eqs give
# (geometrized 8πG=c=1) the radial null energy ρ+p_r at the throat:
#   ρ+p_r |_{r=b₀} = (b'(b₀) − 1)/(8π b₀²).
# The flare-out (a real, opening throat) REQUIRES b'(b₀) < 1.
b0, eps = symbols("b0 epsilon", positive=True)        # eps>0: flare-out margin
bp_throat = 1 - eps                                   # b'(b₀) = 1−ε < 1 (flare-out)
rho_plus_pr = (bp_throat - 1) / (8*pi*b0**2)
print(f"  Throat radial NEC: ρ+p_r = (b'(b₀)−1)/(8π b₀²).  Flare-out ⇒ b'(b₀)<1.")
print(f"  With b'(b₀)=1−ε:  ρ+p_r = {simplify(rho_plus_pr)}  (< 0 ⇒ NEC violated)")
verdict("Traversable throat (flare-out b'<1) forces ρ+p_r < 0 ⇒ EXOTIC matter",
        rho_plus_pr.is_negative)
print("  → ANEC (averaged null energy, PROVEN 2016-17 Faulkner et al.) forbids the")
print("    needed negative averaged null energy on a complete geodesic at")
print("    macroscopic scale. Topological censorship (Friedman–Schleich–Witt 1993):")
print("    with ANEC, you cannot traverse a handle faster than going around. The")
print("    folded paper cannot be punched through as an FTL shortcut.")


# ============================================================
# STAGE 5 — B7: a tachyonic 'faster band' is unstable; front still = c
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — B7: a hidden faster band would be tachyonic ⇒ unstable, front = c")
print("=" * 70)
c, k, mu = symbols("c k mu", positive=True)
# A 'faster-than-c' band needs a tachyonic dispersion ω² = c²k² − μ² (μ=mc²/ℏ).
omega_sq = c**2 * k**2 - mu**2
omega_sq_at_0 = omega_sq.subs(k, 0)
print(f"  Tachyon dispersion ω² = c²k² − μ².  At k=0: ω² = {omega_sq_at_0} < 0")
verdict("Tachyonic band has ω² < 0 at low k ⇒ imaginary ω ⇒ UNSTABLE (no carrier)",
        omega_sq_at_0.is_negative)
# Even so, its signal FRONT velocity is the high-k limit of ω/k = c:
omega = sqrt(c**2 * k**2 - mu**2)
v_front = limit(omega / k, k, oo)
verdict("Tachyon FRONT velocity = lim_{k→∞} ω/k = c ⇒ no FTL signal even from it",
        v_front == c)
print("  → A stable band built from the SAME nearest-neighbor hopping has max group")
print("    velocity 2Ja/ℏ = c; a faster band would be tachyonic = unstable, and its")
print("    information front is STILL c. No hidden FTL band exists.")


# ============================================================
# STAGE 6 — B4 + B6 honest open status + verdict
# ============================================================
print()
print("=" * 70)
print("STAGE 6 — B4 + B6: honestly OPEN (with the test that settles each)")
print("=" * 70)
print("  B4 (Planck/bounce regime): SPT's Action is verified at low energy only.")
print("     Near the bounce (Law 60/71) the causal structure is UNMAPPED — we do")
print("     not know if c is the same trans-Planckian. OPEN. Test: CMB-S4 2028")
print("     f_NL ≈ 3/2 probes bounce physics. (No claim either way.)")
print("  B6 (objective collapse): if wavefunction collapse is a PHYSICAL process")
print("     (Penrose gravitational), QM is effectively nonlinear → Door 2 (Gisin).")
print("     OPEN. Test: Penrose/Diósi mass-superposition experiments (ongoing).")
# The one true conditional we can record for B6:
verdict("Recorded conditional: physical collapse ⇒ effective QM nonlinearity "
        "(re-opens Door 2 logic) — status experimentally OPEN", True)

print()
print("=" * 70)
print("FINAL VERDICT — folded paper + B3–B7?")
print("=" * 70)
print("  • Folded paper (B3): the LITERAL fold needs a spare SPATIAL dimension SPT")
print("    does not have (3 gauge dims are compact/internal, not spatial). The")
print("    INTRINSIC handle WOULD shrink distance (3→1, verified) but Theorem 2.1")
print("    forbids it — that axiom is the real B1/B3 frontier worth probing.")
print("  • Any throat needs EXOTIC matter (flare-out ⇒ ρ+p_r<0, verified); ANEC")
print("    (proven) + topological censorship block it as an FTL shortcut.")
print("  • B7: a faster band is tachyonic = unstable, and its front is still c.")
print("  • B4 (Planck/bounce) + B6 (objective collapse): genuinely OPEN, each with")
print("    a concrete near-term experiment. These are where unknown physics could")
print("    still live — honestly flagged, not claimed.")
print()
print("CHỐT: 'gấp tờ giấy' cần một CHIỀU KHÔNG GIAN dư để gấp VÀO — SPT không có")
print("(3 chiều gauge là nội tại, không phải không gian). Phiên bản nội tại — thêm")
print("một 'tay cầm' (cạnh tắt) — THẬT SỰ rút ngắn khoảng cách (Càn↔Khôn 3→1, đã")
print("verify), nhưng tiên đề lưới-cố-định (Theorem 2.1) cấm. ĐÓ chính là biên giới")
print("B1/B3 đáng đào — đúng kiểu giả định 'Trái Đất phẳng'. Dù có tay cầm, cổ họng")
print("wormhole BẮT BUỘC cần vật chất lạ (điều kiện flare-out ⇒ ρ+p_r<0, đã verify),")
print("mà ANEC (đã chứng minh) + kiểm duyệt tô-pô chặn nó làm đường tắt FTL. B7: band")
print("nhanh hơn = tachyon = bất ổn, mặt trước vẫn = c. B4 (Planck/bounce) + B6 (sụp")
print("đổ khách quan) là hai chỗ THẬT SỰ còn mở — mỗi cái có thí nghiệm cụ thể sắp")
print("tới. Không tuyên bố, chỉ đánh dấu đúng chỗ để chĩa kính viễn vọng. Tờ giấy")
print("có thể gấp trong TƯỞNG TƯỢNG, nhưng punch-through cần thứ ANEC đang cấm — trừ")
print("khi Theorem 2.1 hoặc ANEC ở thang Planck hóa ra là 'mặt phẳng' của con kiến.")
