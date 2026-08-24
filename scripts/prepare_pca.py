pca_file = "../results/plink/pca.eigenvec"
metadata_file = "../reference/1kg/all_phase3.psam"
output_file = "../results/plink/pca_with_populations.tsv"

populations = {}

with open(metadata_file) as f:
    next(f)

    for line in f:
        parts = line.split()

        iid = parts[0]
        superpop = parts[4]
        population = parts[5]

        populations[iid] = (superpop, population)


with open(pca_file) as f, open(output_file, "w") as out:

    out.write("IID\tSuperPop\tPopulation")

    for i in range(1, 21):
        out.write(f"\tPC{i}")

    out.write("\n")

    for line in f:
        parts = line.split()

        iid = parts[1]
        pcs = parts[2:]

        if iid == "SAMPLE1":
            superpop = "SAMPLE"
            population = "SAMPLE"
        else:
            superpop, population = populations[iid]

        out.write(
            iid + "\t" +
            superpop + "\t" +
            population + "\t" +
            "\t".join(pcs) +
            "\n"
        )


print("Output:", output_file)
