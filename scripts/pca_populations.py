import pandas as pd
import matplotlib.pyplot as plt

input_file = "../results/plink/pca_with_populations.tsv"

df = pd.read_csv(input_file, sep="\t")

reference = df[df["Population"] != "SAMPLE"]
sample = df[df["Population"] == "SAMPLE"]

plots = [
    ("PC1", "PC2"),
    ("PC1", "PC3"),
    ("PC2", "PC3")
]

for x, y in plots:

    for population in reference["Population"].unique():
        data = reference[reference["Population"] == population]

        plt.scatter(
            data[x],
            data[y],
            label=population,
            s=12,
            alpha=0.6
        )

    plt.scatter(
        sample[x],
        sample[y],
        marker="*",
        s=250,
        edgecolors="black",
        label="SAMPLE1"
    )

    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"PCA - 1000 Genomes Populations ({x} vs {y})")

    plt.legend(
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        fontsize=8
    )

    plt.tight_layout()

    output_file = f"../results/plink/pca_populations_{x}_{y}.png"

    plt.savefig(output_file, dpi=300)
    plt.show()
    plt.close()

    print("Output:", output_file)
