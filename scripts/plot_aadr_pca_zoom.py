from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path("../results/aadr")
INPUT = RESULTS / "aadr_pca_populations.tsv"

df = pd.read_csv(INPUT, sep="\t")

pc_cols = [f"PC{i}" for i in range(1, 21)]
df[pc_cols] = df[pc_cols].apply(pd.to_numeric)

# Populations most relevant to SAMPLE1's local West Eurasian position
focus_populations = [
    "Turkish",
    "Turkish_Trabzon",
    "Kurd",
    "Kurd_WGA",
    "Iranian",
    "Iranian_Non_Zoroastrian",
    "Azeri",
    "Azeri_Dagestan",
    "Armenian",
    "Armenian_Hemsheni",
    "Georgian",
    "Georgian_WGA",
    "Assyrian",
    "Greek",
    "Greek_WGA",
    "Cypriot",
]

focus = df[
    df["Population"].isin(focus_populations)
].copy()

sample = df[df["Population"] == "FTDNA_SAMPLE"].copy()

print(f"Reference samples plotted: {len(focus)}")
print(f"Populations plotted: {focus['Population'].nunique()}")


def plot_zoom(pc_x, pc_y):
    fig, ax = plt.subplots(figsize=(12, 9))

    populations = sorted(focus["Population"].unique())
    cmap = plt.get_cmap("tab20")

    for i, population in enumerate(populations):
        group = focus[focus["Population"] == population]

        ax.scatter(
            group[pc_x],
            group[pc_y],
            s=35,
            alpha=0.65,
            color=cmap(i % 20),
            label=population,
        )

        # Population centroid
        cx = group[pc_x].mean()
        cy = group[pc_y].mean()

        ax.scatter(
            cx,
            cy,
            marker="x",
            s=70,
            color=cmap(i % 20),
            linewidth=2,
        )

    # SAMPLE1
    sx = sample.iloc[0][pc_x]
    sy = sample.iloc[0][pc_y]

    ax.scatter(
        sx,
        sy,
        marker="*",
        s=450,
        color="black",
        edgecolor="white",
        linewidth=1.2,
        zorder=10,
        label="SAMPLE1",
    )

    ax.annotate(
        "SAMPLE1",
        (sx, sy),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=12,
        fontweight="bold",
    )

    ax.set_xlabel(pc_x)
    ax.set_ylabel(pc_y)

    ax.set_title(
        f"AADR Local West Eurasian PCA — {pc_x} vs {pc_y}"
    )

    ax.grid(alpha=0.2)

    ax.legend(
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        fontsize=8,
    )

    fig.tight_layout()

    output = RESULTS / f"aadr_zoom_{pc_x}_{pc_y}.png"

    fig.savefig(
        output,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"Output: {output}")


plot_zoom("PC1", "PC2")
plot_zoom("PC1", "PC3")
plot_zoom("PC2", "PC3")
