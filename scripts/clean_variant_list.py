shared_file = "../results/plink/shared_variants.snplist"
ref_file = "../results/plink/shared_variants.pvar"
position_file = "../results/plink/position_mismatches.txt"
output_file = "../results/plink/clean_variants.snplist"


bad_positions = set()

with open(position_file) as f:
    next(f)

    for line in f:
        rsid = line.split()[0]
        bad_positions.add(rsid)


keep = set()
ambiguous = 0
non_biallelic = 0

with open(ref_file) as f:
    for line in f:
        if line.startswith("#"):
            continue

        parts = line.split()

        rsid = parts[2]
        ref = parts[3]
        alt = parts[4]

        alleles = {ref, alt}

        if rsid in bad_positions:
            continue

        if len(alleles) != 2:
            non_biallelic += 1
            continue

        if ref not in "ACGT" or alt not in "ACGT":
            non_biallelic += 1
            continue

        if alleles == {"A", "T"} or alleles == {"C", "G"}:
            ambiguous += 1
            continue

        keep.add(rsid)


with open(shared_file) as f, open(output_file, "w") as out:
    for line in f:
        rsid = line.strip()

        if rsid in keep:
            out.write(rsid + "\n")


print("Position mismatches removed:", len(bad_positions))
print("Ambiguous variants removed:", ambiguous)
print("Non-biallelic/non-SNP variants removed:", non_biallelic)
print("Variants kept:", len(keep))
print("Output:", output_file)
