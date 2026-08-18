#!/bin/bash

file="../data/autosomal.csv"
mkdir -p ../results/qc
output="../results/qc/autosomal_qc.txt"


total=$(awk 'END {print NR-1}' "$file")

valid=$(awk -F, 'NR>1 && $4!="--" {count++} END {print count}' "$file")

missing=$(awk -F, 'NR>1 && $4=="--" {count++} END {print count}' "$file")

rsid=$(awk -F, 'NR>1 && $1 ~ /^rs/ {count++} END {print count}' "$file")

non_rsid=$(awk -F, 'NR>1 && $1 !~ /^rs/ {count++} END {print count}' "$file")

chr0=$(awk -F, 'NR>1 && $2=="0" {count++} END {print count}' "$file")

chr0_gt=$(awk -F, 'NR>1 && $2=="0" && $4!="--" {count++} END {print count}' "$file")

missing_rate=$(awk -v m="$missing" -v t="$total" 'BEGIN {printf "%.2f", (m/t)*100}')
valid_rate=$(awk -v v="$valid" -v t="$total" 'BEGIN {printf "%.2f", (v/t)*100}')
{
	echo "Autosomal QC"
	echo "Total markers: $total"
	echo "Valid genotypes: $valid"
	echo "Missing genotypes: $missing"
	echo "rsID markers: $rsid"
	echo "Non-rs markers: $non_rsid"
	echo "Chromosome 0 markers: $chr0"
	echo "Chromosome 0 with genotype: $chr0_gt"
	echo "Valid genotype rate: $valid_rate%"
	echo "Missing genotype rate: $missing_rate%"

	echo
	echo "Chromosome distribution"
	awk -F, 'NR>1 {count[$2]++} END {for (chr in count) print chr, count[chr]}' "$file" | sort -V

	echo
	echo "Genotype distribution"
	awk -F, 'NR>1 {count[$4]++} END {for (gt in count) print gt, count[gt]}' "$file" | sort -k2 -nr
} | tee "$output"
