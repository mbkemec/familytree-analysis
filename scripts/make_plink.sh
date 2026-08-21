#!/bin/bash

input="../results/plink/sample"
output="../results/plink/sample"

plink2 \
  --pedmap "$input" \
  --make-pgen \
  --out "$output"
