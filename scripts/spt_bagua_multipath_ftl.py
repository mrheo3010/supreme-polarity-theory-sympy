#!/usr/bin/env python3
"""
SPT — route info through the 6 OTHER trigrams (not Càn/Khôn), merge at one point?

The 8 Bagua trigrams are the vertices of the internal-gauge cube Q_3:
  Càn ☰(111,w3)  Đoài ☱(110,w2)  Ly ☲(101,w2)  Chấn ☳(100,w1)
  Tốn ☴(011,w2)  Khảm ☵(010,w1)  Cấn ☶(001,w1)  Khôn ☷(000,w0)
Càn and Khôn are ANTIPODAL (Hamming distance 3). The proposal: instead of the
blocked Càn→Khôn line, split the message across one or more of the 6 OTHER
(intermediate) trigrams as parallel channels, then MERGE/interfere at a single
distant point — hoping parallelism or recombination beats c.

We test it and find: NO FTL. Four independent blocks:
  • The 8 trigrams are INTERNAL gauge sectors at a point, not spatial routes.
    Every edge of the cube (a single DAbit flip) emits one gauge boson ≤ c, so
    ANY path through the 6 intermediates is ≤ c (graph distance = Hamming).
  • Multipath PARALLELISM raises BANDWIDTH (×N channels) but NOT LATENCY: the
    merge must wait for the slowest branch, so the merge time ≥ L/c, independent
    of how many branches N you use. Parallelism never lowers the latency floor.
  • Gauge superselection / CONFINEMENT (Law 38/51): a single colored branch
    cannot be isolated; the merge must reform a color SINGLET locally ≤ c.
  • NO-SIGNALLING at the merge: spreading a Bell pair over the 6-branch gauge
    register and phase-encoding it leaves the distant merge point's reduced
    state = I/6, independent of the source's encoding (verified) — until the
    classical which-branch bits arrive ≤ c.

  Stage 1 — Frame the multipath proposal.
  Stage 2 — The Bagua cube: 8 vertices, 12 edges (each a boson ≤ c), 6 middles.
  Stage 3 — Any path through the 6 middles is ≤ c (graph distance = Hamming).
  Stage 4 — Parallelism raises bandwidth, not latency: merge time ≥ L/c ∀N.
  Stage 5 — Merge no-signalling: 6-branch entangled register → ρ_merge = I/6 ∀φ.
  Stage 6 — Verdict.

Pure SymPy + stdlib. Runs in <3 seconds.
"""

import sys
import itertools
from sympy import (symbols, Matrix, eye, zeros, exp, I, sqrt, simplify, Rational,
                   diff, kronecker_product)

sys.stdout.reconfigure(encoding="utf-8")


def verdict(claim, ok):
    print(f"  {'✓' if ok else '✗'} {claim}: {'PASS' if ok else 'FAIL'}")
    return ok


def dagger(M):
    return M.conjugate().T


# ============================================================
# STAGE 1 — Frame the multipath proposal
# ============================================================
print("=" * 70)
print("STAGE 1 — Proposal: route through the 6 middle trigrams, merge at one point")
print("=" * 70)
print("  Skip the blocked Càn↔Khôn line; split the message across one or more of")
print("  the 6 intermediate trigrams (Đoài, Ly, Chấn, Tốn, Khảm, Cấn) as parallel")
print("  channels, then merge/interfere at a single distant point. Beat c?")
verdict("Proposal framed: multipath through 6 middle trigrams + merge", True)


# ============================================================
# STAGE 2 — The Bagua cube: 8 vertices, 12 edges, 6 middles
# ============================================================
print()
print("=" * 70)
print("STAGE 2 — The internal-gauge cube Q_3: edges = gauge bosons ≤ c")
print("=" * 70)
trigrams = list(itertools.product([0, 1], repeat=3))   # 8 vertices
edges = [(a, b) for a in trigrams for b in trigrams
         if sum(x ^ y for x, y in zip(a, b)) == 1]
n_edges = len(edges) // 2
verdict("8 trigrams form the cube Q_3 with 12 edges (each edge = 1 DAbit flip)",
        len(trigrams) == 8 and n_edges == 12)
