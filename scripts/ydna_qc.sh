#!/bin/bash

file="../data/y_dna"
output="../results/qc/y_dna_qc.txt"

mkdir -p ../results/qc

total=$(awk 'END {print NR-1}' "$file")

valid=$(awk -F, 'NR>1 && $4!="--" {count++} END {print count}' "$file")

missing=$(awk -F, 'NR>1 && $4=="--" {count++} END {print count}' "$file")

rsid=$(awk -F, 'NR>1 && $1 ~ /^rs/ {count++} END {print count}' "$file")

named=$(awk -F, 'NR>1 && $1 !~ /^rs/ {count++} END {print count}' "$file")

missing_rate=$(awk -v m="$missing" -v t="$total" 'BEGIN {printf "%.2f", (m/t)*100}')

valid_rate=$(awk -v v="$valid" -v t="$total" 'BEGIN {printf "%.2f", (v/t)*100}')

{
    	echo "Y-DNA QC"
    	echo "Total markers: $total"
    	echo "Valid genotypes: $valid"
    	echo "Missing genotypes: $missing"
    	echo "Valid genotype rate: $valid_rate%"
    	echo "Missing genotype rate: $missing_rate%"
    	echo "rsID markers: $rsid"
    	echo "Named Y markers: $named"

    	echo
    	echo "Genotype distribution"
    	awk -F, 'NR>1 {count[$4]++} END {for (gt in count) print gt, count[gt]}' "$file" | sort -k2 -nr

    	echo
	echo "Duplicate marker names"
	awk -F, 'NR>1 {count[$1]++} END {for (id in count) if (count[id] > 1) print id, count[id]}' "$file" | sort -k2 -nr | head

	echo
	echo "Duplicate positions"
	awk -F, 'NR>1 {count[$3]++} END {for (pos in count) if (count[pos] > 1) print pos, count[pos]}' "$file" | sort -k2 -nr | head

} | tee "$output"
