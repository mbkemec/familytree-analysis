#!/bin/bash

input="../results/aadr/aadr_merged"
variants="../results/aadr/aadr_ld_pruned.prune.in"
output="../results/aadr/aadr_pca"

plink \
  --bfile "$input" \
  --extract "$variants" \
  --allow-no-sex \
  --pca 20 \
  --out "$output"
