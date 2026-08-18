#!/bin/bash

echo "1. File types"
file ../data/autosomal.csv ../data/y_dna ../data/snp_results.csv

echo
echo "2. Line counts"
wc -l ../data/autosomal.csv ../data/y_dna ../data/snp_results.csv

echo
echo "3. Autosomal data"
head -n 5 ../data/autosomal.csv

echo
echo "4. Y-DNA data"
head -n 5 ../data/y_dna

echo
echo "5. SNP results"
head -n 5 ../data/snp_results.csv
