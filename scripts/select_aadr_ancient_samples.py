#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import re


# ============================================================
# PATHS
# ============================================================

ANNO = Path(
    "../reference/aadr/v66.p1_compatibility_HO.aadr.PUB.anno"
)

FAM = Path(
    "../results/aadr/aadr_master.fam"
)

OUTDIR = Path("../results/aadr")
OUTDIR.mkdir(parents=True, exist_ok=True)

OUT_META = OUTDIR / "selected_ancient_samples.tsv"
OUT_KEEP = OUTDIR / "selected_ancient_samples.keep"
OUT_GROUPS = OUTDIR / "selected_ancient_groups.txt"


# ============================================================
# SETTINGS
# ============================================================

# AADR dates are expressed as years before 1950 CE.
#
# 300 BP ~= 1650 CE
# 12000 BP ~= beginning of the Holocene / late prehistoric range
#
# The goal here is to retain historical and prehistoric samples
# relevant to later ancestry analysis while excluding modern
# reference individuals and extremely deep Paleolithic samples.

MIN_DATE_BP = 300
MAX_DATE_BP = 12000


# Minimum number of SNPs available on the AADR
# Compatibility_HO SNP set.
#
# This is intentionally permissive at the selection stage.
# Further shared-variant filtering will be performed before PCA.

MIN_COMPAT_HO_SNPS = 10000


# Prevent large archaeological groups from dominating PCA.
#
# Selection is performed at the actual AADR Group_ID level,
# NOT at the broad Analysis_region level.
#
# Example:
#
# Turkey_N
# Turkey_EBA
# Turkey_MLBA
# Turkey_Medieval_Byzantine
#
# remain separate groups.

MAX_SAMPLES_PER_GROUP = 5


# ============================================================
# BROAD ANALYTICAL REGIONS
# ============================================================
#
# These labels are NOT used to collapse ancient populations.
#
# They are retained only as higher-level metadata for:
#
# - plotting
# - summaries
# - exploratory filtering
#
# The actual ancestry comparisons will use AADR Group_ID.

REGION_PATTERNS = {

    "Anatolia": [
        r"Turkey",
    ],

    "Iran": [
        r"Iran",
    ],

    "Iraq_Mesopotamia": [
        r"Iraq",
    ],

    "South_Caucasus": [
        r"Armenia",
        r"Georgia",
    ],

    "North_Caucasus": [
        r"Caucasus",
    ],

    "Central_Asia": [
        r"Kazakhstan",
        r"Kyrgyzstan",
        r"Uzbekistan",
        r"Turkmenistan",
        r"Tajikistan",
    ],

    "Steppe": [
        r"Yamnaya",
        r"Sintashta",
        r"Andronovo",
        r"Scyth",
        r"Sarmat",
        r"Saka",
        r"Kangju",
        r"Hunnic",
        r"Xiongnu",
    ],

    "Mongolia": [
        r"Mongolia",
    ],
}


# ============================================================
# REGION CLASSIFICATION FUNCTION
# ============================================================

def find_regions(text):

    matched = []

    for region, patterns in REGION_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                matched.append(region)
                break

    return ",".join(matched)


# ============================================================
# LOAD AADR ANNOTATION
# ============================================================

print("Loading AADR annotation...")

df = pd.read_csv(
    ANNO,
    sep="\t",
    dtype=str,
    low_memory=False
)

print(f"Rows loaded: {len(df)}")


# ============================================================
# COLUMN DEFINITIONS
# ============================================================
#
# Column positions correspond to the AADR v66.1 annotation
# structure inspected previously.

COL_GENETIC_ID = df.columns[0]
COL_DATE_BP = df.columns[10]
COL_FULL_DATE = df.columns[12]

COL_GROUP = df.columns[14]
COL_LOCALITY = df.columns[15]
COL_POLITICAL = df.columns[16]

COL_LAT = df.columns[17]
COL_LON = df.columns[18]

COL_COMPAT_HO = df.columns[29]

COL_ASSESSMENT = df.columns[47]


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

