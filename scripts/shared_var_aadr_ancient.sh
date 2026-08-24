#!/usr/bin/env bash

set -euo pipefail

SAMPLE="../results/plink/sample_clean"
AADR="../results/aadr/aadr_ancient"
OUTDIR="../results/aadr"

echo "Finding shared variants between FTDNA sample and AADR ancient panel!"

# 1. Write FTDNA variant IDs

plink2 \
    --pfile "${SAMPLE}" \
    --write-snplist \
    --out "${OUTDIR}/sample_variants_ancient"


# 2. Find variants also present in ancient AADR panel

plink \
    --bfile "${AADR}" \
    --extract "${OUTDIR}/sample_variants_ancient.snplist" \
    --write-snplist \
    --allow-no-sex \
    --out "${OUTDIR}/shared_variants_ancient"

echo "Shared variant summary"

echo "FTDNA variants:"
wc -l "${OUTDIR}/sample_variants_ancient.snplist"

echo
echo "Shared AADR ancient variants:"
wc -l "${OUTDIR}/shared_variants_ancient.snplist"

echo
echo "Shared variant detection complete."
