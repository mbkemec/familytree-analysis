#!/bin/bash

input="../results/plink/sample"
output="../results/plink/sample"

plink \
  --file "$input" \
  --make-bed \
  --out "$output"
