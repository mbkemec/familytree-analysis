#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import pandas as pd


# Configuration

PCA_FILE = Path("../results/aadr/aadr_ancient_pca.eigenvec")
META_FILE = Path("../results/aadr/selected_ancient_samples.tsv")
OUTDIR = Path("../results/aadr")

TARGET = "SAMPLE1"
N_PCS = 10
TOP_N = 30
GROUP_TOP_N = 30
K_NEAREST = 5


# Load PCA

print("AADR ancient PCA distance analysis")

pc_columns = [f"PC{i}" for i in range(1, 21)]

pca = pd.read_csv(
    PCA_FILE,
    sep=r"\s+",
    header=None,
    names=["FID", "IID"] + pc_columns
)

print(f"PCA samples loaded: {len(pca)}")

if TARGET not in set(pca["IID"]):
    raise RuntimeError(f"Target sample '{TARGET}' not found in PCA file.")

target = pca.loc[pca["IID"] == TARGET].iloc[0]
references = pca.loc[pca["IID"] != TARGET].copy()

print(f"Target sample: {TARGET}")
print(f"Ancient PCA references: {len(references)}")


# Load metadata

meta = pd.read_csv(
    META_FILE,
    sep="\t",
    dtype=str
)

print(f"Metadata rows loaded: {len(meta)}")


# Detect Genetic ID column

genetic_id_candidates = [
    "Genetic ID",
    "Genetic_ID",
    "GeneticID",
    "IID"
]

genetic_id_col = None

for col in genetic_id_candidates:
    if col in meta.columns:
        genetic_id_col = col
        break

if genetic_id_col is None:
    matches = [
        col for col in meta.columns
        if col.startswith("Genetic ID")
    ]

    if matches:
        genetic_id_col = matches[0]

if genetic_id_col is None:
    raise RuntimeError(
        "Could not identify Genetic ID column in metadata."
    )

print(f"Genetic ID column detected: {genetic_id_col}")


# Merge PCA coordinates with metadata

merged = references.merge(
    meta,
    left_on="IID",
    right_on=genetic_id_col,
    how="left"
)

matched = merged[genetic_id_col].notna().sum()
unmatched = len(merged) - matched

print(f"Metadata matches: {matched}")
print(f"Metadata unmatched: {unmatched}")

if unmatched:
    print("PCA samples without metadata:")
    print(
        merged.loc[
            merged[genetic_id_col].isna(),
            "IID"
        ].head(20).to_string(index=False)
    )


# Calculate PCA distance

pcs_used = [f"PC{i}" for i in range(1, N_PCS + 1)]

target_vector = target[pcs_used].to_numpy(dtype=float)
reference_matrix = merged[pcs_used].to_numpy(dtype=float)

merged["PCA_distance"] = np.sqrt(
    np.sum(
        (reference_matrix - target_vector) ** 2,
        axis=1
    )
)

merged = merged.sort_values("PCA_distance").reset_index(drop=True)
merged["rank"] = np.arange(1, len(merged) + 1)


# Helper for metadata columns

def find_column(candidates):
    for candidate in candidates:
        if candidate in merged.columns:
            return candidate

    for col in merged.columns:
        for candidate in candidates:
            if col.startswith(candidate):
                return col

    return None


group_col = find_column([
    "Group ID",
    "Group_ID"
])

locality_col = find_column([
    "Locality"
])

political_col = find_column([
    "Political Entity",
    "Political_Entity"
])

date_mean_col = find_column([
    "Date mean in BP",
    "Date_mean_BP"
])

full_date_col = find_column([
    "Full Date",
    "Full_Date"
])

region_col = find_column([
    "Analysis_region",
    "Analysis Region"
])

individual_col = find_column([
    "Individual ID",
    "Individual_ID"
])


# Convert BP to approximate BCE/CE

def bp_to_calendar(value):
    try:
        bp = float(value)
    except (TypeError, ValueError):
        return "Unknown"

    year = 1950 - bp

    if year < 0:
        return f"~{abs(int(round(year)))} BCE"

    return f"~{int(round(year))} CE"


if date_mean_col is not None:
    merged["Approx_calendar_date"] = (
        merged[date_mean_col].apply(bp_to_calendar)
    )
