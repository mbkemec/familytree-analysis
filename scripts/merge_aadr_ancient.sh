#!/usr/bin/env bash

set -euo pipefail

AADR="../results/aadr/aadr_ancient_clean"
SAMPLE="../results/aadr/sample_aadr_ancient_clean"
OUT="../results/aadr/aadr_ancient_merged"

echo "Merging FTDNA sample with AADR ancient reference panel..."
echo

plink \
    --bfile "${AADR}" \
    --bmerge "${SAMPLE}" \
    --allow-no-sex \
    --make-bed \
    --out "${OUT}"

echo "Ancient merge summary"

echo -n "Individuals: "
wc -l < "${OUT}.fam"

echo -n "Variants   : "
wc -l < "${OUT}.bim"

echo
echo "Expected:"
echo "  Individuals: 1277"
echo "  Variants   : 20900"

echo
echo "FTDNA sample:"
grep "SAMPLE1" "${OUT}.fam" || true

echo
echo "Ancient AADR + FTDNA merge complete."
