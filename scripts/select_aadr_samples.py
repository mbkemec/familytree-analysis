import os

ind_file = "../reference/aadr/v66.p1_compatibility_HO.aadr.patch.PUB.ind"
output_dir = "../results/aadr"
output_file = f"{output_dir}/selected_samples.txt"

os.makedirs(output_dir, exist_ok=True)

groups = {
    "Turkish",
    "Turkish_Trabzon",
    "Kurd",
    "Iranian",
    "Iranian_Non_Zoroastrian",
    "Iranian_Zoroastrian",
    "Georgian",
    "Armenian",
    "Armenian_Hemsheni",
    "Azeri",
    "Azeri_Dagestan",
    "Greek",
    "Bulgarian",
    "Cypriot",
    "Assyrian",
    "Druze",
    "Palestinian",
    "Lebanese",
    "Lebanese_Muslim",
    "Lebanese_Christian",
    "Syrian",
    "Jordanian",
    "Ossetian",
    "Chechen",
    "Lezgin",
    "Adygei",
    "Italian_South",
    "Italian_Central",
    "Sicilian",
    "Serbian_Serb",
    "Romanian",
    "Albanian",
    "Gagauz",
    "Turkmen",
    "Uzbek",
    "Tajik"
}

selected = []

with open(ind_file) as f:
    for line in f:
        parts = line.split()

        sample = parts[0]
        group = parts[2]

        if sample.endswith(".HO") and group in groups:
            selected.append((sample, group))


with open(output_file, "w") as out:
    for sample, group in selected:
        out.write(f"{sample}\t{group}\n")


print("Selected samples:", len(selected))
print("Output:", output_file)
