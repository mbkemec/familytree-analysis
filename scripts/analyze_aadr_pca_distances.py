#!/usr/bin/env python3

from pathlib import Path
import sys

import numpy as np
import pandas as pd


INPUT_FILE = Path("../results/aadr/aadr_pca_populations.tsv")
OUTPUT_DIR = Path("../results/aadr")

TARGET_SAMPLE = "SAMPLE1"

# Number of principal components used for distance calculations.
# PC1-PC10 gives us substantially more information than a 2D PCA plot
# while avoiding excessive influence from very low-variance PCs.
N_PCS = 10

# Number of nearest individual AADR samples to report.
N_NEIGHBORS = 30

# Number of closest individuals within each population used for the
# robust population-distance estimate.
N_CLOSEST_PER_POP = 5


def euclidean_distance(a, b):
    """Calculate Euclidean distance between two vectors."""
    return np.linalg.norm(a - b)


def find_column(df, candidates):
    """Find a column using several possible names."""
    lower_map = {str(col).lower(): col for col in df.columns}

    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]

    return None


# Load PCA dataset

if not INPUT_FILE.exists():
    sys.exit(f"ERROR: Input file not found: {INPUT_FILE}")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE, sep="\t")

print("AADR PCA distance analysis")
print("=" * 60)
print(f"Input: {INPUT_FILE}")
print(f"Samples loaded: {len(df)}")


# Detect required columns

iid_col = find_column(df, ["IID", "iid", "sample", "sample_id"])
fid_col = find_column(df, ["FID", "fid"])
pop_col = find_column(df, ["Population", "population", "POP", "pop"])

if iid_col is None:
    sys.exit(
        "ERROR: Could not identify sample/IID column.\n"
        f"Available columns: {list(df.columns)}"
    )

if pop_col is None:
    sys.exit(
        "ERROR: Could not identify population column.\n"
        f"Available columns: {list(df.columns)}"
    )


# Select PCs

pc_columns = []

for i in range(1, N_PCS + 1):
    col = find_column(df, [f"PC{i}"])

    if col is None:
        sys.exit(
            f"ERROR: PC{i} not found.\n"
            f"Available columns: {list(df.columns)}"
        )

    pc_columns.append(col)

print(f"PCs used: {', '.join(pc_columns)}")


# Find target sample

target_rows = df[df[iid_col].astype(str) == TARGET_SAMPLE]

if len(target_rows) == 0:
    sys.exit(f"ERROR: Target sample '{TARGET_SAMPLE}' not found.")

if len(target_rows) > 1:
    sys.exit(f"ERROR: Multiple rows found for '{TARGET_SAMPLE}'.")

target = target_rows.iloc[0]

print(f"Target sample: {TARGET_SAMPLE}")
print(f"Target population label: {target[pop_col]}")


# Reference population

reference = df[df[iid_col].astype(str) != TARGET_SAMPLE].copy()

# Remove accidental FTDNA/sample pseudo-populations if present.
reference = reference[
    ~reference[pop_col].astype(str).str.upper().str.contains("FTDNA", na=False)
].copy()

# Ensure PCA values are numeric.
for pc in pc_columns:
    reference[pc] = pd.to_numeric(reference[pc], errors="coerce")

target_vector = pd.to_numeric(
    target[pc_columns],
    errors="coerce"
).to_numpy(dtype=float)

reference = reference.dropna(subset=pc_columns)

print(f"Reference samples: {len(reference)}")
print(f"Reference populations: {reference[pop_col].nunique()}")


# 1. Individual nearest-neighbour analysis

reference_matrix = reference[pc_columns].to_numpy(dtype=float)

reference["distance"] = np.linalg.norm(
    reference_matrix - target_vector,
    axis=1
)

nearest = (
    reference
    .sort_values("distance")
    .head(N_NEIGHBORS)
    .copy()
)

nearest.insert(
    0,
    "rank",
    range(1, len(nearest) + 1)
)

nearest_columns = ["rank"]

if fid_col is not None:
    nearest_columns.append(fid_col)

