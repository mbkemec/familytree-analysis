#!/bin/bash

input="../results/plink/sample"

plink2 \
  --pfile "$input" \
  --missing \
  --out ../results/plink/missingness