df["Date_BP_numeric"] = pd.to_numeric(
    df[COL_DATE_BP],
    errors="coerce"
)

df["Compat_HO_SNPs_numeric"] = pd.to_numeric(
    df[COL_COMPAT_HO],
    errors="coerce"
)


# ============================================================
# BUILD SEARCHABLE METADATA STRING
# ============================================================

df["_search_text"] = (
    df[COL_GROUP].fillna("")
    + " "
    + df[COL_LOCALITY].fillna("")
    + " "
    + df[COL_POLITICAL].fillna("")
)


# ============================================================
# ASSIGN BROAD ANALYTICAL REGION
# ============================================================

df["Analysis_region"] = (
    df["_search_text"]
    .apply(find_regions)
)


# ============================================================
# FILTER 1
# DATE RANGE
# ============================================================

ancient = df[
    df["Date_BP_numeric"].notna()
    & (df["Date_BP_numeric"] >= MIN_DATE_BP)
    & (df["Date_BP_numeric"] <= MAX_DATE_BP)
].copy()


print(
    f"Samples passing date filter "
    f"({MIN_DATE_BP}-{MAX_DATE_BP} BP): "
    f"{len(ancient)}"
)


# ============================================================
# FILTER 2
# GEOGRAPHIC / HISTORICAL RELEVANCE
# ============================================================

ancient = ancient[
    ancient["Analysis_region"] != ""
].copy()


print(
    "Samples in selected regions:",
    len(ancient)
)


# ============================================================
# FILTER 3
# COMPATIBILITY_HO COVERAGE
# ============================================================

ancient = ancient[
    ancient["Compat_HO_SNPs_numeric"].notna()
    & (
        ancient["Compat_HO_SNPs_numeric"]
        >= MIN_COMPAT_HO_SNPS
    )
].copy()


print(
    "Samples passing Compatibility_HO coverage filter:",
    len(ancient)
)


# ============================================================
# FILTER 4
# AADR QC
# ============================================================
#
# Remove samples explicitly marked as FAIL or CRITICAL.
#
# QUESTIONABLE samples are retained at this stage because
# ancient DNA quality varies substantially and later filtering
# will further constrain usable variants.

assessment = (
    ancient[COL_ASSESSMENT]
    .fillna("")
    .str.upper()
)


fail_mask = (

    assessment.str.contains(
        "FAIL",
        regex=False
    )

    |

    assessment.str.contains(
        "CRITICAL",
        regex=False
    )
)


ancient = ancient[
    ~fail_mask
].copy()


print(
    "Samples remaining after QC filter:",
    len(ancient)
)


# ============================================================
# FILTER 5
# BALANCE INDIVIDUAL AADR GROUPS
# ============================================================
#
# Important:
#
# We balance at Group_ID level rather than Analysis_region.
#
# Therefore:
#
# Turkey_N
# Turkey_C
# Turkey_EBA
# Turkey_MLBA
# Turkey_IA
# Turkey_Medieval_Byzantine
#
# remain distinct reference populations.
#
# If a Group_ID contains more than five eligible individuals,
# the individuals with the highest Compatibility_HO coverage
# are retained.

ancient = (
    ancient
    .sort_values(
        [
            COL_GROUP,
            "Compat_HO_SNPs_numeric",
            COL_GENETIC_ID
        ],
        ascending=[
            True,
            False,
            True
        ]
    )
    .groupby(
        COL_GROUP,
        group_keys=False,
        dropna=False
    )
    .head(MAX_SAMPLES_PER_GROUP)
    .copy()
)


print(
    f"Samples remaining after Group_ID balancing "
    f"(max {MAX_SAMPLES_PER_GROUP} per group): "
    f"{len(ancient)}"
)


# ============================================================
# PREPARE OUTPUT METADATA
# ============================================================

