#!/bin/bash

variants="../results/aadr/aadr_final_variants.snplist"

aadr="../results/aadr/aadr_modern"
sample="../results/plink/sample_clean"

out="../results/aadr"

plink \
  --bfile "$aadr" \
  --extract "$variants" \
  --make-bed \
  --out "$out/aadr_modern_clean"

plink2 \
  --pfile "$sample" \
  --extract "$variants" \
  --make-bed \
  --out "$out/sample_aadr_clean"
