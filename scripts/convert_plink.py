import csv
import os

input_file = "../data/autosomal.csv"
output_dir = "../results/plink"

map_file = f"{output_dir}/sample.map"
ped_file = f"{output_dir}/sample.ped"

os.makedirs(output_dir, exist_ok=True)

markers = []
genotypes = []

with open(input_file) as f:
    reader = csv.DictReader(f)

    for row in reader:
        rsid = row["RSID"].strip()
        chrom = row["CHROMOSOME"].strip()
        pos = row["POSITION"].strip()
        genotype = row["RESULT"].strip()

        # Keep only autosomal chromosomes
        if not chrom.isdigit():
            continue

        if int(chrom) < 1 or int(chrom) > 22:
            continue

        markers.append((chrom, rsid, pos))

        # PLINK uses 0 0 for missing genotypes
        if genotype == "--":
            genotypes.append(("0", "0"))
        else:
            genotypes.append((genotype[0], genotype[1]))


with open(map_file, "w") as f:
    for chrom, rsid, pos in markers:
        f.write(f"{chrom}\t{rsid}\t0\t{pos}\n")


with open(ped_file, "w") as f:
    f.write("FAM1 SAMPLE1 0 0 0 -9")

    for allele1, allele2 in genotypes:
        f.write(f" {allele1} {allele2}")

    f.write("\n")


print("Markers:", len(markers))
print("MAP:", map_file)
print("PED:", ped_file)