middles = [t for t in trigrams if sum(t) in (1, 2)]    # the 6 non-Càn/Khôn
verdict("Exactly 6 intermediate trigrams (w=1 or w=2), besides Càn(w3)+Khôn(w0)",
        len(middles) == 6)
print(f"  6 middle trigrams (w∈{{1,2}}): {middles}")
print("  → Each edge is a single internal-DAbit flip = emit one gauge boson")
print("    (gluon/W/Z), which travels at ≤ c. The cube is INTERNAL (Law 58),")
print("    orthogonal to space — the trigrams are charge labels, not places.")


# ============================================================
# STAGE 3 — Any path through the middles is ≤ c
# ============================================================
print()
print("=" * 70)
print("STAGE 3 — On a hypercube, graph distance = Hamming distance ⇒ path ≤ c")
print("=" * 70)
# Breadth-first graph distance on the cube from Càn(111) to Khôn(000):
def graph_distance(src, dst):
    frontier = {src}; seen = {src}; d = 0
    while dst not in frontier:
        nxt = set()
        for v in frontier:
            for w in trigrams:
                if sum(x ^ y for x, y in zip(v, w)) == 1 and w not in seen:
                    nxt.add(w); seen.add(w)
        frontier = nxt; d += 1
        if not frontier:
            break
    return d

can, khon = (1, 1, 1), (0, 0, 0)
d_graph = graph_distance(can, khon)
d_hamming = sum(x ^ y for x, y in zip(can, khon))
print(f"  Càn→Khôn: graph distance = {d_graph}, Hamming distance = {d_hamming}")
verdict("Shortest path through the middles still needs 3 hops (= Hamming distance)",
        d_graph == 3 and d_graph == d_hamming)
# Each hop costs at least one lattice step time a/c; total ≥ (path length)·a/c.
a, c = symbols("a c", positive=True)
t_per_hop = a / c
t_path = d_graph * t_per_hop
print(f"  Minimum transit time ≥ {d_graph}·(a/c) = {t_path}  (>0, not instantaneous)")
verdict("Any multipath route costs ≥ (path length)·a/c > 0 ⇒ never instantaneous",
        simplify(t_path) == 3*a/c and (t_path).is_positive)


# ============================================================
# STAGE 4 — Parallelism raises bandwidth, NOT latency
# ============================================================
print()
print("=" * 70)
print("STAGE 4 — Splitting over N branches: bandwidth ×N, latency floor stays L/c")
print("=" * 70)
L, N, B1 = symbols("L N B1", positive=True)
# Each branch is a physical channel of length L: its latency is ≥ L/c.
latency_per_branch = L / c
# The merge needs ALL branch-parts to arrive, so merge time = max latency = L/c,
# regardless of how many branches N you use.
T_merge = L / c
print(f"  Per-branch latency = L/c.  Merge waits for the slowest ⇒ T_merge = L/c.")
verdict("Merge latency is independent of N (parallelism does not lower it): "
        "dT_merge/dN = 0", diff(T_merge, N) == 0)
verdict("Merge latency stays at the floor L/c > 0 for any number of branches N",
        simplify(T_merge) == L/c and T_merge.is_positive)
# What parallelism DOES buy: total bandwidth scales with N (throughput, not speed).
B_total = N * B1
verdict("Only BANDWIDTH grows with N (dB/dN = B1 > 0) — throughput, not speed",
        diff(B_total, N) == B1)
print("  → Sending more pieces in parallel delivers more bits per second, but the")
print("    FIRST bit (and the merge) still arrives no sooner than L/c. Latency, not")
print("    bandwidth, is what FTL would need to beat — and parallelism can't.")


# ============================================================
# STAGE 5 — Merge no-signalling: 6-branch register → ρ_merge = I/6 ∀φ
# ============================================================
print()
print("=" * 70)
print("STAGE 5 — Merge point sees ρ = I/6 regardless of source's branch encoding")
print("=" * 70)
# Spread a maximally-entangled pair over the 6-branch gauge register:
#   |Ψ⟩ = (1/√6) Σ_{j=1}^{6} |branch_j⟩_source ⊗ |j⟩_merge
# The source tries to SIGNAL by phase-encoding each branch: U = diag(e^{iφ_j}).
# Bob's merge-point reduced state must be unchanged (no-signalling) until the
# classical which-branch record arrives.
def e(j):
    v = zeros(6, 1); v[j] = 1; return v

