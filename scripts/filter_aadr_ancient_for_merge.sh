#!/usr/bin/env bash

set -euo pipefail

AADR="../results/aadr/aadr_ancient"
SAMPLE="../results/plink/sample_clean"

# This list was already validated against the AADR marker definitions:
# - matching chromosome/position
# - compatible alleles
# - non-missing genotype in the FTDNA sample
BASE_VARIANTS="../results/aadr/aadr_final_variants.snplist"

OUTDIR="../results/aadr"

MISSING_PREFIX="${OUTDIR}/aadr_ancient_final_missingness"
FINAL_VARIANTS="${OUTDIR}/aadr_ancient_final_variants.snplist"

AADR_OUT="${OUTDIR}/aadr_ancient_clean"
SAMPLE_OUT="${OUTDIR}/sample_aadr_ancient_clean"

echo "Preparing ancient AADR and FTDNA datasets for merge..."

plink \
    --bfile "${AADR}" \
    --extract "${BASE_VARIANTS}" \
    --missing \
    --allow-no-sex \
    --out "${MISSING_PREFIX}"

# 2. Retain SNPs with >= 50% call rate in ancient individuals
#
#    F_MISS <= 0.50

python3 - <<'PY'
import pandas as pd

input_file = "../results/aadr/aadr_ancient_final_missingness.lmiss"
output_file = "../results/aadr/aadr_ancient_final_variants.snplist"

df = pd.read_csv(input_file, sep=r"\s+")

selected = df.loc[df["F_MISS"] <= 0.50, "SNP"]

selected.to_csv(
    output_file,
    index=False,
    header=False
)

print("Ancient SNP call-rate filtering")
print(f"Starting variants : {len(df)}")
print(f"Retained variants : {len(selected)}")
print(f"Removed variants  : {len(df) - len(selected)}")
print(f"Minimum call rate : 50%")
print(f"Output             : {output_file}")
PY

# 3. Create clean ancient AADR dataset

echo "Creating clean ancient AADR dataset."

plink \
    --bfile "${AADR}" \
    --extract "${FINAL_VARIANTS}" \
    --make-bed \
    --allow-no-sex \
    --out "${AADR_OUT}"

# 4. Create matching FTDNA dataset

echo "Creating matching FTDNA dataset"

plink2 \
    --pfile "${SAMPLE}" \
    --extract "${FINAL_VARIANTS}" \
    --make-bed \
    --out "${SAMPLE_OUT}"

# 5. Validation


echo "Final datasets"

echo "Ancient AADR:"
echo -n "Samples : "
wc -l < "${AADR_OUT}.fam"
echo -n "Variants: "
wc -l < "${AADR_OUT}.bim"

echo "FTDNA:"
echo -n "Samples : "
wc -l < "${SAMPLE_OUT}.fam"
echo -n "Variants: "
wc -l < "${SAMPLE_OUT}.bim"

echo "Ancient AADR dataset preparation complete."
