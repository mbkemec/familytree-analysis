#!/bin/bash

input="../results/aadr/aadr_master"
samples="../results/aadr/selected_samples.keep"
output="../results/aadr/aadr_modern"

plink \
  --bfile "$input" \
  --keep "$samples" \
  --make-bed \
  --out "$output"
