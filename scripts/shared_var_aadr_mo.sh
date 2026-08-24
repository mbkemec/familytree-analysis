#!/bin/bash

sample="../results/plink/sample_clean"
aadr="../results/aadr/aadr_modern"
out="../results/aadr"

# Write FTDNA sample variant IDs
plink2 \
  --pfile "$sample" \
  --write-snplist \
  --out "$out/sample_variants"

# Keep only AADR variants shared with the FTDNA sample
plink \
  --bfile "$aadr" \
  --extract "$out/sample_variants.snplist" \
  --write-snplist \
  --out "$out/shared_variants"

echo
echo "FTDNA variants:"
wc -l "$out/sample_variants.snplist"

echo "Shared AADR variants:"
wc -l "$out/shared_variants.snplist"
