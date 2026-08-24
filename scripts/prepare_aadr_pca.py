from pathlib import Path

RESULTS = Path("../results/aadr")

eigenvec_file = RESULTS / "aadr_pca.eigenvec"
population_file = RESULTS / "selected_samples.txt"
output_file = RESULTS / "aadr_pca_populations.tsv"

# sample ID -> population
populations = {}

with open(population_file) as f:
    for line in f:
        if not line.strip():
            continue

        parts = line.split()

        if len(parts) >= 2:
            sample_id = parts[0]
            population = parts[1]
            populations[sample_id] = population

rows = []

with open(eigenvec_file) as f:
    for line in f:
        parts = line.split()

        if len(parts) < 22:
            continue

        fid = parts[0]
        iid = parts[1]
        pcs = parts[2:22]

        if iid == "SAMPLE1":
            population = "FTDNA_SAMPLE"
        else:
            population = populations.get(iid, "UNKNOWN")

        rows.append([fid, iid, population] + pcs)

header = ["FID", "IID", "Population"] + [
    f"PC{i}" for i in range(1, 21)
]

with open(output_file, "w") as out:
    out.write("\t".join(header) + "\n")

    for row in rows:
        out.write("\t".join(row) + "\n")

print(f"Samples written: {len(rows)}")
print(
    "Unknown populations:",
    sum(row[2] == "UNKNOWN" for row in rows)
)
print(f"Output: {output_file}")
