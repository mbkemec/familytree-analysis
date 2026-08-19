# Input Data

Place the raw DNA files inside the `data/` directory before running the pipeline.

The pipeline currently expects the following file names:

```text
data/
├── autosomal.csv.gz
├── y_dna.gz
└── snp_results.csv
```

Rename the original files accordingly before starting the analysis.

* `autosomal.csv.gz` — autosomal genotype data
* `y_dna.gz` — Y-chromosome SNP data
* `snp_results.csv` — SNP result summary exported by FamilyTreeDNA

### External tools

- PLINK v1.9.0-b.7.11 64-bit (19 Aug 2025)
- Link: https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20250819.zip

# Data Preparation for PLINK

The raw autosomal genotype file is provided as a CSV file with the following structure:

```text
RSID,CHROMOSOME,POSITION,RESULT
rs3131972,1,752721,AG
```

PLINK does not directly use this CSV format. Therefore, the genotype data must first be converted into a PLINK-compatible input format before downstream analyses such as PCA, heterozygosity, relatedness, and population-genetic analyses can be performed.

For the first autosomal analysis, only chromosomes 1–22 are used.

The following markers are handled separately:

* `X`, `XY`, and `MT` markers are excluded from the initial autosomal analysis and retained in the original dataset.
* Markers with `CHROMOSOME=0` are not treated as invalid, because some of them contain valid genotype calls. However, they cannot be reliably placed in the genome because their chromosome and position are missing, so they are not included in the initial PLINK autosomal dataset.
* Missing genotypes encoded as `--` are retained as missing values during conversion rather than being interpreted as real alleles.
* Non-rsID markers are not automatically removed if they have valid chromosome and position information.

The conversion step creates a standard PLINK dataset, which is then used as the common input for downstream analyses.

# PLINK Binary Conversion

After the raw autosomal genotype data is converted into PLINK PED/MAP format, PLINK is used to create the binary BED/BIM/FAM dataset:

```bash
plink \
  --file results/plink/sample \
  --make-bed \
  --out results/plink/sample
```

For the current sample, PLINK loaded 612,272 autosomal variants and reported a total genotyping rate of 97.9734%.

The generated files are:

* `sample.bed` — binary genotype data
* `sample.bim` — variant information
* `sample.fam` — sample information
* `sample.log` — PLINK execution log

The sample sex and phenotype are currently unspecified, so PLINK reports the individual as having ambiguous sex and no phenotype. This does not affect the initial autosomal analyses.
