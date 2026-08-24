#!/bin/bash

sample="../results/plink/sample_clean"
ref="../results/plink/1kg_clean"
out="../results/plink"

# Convert clean datasets to PLINK 1 binary format

plink2 \
  --pfile "$sample" \
  --make-bed \
  --out "$out/sample_merge"

plink2 \
  --pfile "$ref" \
  --make-bed \
  --out "$out/1kg_merge"

# Merge sample with reference

plink \
  --bfile "$out/1kg_merge" \
  --bmerge "$out/sample_merge" \
  --make-bed \
  --out "$out/merged"
