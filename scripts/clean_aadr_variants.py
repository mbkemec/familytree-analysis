sample_ped = "../results/plink/sample.ped"
sample_map = "../results/plink/sample.map"
input_file = "../results/aadr/clean_shared_variants.snplist"
output_file = "../results/aadr/aadr_final_variants.snplist"


clean = set()

with open(input_file) as f:
    for line in f:
        clean.add(line.strip())


markers = []

with open(sample_map) as f:
    for line in f:
        parts = line.split()
        markers.append(parts[1])


with open(sample_ped) as f:
    parts = f.readline().split()

genotypes = parts[6:]


missing = set()

for i, rsid in enumerate(markers):
    if rsid not in clean:
        continue

    allele1 = genotypes[i * 2]
    allele2 = genotypes[i * 2 + 1]

    if allele1 == "0" and allele2 == "0":
        missing.add(rsid)


kept = 0

with open(input_file) as f, open(output_file, "w") as out:
    for line in f:
        rsid = line.strip()

        if rsid in missing:
            continue

        out.write(rsid + "\n")
        kept += 1


print("Starting variants:", len(clean))
print("Missing variants removed:", len(missing))
print("Final variants:", kept)
print("Output:", output_file)
