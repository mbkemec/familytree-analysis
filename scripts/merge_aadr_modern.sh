#!/bin/bash

aadr="../results/aadr/aadr_modern_clean"
sample="../results/aadr/sample_aadr_clean"
output="../results/aadr/aadr_merged"

plink \
  --bfile "$aadr" \
  --bmerge "$sample" \
  --allow-no-sex \
  --make-bed \
  --out "$output"
