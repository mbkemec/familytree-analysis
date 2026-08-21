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


ambiguous = set()

with open(ref_file) as f:
    for line in f:
        if line.startswith("#"):
            continue

        parts = line.split()

        rsid = parts[2]
        ref = parts[3]
        alt = parts[4]

        alleles = {ref, alt}

        if alleles == {"A", "T"} or alleles == {"C", "G"}:
            ambiguous.add(rsid)


kept = 0
removed = 0

with open(shared_file) as f, open(output_file, "w") as out:
    for line in f:
        rsid = line.strip()

        if rsid in bad_positions or rsid in ambiguous:
            removed += 1
            continue

        out.write(rsid + "\n")
        kept += 1


print("Position mismatches removed:", len(bad_positions))
print("Ambiguous variants removed:", len(ambiguous))
print("Variants kept:", kept)
print("Total removed:", removed)
print("Output:", output_file)
