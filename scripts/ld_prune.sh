#!/bin/bash

input="../results/plink/merged"
output="../results/plink/ld_pruned"

plink \
  --bfile "$input" \
  --indep-pairwise 50 5 0.2 \
  --out "$output"
