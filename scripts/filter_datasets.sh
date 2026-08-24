#!/bin/bash

variants="../results/plink/clean_variants.snplist"

sample="../results/plink/sample"
ref="../reference/1kg/all_phase3"

sample_out="../results/plink/sample_clean"
ref_out="../results/plink/1kg_clean"

plink2 \
  --pfile "$sample" \
  --extract "$variants" \
  --make-pgen \
  --out "$sample_out"

plink2 \
  --pfile "$ref" vzs \
  --extract "$variants" \
  --make-pgen \
  --out "$ref_out"
