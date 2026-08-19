#!/bin/bash

input="../results/plink/sample"

plink \
  --bfile "$input" \
  --missing \
  --out ../results/plink/missingness

plink \
  --bfile "$input" \
  --het \
  --out ../results/plink/heterozygosity
