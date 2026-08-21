sample_ped = "../results/plink/sample.ped"
sample_map = "../results/plink/sample.map"
ref_file = "../results/plink/shared_variants.pvar"
position_file = "../results/plink/position_mismatches.txt"
output_file = "../results/plink/allele_mismatches.txt"


position_mismatches = set()

with open(position_file) as f:
    next(f)

    for line in f:
        rsid = line.split()[0]
        position_mismatches.add(rsid)


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
    allele1 = genotypes[i * 2]
    allele2 = genotypes[i * 2 + 1]

    alleles = set()

    if allele1 != "0":
        alleles.add(allele1)

    if allele2 != "0":
        alleles.add(allele2)

    sample_alleles[rsid] = alleles


matches = 0
ambiguous = 0
mismatches = 0
examples = []


with open(output_file, "w") as out:
    out.write("RSID\tSAMPLE_ALLELES\tREF_ALLELES\n")

    with open(ref_file) as f:
        for line in f:
            if line.startswith("#"):
                continue

            parts = line.split()

            rsid = parts[2]
            ref = parts[3]
            alt = parts[4]

            if rsid in position_mismatches:
                continue

            if rsid not in sample_alleles:
                continue

            sample = sample_alleles[rsid]
            reference = {ref, alt}

            if not sample:
                continue

            if reference == {"A", "T"} or reference == {"C", "G"}:
                ambiguous += 1
                continue

            if sample.issubset(reference):
                matches += 1

                if len(examples) < 10:
                    examples.append((rsid, sample, reference))

            else:
                mismatches += 1

                out.write(
                    f"{rsid}\t"
                    f"{'/'.join(sorted(sample))}\t"
                    f"{ref}/{alt}\n"
                )


print("Compatible alleles:", matches)
print("Ambiguous A/T or C/G:", ambiguous)
print("Allele mismatches:", mismatches)
print("Mismatch file:", output_file)

print()
print("Example matches:")

for rsid, sample, reference in examples:
    print(
        rsid,
        "sample:", "/".join(sorted(sample)),
        "reference:", "/".join(sorted(reference))
    )
