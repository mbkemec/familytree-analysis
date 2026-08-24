#!/usr/bin/env bash

set -euo pipefail

AADR="../results/aadr/aadr_ancient"
SHARED="../results/aadr/shared_variants_ancient.snplist"
OUT="../results/aadr/aadr_ancient_missingness"

echo "Inspecting missingness of shared SNPs in AADR ancient panel..."
echo

plink \
    --bfile "${AADR}" \
    --extract "${SHARED}" \
    --missing \
    --allow-no-sex \
    --out "${OUT}"


echo "Ancient SNP missingness summary"

python3 - <<'PY'
import pandas as pd

path = "../results/aadr/aadr_ancient_missingness.lmiss"

df = pd.read_csv(path, sep=r"\s+")

print(f"Variants analysed: {len(df)}")
print()

print("Missingness distribution:")
print(df["F_MISS"].describe(percentiles=[
    0.10,
    0.25,
    0.50,
    0.75,
    0.90,
    0.95,
    0.99
]).to_string())

print("Variants retained at different call-rate thresholds")

thresholds = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]

for call_rate in thresholds:
    max_missing = 1 - call_rate
    n = (df["F_MISS"] <= max_missing).sum()
    pct = n / len(df) * 100

    print(
        f"Call rate >= {call_rate:>4.0%}: "
        f"{n:>6} variants ({pct:5.1f}%)"
    )


print("Variants by number of ancient individuals genotyped")


n_samples = 1276

for minimum in [50, 100, 250, 500, 750, 1000, 1200]:
    observed = n_samples - df["N_MISS"]
    n = (observed >= minimum).sum()

    print(
        f"Genotyped in >= {minimum:4} individuals: "
        f"{n:>6} variants"
    )


print("Inspection complete.")
PY
