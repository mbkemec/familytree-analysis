#!/usr/bin/env bash

set -euo pipefail

INPUT="../results/aadr/aadr_ancient_merged"
PRUNE="../results/aadr/aadr_ancient_ld_pruned.prune.in"
OUTPUT="../results/aadr/aadr_ancient_pca"

echo "Running PCA on AADR ancient + FTDNA dataset..."
echo

plink \
    --bfile "${INPUT}" \
    --extract "${PRUNE}" \
    --pca 20 \
    --allow-no-sex \
    --out "${OUTPUT}"


echo "Ancient PCA summary"

echo -n "Individuals: "
wc -l < "${OUTPUT}.eigenvec"

echo -n "PCs        : "
wc -l < "${OUTPUT}.eigenval"

echo
echo "FTDNA sample:"
grep "SAMPLE1" "${OUTPUT}.eigenvec" || true

echo
echo "Eigenvalues:"
head -10 "${OUTPUT}.eigenval"

echo
echo "PCA complete."
