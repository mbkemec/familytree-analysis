sample_file = "../results/plink/sample_clean.pvar"
aadr_file = "../results/aadr/aadr_modern.bim"
shared_file = "../results/aadr/shared_variants.snplist"

mismatch_file = "../results/aadr/aadr_position_mismatches.txt"
clean_file = "../results/aadr/clean_shared_variants.snplist"


shared = set()

with open(shared_file) as f:
    for line in f:
        shared.add(line.strip())


sample_variants = {}

with open(sample_file) as f:
    for line in f:
        if line.startswith("#"):
            continue

        parts = line.split()

        chrom = parts[0]
        pos = parts[1]
        rsid = parts[2]

        if rsid in shared:
            sample_variants[rsid] = (chrom, pos)


position_matches = 0
position_mismatches = 0
ambiguous = 0
clean = 0


with open(mismatch_file, "w") as mismatch_out, \
     open(clean_file, "w") as clean_out:

    mismatch_out.write(
        "RSID\tSAMPLE_CHR\tSAMPLE_POS\tAADR_CHR\tAADR_POS\n"
    )

    with open(aadr_file) as f:
        for line in f:
            parts = line.split()

            chrom = parts[0]
            rsid = parts[1]
            pos = parts[3]
            allele1 = parts[4]
            allele2 = parts[5]

            if rsid not in shared:
                continue

            if rsid not in sample_variants:
                continue

            sample_chrom, sample_pos = sample_variants[rsid]

            if sample_chrom != chrom or sample_pos != pos:
                position_mismatches += 1

                mismatch_out.write(
                    f"{rsid}\t"
                    f"{sample_chrom}\t"
                    f"{sample_pos}\t"
                    f"{chrom}\t"
                    f"{pos}\n"
                )

                continue

            position_matches += 1

            alleles = {allele1, allele2}

            if alleles == {"A", "T"} or alleles == {"C", "G"}:
                ambiguous += 1
                continue

            clean_out.write(rsid + "\n")
            clean += 1


print("Shared variants:", len(shared))
print("Position matches:", position_matches)
print("Position mismatches:", position_mismatches)
print("Ambiguous A/T or C/G:", ambiguous)
print("Clean variants:", clean)

print()
print("Mismatch file:", mismatch_file)
print("Clean variant list:", clean_file)
