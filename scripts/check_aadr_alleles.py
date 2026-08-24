sample_ped = "../results/plink/sample.ped"
sample_map = "../results/plink/sample.map"
aadr_bim = "../results/aadr/aadr_modern.bim"
clean_file = "../results/aadr/clean_shared_variants.snplist"
output_file = "../results/aadr/aadr_allele_mismatches.txt"


clean = set()

with open(clean_file) as f:
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


sample_alleles = {}

for i, rsid in enumerate(markers):
    if rsid not in clean:
        continue

    allele1 = genotypes[i * 2]
    allele2 = genotypes[i * 2 + 1]

    alleles = set()

    if allele1 != "0":
        alleles.add(allele1)

    if allele2 != "0":
        alleles.add(allele2)

    sample_alleles[rsid] = alleles


matches = 0
missing = 0
mismatches = 0


with open(output_file, "w") as out:
    out.write("RSID\tSAMPLE_ALLELES\tAADR_ALLELES\n")

    with open(aadr_bim) as f:
        for line in f:
            parts = line.split()

            rsid = parts[1]

            if rsid not in clean:
                continue

            allele1 = parts[4]
            allele2 = parts[5]

            reference = {allele1, allele2}
            sample = sample_alleles.get(rsid, set())

            if not sample:
                missing += 1
                continue

            if sample.issubset(reference):
                matches += 1
            else:
                mismatches += 1

                out.write(
                    f"{rsid}\t"
                    f"{'/'.join(sorted(sample))}\t"
                    f"{'/'.join(sorted(reference))}\n"
                )


print("Compatible alleles:", matches)
print("Missing sample genotypes:", missing)
print("Allele mismatches:", mismatches)
print("Mismatch file:", output_file)