else:
    merged["Approx_calendar_date"] = "Unknown"


# Select useful output columns

display_columns = [
    "rank",
    "IID",
    "PCA_distance"
]

optional_columns = [
    individual_col,
    group_col,
    locality_col,
    political_col,
    date_mean_col,
    "Approx_calendar_date",
    full_date_col,
    region_col
]

for col in optional_columns:
    if col is not None and col not in display_columns:
        display_columns.append(col)


# Nearest ancient individuals

nearest = merged.head(TOP_N)[display_columns].copy()

nearest_file = OUTDIR / "aadr_ancient_pca_nearest_individuals.tsv"

nearest.to_csv(
    nearest_file,
    sep="\t",
    index=False
)

print()
print(f"Top {TOP_N} nearest ancient individuals:")
print(nearest.head(20).to_string(index=False))


# Group-level analysis

group_results = None
group_file = None

if group_col is not None:

    group_rows = []

    for group, group_df in merged.groupby(group_col):

        group_df = group_df.sort_values("PCA_distance")
        k = min(K_NEAREST, len(group_df))
        closest = group_df.iloc[:k]

        group_rows.append({
            "Group_ID": group,
            "n_samples": len(group_df),
            "k_used": k,
            "nearest_distance":
                group_df["PCA_distance"].iloc[0],
            "mean_k_nearest_distance":
                closest["PCA_distance"].mean(),
            "median_k_nearest_distance":
                closest["PCA_distance"].median(),
            "mean_group_distance":
                group_df["PCA_distance"].mean()
        })

    group_results = pd.DataFrame(group_rows)

    group_results = group_results.sort_values(
        [
            "mean_k_nearest_distance",
            "nearest_distance"
        ]
    ).reset_index(drop=True)

    group_results.insert(
        0,
        "rank",
        np.arange(1, len(group_results) + 1)
    )

    group_file = OUTDIR / "aadr_ancient_pca_nearest_groups.tsv"

    group_results.to_csv(
        group_file,
        sep="\t",
        index=False
    )

    print()
    print(f"Top {GROUP_TOP_N} nearest AADR groups:")
    print(
        group_results
        .head(GROUP_TOP_N)
        .to_string(index=False)
    )

else:
    print("Warning: Group ID column not found.")


# Region counts among top 100

region_file = None

if region_col is not None:

    region_counts = (
        merged
        .head(100)[region_col]
        .value_counts()
        .rename_axis("Analysis_region")
        .reset_index(name="count")
    )

    region_counts["fraction"] = (
        region_counts["count"]
        / region_counts["count"].sum()
    )

    region_file = (
        OUTDIR /
        "aadr_ancient_pca_top100_region_counts.tsv"
    )

    region_counts.to_csv(
        region_file,
        sep="\t",
        index=False
    )

    print()
    print("Regions among top 100 ancient neighbors:")
    print(region_counts.to_string(index=False))


# Date distribution among top 100

if date_mean_col is not None:

    nearest_dates = pd.to_numeric(
        merged.head(100)[date_mean_col],
        errors="coerce"
    ).dropna()

    if len(nearest_dates):

        oldest_bp = nearest_dates.max()
        median_bp = nearest_dates.median()
        youngest_bp = nearest_dates.min()

        def format_bp(bp):
            year = 1950 - bp

            if year < 0:
                return f"{bp:.0f} BP (~{abs(int(year))} BCE)"

            return f"{bp:.0f} BP (~{int(year)} CE)"

        print()
        print("Dates among top 100 ancient neighbors:")
        print(f"Oldest : {format_bp(oldest_bp)}")
        print(f"Median : {format_bp(median_bp)}")
        print(f"Youngest: {format_bp(youngest_bp)}")


# Save complete annotated table

full_file = OUTDIR / "aadr_ancient_pca_annotated.tsv"

merged.to_csv(
    full_file,
    sep="\t",
    index=False
)


# Final summary

print()
print("Output files:")
print(nearest_file)

if group_file is not None:
    print(group_file)

if region_file is not None:
    print(region_file)

print(full_file)

print()
print("Analysis complete.")