nearest_columns += [
    iid_col,
    pop_col,
    "distance"
]

nearest_columns += pc_columns

nearest_output = nearest[nearest_columns]

nearest_file = OUTPUT_DIR / "aadr_pca_nearest_individuals.tsv"

nearest_output.to_csv(
    nearest_file,
    sep="\t",
    index=False
)


# 2. Population centroid analysis

centroid_rows = []

for population, group in reference.groupby(pop_col):

    centroid = group[pc_columns].mean().to_numpy(dtype=float)

    distance = euclidean_distance(
        target_vector,
        centroid
    )

    row = {
        "population": population,
        "n_samples": len(group),
        "centroid_distance": distance,
    }

    for i, value in enumerate(centroid, start=1):
        row[f"centroid_PC{i}"] = value

    centroid_rows.append(row)


centroids = pd.DataFrame(centroid_rows)

centroids = centroids.sort_values(
    "centroid_distance"
).reset_index(drop=True)

centroids.insert(
    0,
    "rank",
    range(1, len(centroids) + 1)
)

centroid_file = OUTPUT_DIR / "aadr_pca_population_centroids.tsv"

centroids.to_csv(
    centroid_file,
    sep="\t",
    index=False
)


# 3. Robust population proximity analysis

robust_rows = []

for population, group in reference.groupby(pop_col):

    distances = np.sort(
        group["distance"].to_numpy(dtype=float)
    )

    k = min(
        N_CLOSEST_PER_POP,
        len(distances)
    )

    closest = distances[:k]

    robust_rows.append({
        "population": population,
        "n_samples": len(group),
        "k_used": k,
        "nearest_distance": distances[0],
        "mean_k_nearest_distance": closest.mean(),
        "median_k_nearest_distance": np.median(closest),
        "population_median_distance": np.median(distances),
    })


robust = pd.DataFrame(robust_rows)

robust = robust.sort_values(
    [
        "mean_k_nearest_distance",
        "median_k_nearest_distance"
    ]
).reset_index(drop=True)

robust.insert(
    0,
    "rank",
    range(1, len(robust) + 1)
)

robust_file = OUTPUT_DIR / "aadr_pca_population_proximity.tsv"

robust.to_csv(
    robust_file,
    sep="\t",
    index=False
)


# Console summary

print()
print("=" * 60)
print("TOP 15 NEAREST INDIVIDUALS")
print("=" * 60)

display_cols = [iid_col, pop_col, "distance"]

print(
    nearest[display_cols]
    .head(15)
    .to_string(index=False)
)


print()
print("=" * 60)
print("TOP 15 POPULATION CENTROIDS")
print("=" * 60)

print(
    centroids[
        [
            "rank",
            "population",
            "n_samples",
            "centroid_distance"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print()
print("=" * 60)
print(
    f"TOP 15 POPULATIONS "
    f"(mean distance of closest {N_CLOSEST_PER_POP} samples)"
)
print("=" * 60)

print(
    robust[
        [
            "rank",
            "population",
            "n_samples",
            "k_used",
            "nearest_distance",
            "mean_k_nearest_distance",
            "median_k_nearest_distance"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


# Population counts among nearest individuals

neighbor_counts = (
    nearest[pop_col]
    .value_counts()
    .rename_axis("population")
    .reset_index(name="count")
)

neighbor_counts["fraction"] = (
    neighbor_counts["count"] / len(nearest)
)

neighbor_counts_file = (
    OUTPUT_DIR / "aadr_pca_nearest_population_counts.tsv"
)

neighbor_counts.to_csv(
    neighbor_counts_file,
    sep="\t",
    index=False
)


print()
print("=" * 60)
print(f"POPULATION COUNTS AMONG TOP {N_NEIGHBORS} NEIGHBORS")
print("=" * 60)

print(
    neighbor_counts.to_string(index=False)
)


# Output summary

print()
print("=" * 60)
print("OUTPUT FILES")
print("=" * 60)

print(nearest_file)
print(centroid_file)
print(robust_file)
print(neighbor_counts_file)

print()
print("Analysis complete.")