output = pd.DataFrame({

    "Genetic_ID":
        ancient[COL_GENETIC_ID],

    "Group_ID":
        ancient[COL_GROUP],

    "Analysis_region":
        ancient["Analysis_region"],

    "Date_mean_BP":
        ancient["Date_BP_numeric"],

    "Full_date":
        ancient[COL_FULL_DATE],

    "Locality":
        ancient[COL_LOCALITY],

    "Political_entity":
        ancient[COL_POLITICAL],

    "Latitude":
        ancient[COL_LAT],

    "Longitude":
        ancient[COL_LON],

    "Compatibility_HO_SNPs":
        ancient["Compat_HO_SNPs_numeric"],

    "Assessment":
        ancient[COL_ASSESSMENT],
})


# ============================================================
# SORT OUTPUT
# ============================================================

output = output.sort_values(

    [
        "Analysis_region",
        "Group_ID",
        "Date_mean_BP",
        "Compatibility_HO_SNPs"
    ],

    ascending=[
        True,
        True,
        False,
        False
    ]
)


# ============================================================
# WRITE SAMPLE METADATA
# ============================================================

output.to_csv(
    OUT_META,
    sep="\t",
    index=False
)


# ============================================================
# CREATE PLINK KEEP FILE
# ============================================================
#
# aadr_master.fam structure:
#
# FID IID PAT MAT SEX PHENO
#
# Example:
#
# 1 Loschbour.AG 0 0 1 2
#
# The Genetic_ID from AADR annotation corresponds to IID.

fam = pd.read_csv(
    FAM,
    sep=r"\s+",
    header=None,

    names=[
        "FID",
        "IID",
        "PAT",
        "MAT",
        "SEX",
        "PHENO"
    ],

    dtype=str
)


selected_ids = set(
    output["Genetic_ID"]
)


keep = fam[
    fam["IID"].isin(
        selected_ids
    )
][
    ["FID", "IID"]
].copy()


keep.to_csv(
    OUT_KEEP,
    sep="\t",
    header=False,
    index=False
)


# ============================================================
# CREATE GROUP SUMMARY
# ============================================================

group_summary = (
    output
    .groupby(
        [
            "Analysis_region",
            "Group_ID"
        ],
        dropna=False
    )
    .agg(

        N=(
            "Genetic_ID",
            "size"
        ),

        Mean_date_BP=(
            "Date_mean_BP",
            "mean"
        ),

        Median_Compatibility_HO_SNPs=(
            "Compatibility_HO_SNPs",
            "median"
        )
    )
    .reset_index()
    .sort_values(

        [
            "Analysis_region",
            "Group_ID"
        ]
    )
)


group_summary.to_csv(
    OUT_GROUPS,
    sep="\t",
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

selected_count = len(output)
keep_count = len(keep)

missing_from_plink = (
    selected_ids
    - set(fam["IID"])
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("AADR ancient sample selection")
print("=" * 60)

print(
    f"Selected samples: {selected_count}"
)

print(
    f"PLINK samples found: {keep_count}"
)

print(
    f"Unique AADR Group_IDs: "
    f"{output['Group_ID'].nunique()}"
)

print()

print(
    "Samples by analytical region:"
)

print(
    output[
        "Analysis_region"
    ]
    .value_counts()
    .to_string()
)

print()

print(
    "Date range:"
)

if len(output) > 0:

    print(
        f"{output['Date_mean_BP'].min():.0f} - "
        f"{output['Date_mean_BP'].max():.0f} BP"
    )

else:

    print("No samples selected.")


print()

print(
    "Group size distribution:"
)

print(
    output[
        "Group_ID"
    ]
    .value_counts()
    .value_counts()
    .sort_index()
    .rename_axis(
        "samples_per_group"
    )
    .to_string()
)


print()

if missing_from_plink:

    print(
        "WARNING:"
        f" {len(missing_from_plink)} selected samples "
        "were not found in aadr_master.fam."
    )

else:

    print(
        "PLINK validation: all selected samples found."
    )


print()

print("Outputs:")
print(OUT_META)
print(OUT_KEEP)
print(OUT_GROUPS)

print()

print("Ancient panel selection complete.")
