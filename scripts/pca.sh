#!/bin/bash

input="../results/plink/merged"
variants="../results/plink/ld_pruned.prune.in"
output="../results/plink/pca"

plink \
  --bfile "$input" \
  --extract "$variants" \
  --pca 20 \
  --out "$output"
