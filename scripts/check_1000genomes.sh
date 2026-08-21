#!/bin/bash

input="../reference/1kg/all_phase3"
output="../results/1kg_test"

plink2 \
  --pfile "$input" vzs \
  --freq \
  --out "$output"
