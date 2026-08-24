from collections import Counter
from pathlib import Path

IND_FILE = Path(
    "../reference/aadr/v66.p1_compatibility_HO.aadr.patch.PUB.ind"
)

OUTPUT_FILE = Path(
    "../results/aadr/ancient_groups.txt"
)

KEYWORDS = (
    "Turkey",
    "Anatolia",
    "Armenia",
    "Georgia",
    "Caucasus",
    "Iran",
    "Iraq",
    "Syria",
    "Levant",
    "Jordan",
    "Palestine",
    "Lebanon",
    "Steppe",
    "Yamnaya",
    "Sintashta",
    "Andronovo",
    "Scyth",
    "Sarmat",
    "Kazakh",
    "Kyrgyz",
    "Uzbek",
    "Turkmen",
    "Mongol",
    "CentralAsia",
)


def main():

    if not IND_FILE.exists():
        raise FileNotFoundError(
            f"AADR IND file not found: {IND_FILE}"
        )

    groups = Counter()

    with IND_FILE.open() as f:
        for line in f:

            parts = line.split()

            if len(parts) < 3:
                continue

            sample = parts[0]
            group = parts[2]

            # Modern Human Origins samples use the .HO suffix.
            # Here we are interested only in ancient samples.
            if sample.endswith(".HO"):
                continue

            if any(
                keyword.lower() in group.lower()
                for keyword in KEYWORDS
            ):
                groups[group] += 1

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    total_groups = len(groups)
    total_samples = sum(groups.values())

    with OUTPUT_FILE.open("w") as out:

        out.write("Ancient West Eurasian groups\n")
        out.write("=" * 70 + "\n\n")

        out.write("Population\tSamples\n")

        for group, count in groups.most_common():
            out.write(f"{group}\t{count}\n")

        out.write("\n")
        out.write(f"Groups: {total_groups}\n")
        out.write(f"Samples: {total_samples}\n")

    print("AADR ancient population inspection")
    print("=" * 50)
    print(f"Groups found: {total_groups}")
    print(f"Samples found: {total_samples}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
