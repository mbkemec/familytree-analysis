#!/usr/bin/env bash

set -euo pipefail

# Filter selected ancient samples from the full AADR dataset

AADR_MASTER="../results/aadr/aadr_master"
KEEP_FILE="../results/aadr/selected_ancient_samples.keep"
OUTPUT="../results/aadr/aadr_ancient"

echo "Filtering selected ancient AADR samples..."
echo
echo "Input dataset : ${AADR_MASTER}"
echo "Keep file     : ${KEEP_FILE}"
echo "Output prefix : ${OUTPUT}"
echo

# Check required files
for file in \
    "${AADR_MASTER}.bed" \
    "${AADR_MASTER}.bim" \
    "${AADR_MASTER}.fam" \
    "${KEEP_FILE}"
do
    if [[ ! -f "$file" ]]; then
        echo "ERROR: Required file not found: $file"
        exit 1
    fi
done

# Extract selected ancient individuals
plink \
    --bfile "${AADR_MASTER}" \
    --keep "${KEEP_FILE}" \
    --allow-no-sex \
    --make-bed \
    --out "${OUTPUT}"

echo "AADR ancient subset created"

echo "Samples:"
wc -l "${OUTPUT}.fam"

echo
echo "Variants:"
wc -l "${OUTPUT}.bim"

echo
echo "Output files:"
ls -lh \
    "${OUTPUT}.bed" \
    "${OUTPUT}.bim" \
    "${OUTPUT}.fam"

echo "Ancient subset filtering complete."
