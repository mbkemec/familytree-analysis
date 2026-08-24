#!/bin/bash

input="../results/aadr/aadr_merged"
output="../results/aadr/aadr_ld_pruned"

plink \
  --bfile "$input" \
  --indep-pairwise 50 5 0.2 \
  --allow-no-sex \
  --out "$output"
