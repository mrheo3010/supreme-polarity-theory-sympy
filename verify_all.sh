#!/usr/bin/env bash
# Run every SPT SymPy verification script. Exits 0 if all PASS, 1 on first failure.
#
# Usage:
#   bash verify_all.sh              # run all
#   bash verify_all.sh -q           # quiet: only print failures
#
# Requires: python3 with sympy >= 1.12 (`pip install -r requirements.txt`)

set -euo pipefail

QUIET=0
if [[ "${1:-}" == "-q" || "${1:-}" == "--quiet" ]]; then
  QUIET=1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS=( "${SCRIPT_DIR}"/scripts/spt_*.py )
TOTAL=${#SCRIPTS[@]}
PASSED=0
FAILED=0

echo "[verify_all] Running ${TOTAL} SPT SymPy scripts..."
START=$(date +%s)

for f in "${SCRIPTS[@]}"; do
  NAME="$(basename "${f}")"
  if [[ ${QUIET} -eq 0 ]]; then
    echo "  → ${NAME}"
  fi
  if python3 "${f}" > /tmp/spt_verify.out 2>&1; then
    PASSED=$((PASSED + 1))
  else
    FAILED=$((FAILED + 1))
    echo "  ✗ ${NAME} FAILED"
    echo "    --- last 10 lines of output ---"
    tail -10 /tmp/spt_verify.out | sed 's/^/    /'
    echo "    --- end ---"
  fi
done

END=$(date +%s)
ELAPSED=$((END - START))

echo ""
echo "[verify_all] ${PASSED}/${TOTAL} PASSED · ${FAILED} FAILED · ${ELAPSED}s"
if [[ ${FAILED} -gt 0 ]]; then
  exit 1
fi
echo "[verify_all] All scripts PASS ✓"
