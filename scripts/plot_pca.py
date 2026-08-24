import pandas as pd
import matplotlib.pyplot as plt

input_file = "../results/plink/pca_with_populations.tsv"
output_file = "../results/plink/pca_superpop.png"

df = pd.read_csv(input_file, sep="\t")

reference = df[df["SuperPop"] != "SAMPLE"]
sample = df[df["SuperPop"] == "SAMPLE"]

groups = reference["SuperPop"].unique()

for group in groups:
    data = reference[reference["SuperPop"] == group]

    plt.scatter(
        data["PC1"],
        data["PC2"],
        label=group,
        alpha=0.6,
        s=15
    )

plt.scatter(
    sample["PC1"],
    sample["PC2"],
    marker="*",
    s=250,
    label="SAMPLE1",
    edgecolors="black"
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA - 1000 Genomes Reference Populations")

plt.legend()
plt.tight_layout()

plt.savefig(output_file, dpi=300)
plt.show()

print("Output:", output_file)
