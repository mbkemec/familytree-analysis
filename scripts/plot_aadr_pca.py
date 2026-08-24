from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path("../results/aadr")

input_file = RESULTS / "aadr_pca_populations.tsv"

df = pd.read_csv(input_file, sep="\t")

sample = df[df["Population"] == "FTDNA_SAMPLE"].copy()
reference = df[df["Population"] != "FTDNA_SAMPLE"].copy()

# PCA coordinates must be numeric.
pc_cols = [f"PC{i}" for i in range(1, 21)]
df[pc_cols] = df[pc_cols].apply(pd.to_numeric)

sample = df[df["Population"] == "FTDNA_SAMPLE"].copy()
reference = df[df["Population"] != "FTDNA_SAMPLE"].copy()


def plot_pca(pc_x, pc_y):
    fig, ax = plt.subplots(figsize=(14, 10))

    populations = sorted(reference["Population"].unique())

    cmap = plt.get_cmap("tab20")

    for i, population in enumerate(populations):
        group = reference[reference["Population"] == population]

        ax.scatter(
            group[pc_x],
            group[pc_y],
            s=25,
            alpha=0.65,
            color=cmap(i % 20),
        )

        # Population centroid
        cx = group[pc_x].mean()
        cy = group[pc_y].mean()

        ax.text(
            cx,
            cy,
            population,
            fontsize=7,
            alpha=0.85,
        )

    # FTDNA sample
    ax.scatter(
        sample[pc_x],
        sample[pc_y],
        marker="*",
        s=350,
        color="black",
        edgecolor="white",
        linewidth=1.2,
        zorder=10,
        label="FTDNA sample",
    )

    sx = sample.iloc[0][pc_x]
    sy = sample.iloc[0][pc_y]

    ax.annotate(
        "SAMPLE1",
        (sx, sy),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_xlabel(pc_x)
    ax.set_ylabel(pc_y)

    ax.set_title(
        f"AADR West Eurasian PCA — {pc_x} vs {pc_y}"
    )

    ax.grid(alpha=0.2)

    fig.tight_layout()

    output = RESULTS / f"aadr_pca_{pc_x}_{pc_y}.png"

    fig.savefig(
        output,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"Output: {output}")


plot_pca("PC1", "PC2")
plot_pca("PC1", "PC3")
plot_pca("PC2", "PC3")
