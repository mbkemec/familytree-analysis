#!/bin/bash

sample="../results/plink/sample"
ref="../reference/1kg/all_phase3"
out="../results/plink"

mkdir -p "$out"

# Write sample variant IDs
plink2 \
  --pfile "$sample" \
  --write-snplist allow-dups \
  --out "$out/sample_variants"

# Extract those IDs from 1000 Genomes
plink2 \
  --pfile "$ref" vzs \
  --extract "$out/sample_variants.snplist" \
  --write-snplist allow-dups \
  --make-just-pvar \
  --out "$out/shared_variants"

echo
echo "Sample variants:"
wc -l "$out/sample_variants.snplist"

echo "Shared variants:"
wc -l "$out/shared_variants.snplist"