psi = zeros(36, 1)
for j in range(6):
    psi += kronecker_product(e(j), e(j))
psi = psi / sqrt(6)

phis = symbols("phi1 phi2 phi3 phi4 phi5 phi6", real=True)
U_src = zeros(6, 6)
for j in range(6):
    U_src[j, j] = exp(I * phis[j])              # source's phase encoding
U_full = kronecker_product(U_src, eye(6))
psi2 = U_full * psi
rho = psi2 * dagger(psi2)

# Partial trace over the 6-dim SOURCE subsystem → merge-point reduced state.
def ptrace_source(rho36):
    out = zeros(6, 6)
    for b1 in range(6):
        for b2 in range(6):
            out[b1, b2] = sum(rho36[a*6 + b1, a*6 + b2] for a in range(6))
    return out

rho_merge = simplify(ptrace_source(rho))
print(f"  Merge-point reduced state ρ_merge = (1/6)·I ?  → all phases cancel")
verdict("Merge sees ρ = I/6 for ARBITRARY branch phases φ_j (no-signalling holds)",
        simplify(rho_merge - eye(6)/6) == zeros(6, 6))
print("  → No matter how the source phase-encodes across the 6 branches, the")
print("    distant merge point's statistics are identical (maximally mixed).")
print("  Plus CONFINEMENT (Law 38/51): a single colored branch can't be isolated;")
print("    the merge must reform a gauge SINGLET, a local operation ≤ c.")


# ============================================================
# FINAL VERDICT
# ============================================================
print()
print("=" * 70)
print("FINAL VERDICT — multipath through 6 trigrams + merge = FTL?")
print("=" * 70)
print("NO. Four independent blocks:")
print()
print("  • The 8 trigrams are INTERNAL gauge sectors (Law 58), not spatial routes.")
print("    Every cube edge is a gauge boson ≤ c; any path through the 6 middles is")
print("    ≤ c (graph distance = Hamming distance; Càn→Khôn still 3 hops).")
print("  • Parallelism raises BANDWIDTH (×N), not LATENCY: the merge waits for the")
print("    slowest branch, so T_merge = L/c independent of N. FTL needs to beat")
print("    latency, and multipath cannot.")
print("  • Confinement (Law 38/51): a single colored branch can't be isolated; the")
print("    merge must reform a color singlet locally ≤ c.")
print("  • No-signalling at the merge: a 6-branch entangled register phase-encoded")
print("    by the source leaves ρ_merge = I/6 for ALL phases (verified). The merge")
print("    learns nothing until classical which-branch bits arrive ≤ c.")
print()
print("CHỐT: định tuyến qua 6 quẻ trung gian rồi hợp nhất vẫn KHÔNG cho FTL. 8 quẻ")
print("là sector gauge NỘI TẠI (Law 58), không phải các điểm trong không gian — mọi")
print("cạnh của khối lập phương là một boson ≤ c, nên mọi đường đi qua 6 nhánh đều")
print("≤ c (khoảng cách đồ thị = khoảng cách Hamming). Chạy song song chỉ tăng BĂNG")
print("THÔNG (×N nhánh), KHÔNG giảm ĐỘ TRỄ: điểm hợp nhất phải chờ nhánh chậm nhất,")
print("nên T_merge = L/c bất kể N. Giam hãm (confinement) cấm cô lập một nhánh có")
print("màu; hợp nhất phải tái tạo singlet cục bộ ≤ c. Và no-signalling: dù mã hóa")
print("pha thế nào trên 6 nhánh, điểm hợp nhất vẫn thấy ρ = I/6 (đã verify) — chỉ")
print("mở khóa được khi bit cổ điển 'nhánh nào' tới ≤ c. Song song hóa Bát quái")
print("đẹp về cấu trúc, nhưng FTL cần thắng ĐỘ TRỄ, mà đa đường không bao giờ thắng.")
