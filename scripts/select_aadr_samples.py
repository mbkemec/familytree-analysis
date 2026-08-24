import os

ind_file = "../reference/aadr/v66.p1_compatibility_HO.aadr.patch.PUB.ind"
fam_file = "../results/aadr/aadr_master.fam"
output_dir = "../results/aadr"

samples_file = f"{output_dir}/selected_samples.txt"
keep_file = f"{output_dir}/selected_samples.keep"

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

selected = {}

with open(ind_file) as f:
    for line in f:
        parts = line.split()

        sample = parts[0]
        group = parts[2]

        if sample.endswith(".HO") and group in groups:
            selected[sample] = group


with open(samples_file, "w") as out:
    for sample, group in selected.items():
        out.write(f"{sample}\t{group}\n")


kept = 0

with open(fam_file) as f, open(keep_file, "w") as out:
    for line in f:
        parts = line.split()

        fid = parts[0]
        iid = parts[1]

        if iid in selected:
            out.write(f"{fid}\t{iid}\n")
            kept += 1


print("Selected samples:", len(selected))
print("PLINK samples found:", kept)
print("Population file:", samples_file)
print("PLINK keep file:", keep_file)
