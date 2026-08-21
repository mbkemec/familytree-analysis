#!/bin/bash

input="../reference/1kg/all_phase3.pgen.zst"
output="../reference/1kg/all_phase3.pgen"

plink2 --zst-decompress "$input" "$output"
