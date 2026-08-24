#!/usr/bin/env bash

set -euo pipefail

INPUT="../results/aadr/aadr_ancient_merged"
OUTPUT="../results/aadr/aadr_ancient_ld_pruned"

echo "LD pruning AADR ancient + FTDNA dataset..."
echo

plink \
    --bfile "${INPUT}" \
    --indep-pairwise 50 5 0.2 \
    --allow-no-sex \
    --out "${OUTPUT}"


echo "Ancient LD pruning summary"

TOTAL=$(wc -l < "${INPUT}.bim")
KEPT=$(wc -l < "${OUTPUT}.prune.in")
REMOVED=$(wc -l < "${OUTPUT}.prune.out")

echo "Starting variants : ${TOTAL}"
echo "Variants retained : ${KEPT}"
echo "Variants removed  : ${REMOVED}"

echo
echo "Output:"
echo "${OUTPUT}.prune.in"

echo
echo "LD pruning complete."
