#!/bin/bash

file="../data/snp_results.csv"
output="../results/qc/snp_results_qc.txt"

mkdir -p ../results/qc

total=$(awk 'END {print NR-1}' "$file")

positive=$(awk -F, 'NR>1 {
    gsub(/\r/, "", $2)
    if ($2=="Positive") count++
}
END {print count}' "$file")

negative=$(awk -F, 'NR>1 {
    gsub(/\r/, "", $2)
    if ($2=="Negative") count++
}
END {print count}' "$file")

{
    echo "SNP Results QC"
    echo "Total markers: $total"
    echo "Positive markers: $positive"
    echo "Negative markers: $negative"

    echo
    echo "Test type distribution"
    awk -F, 'NR>1 {
        gsub(/\r/, "", $3)
        count[$3]++
    }
    END {
        for (type in count)
            print type, count[type]
    }' "$file" | sort -k3 -nr

    echo
    echo "Result distribution"
    awk -F, 'NR>1 {
        gsub(/\r/, "", $2)
        count[$2]++
    }
    END {
        for (result in count)
            print result, count[result]
    }' "$file" | sort -k2 -nr

    echo
    echo "Duplicate marker names"
    awk -F, 'NR>1 {
        gsub(/\r/, "", $1)
        count[$1]++
    }
    END {
        for (snp in count)
            if (count[snp] > 1)
                print snp, count[snp]
    }' "$file" | sort -k2 -nr

} | tee "$output"
