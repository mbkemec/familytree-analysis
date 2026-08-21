sample_file = "../results/plink/sample.pvar"
ref_file = "../results/plink/shared_variants.pvar"
output_file = "../results/plink/position_mismatches.txt"

sample_pos = {}
ref_pos = {}

with open(sample_file) as f:
    for line in f:
        if line.startswith("#"):
            continue

        parts = line.strip().split()

        chrom = parts[0]
        pos = parts[1]
        rsid = parts[2]

        sample_pos[rsid] = (chrom, pos)

with open(ref_file) as f:
    for line in f:
        if line.startswith("#"):
            continue

        parts = line.strip().split()

        chrom = parts[0]
        pos = parts[1]
        rsid = parts[2]

        ref_pos[rsid] = (chrom, pos)

matches = 0
mismatches = 0

with open(output_file, "w") as out:
    out.write("RSID\tSAMPLE_CHR\tSAMPLE_POS\tREF_CHR\tREF_POS\n")

    for rsid in ref_pos:
        if rsid not in sample_pos:
            continue

        if sample_pos[rsid] == ref_pos[rsid]:
            matches += 1
        else:
            mismatches += 1

            out.write(
                f"{rsid}\t"
                f"{sample_pos[rsid][0]}\t"
                f"{sample_pos[rsid][1]}\t"
                f"{ref_pos[rsid][0]}\t"
                f"{ref_pos[rsid][1]}\n"
            )

print("Position matches:", matches)
print("Position mismatches:", mismatches)
print("Mismatch file:", output_file)
