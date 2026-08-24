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

# PLINK Sample Statistics

After creating the binary PLINK dataset, basic sample-level statistics were calculated with `scripts/plink_stats.sh`.

The script currently runs:

```bash
plink \
  --bfile ../results/plink/sample \
  --missing \
  --out ../results/plink/missingness

plink \
  --bfile ../results/plink/sample \
  --het \
  --out ../results/plink/heterozygosity
```

## Missingness

PLINK reported:

```text
N_MISS = 12408
N_GENO = 612272
F_MISS = 0.02027
```

This means that 12,408 of the 612,272 autosomal genotype calls are missing, corresponding to an autosomal missing genotype rate of approximately 2.03%.

The file `missingness.imiss` contains sample-level missingness statistics, while `missingness.lmiss` contains variant-level missingness.

Since the current dataset contains only one individual, each variant in `missingness.lmiss` currently has either:

* `F_MISS = 0` if the genotype is present
* `F_MISS = 1` if the genotype is missing

Variant-level missingness will become more informative after the sample is combined with a multi-sample reference dataset.

## Heterozygosity

PLINK `--het` was also tested on the current dataset. The output was:

```text
O(HOM) = 0
E(HOM) = 53620
N(NM) = 107230
F = -1
```

This result should not be interpreted as a biological heterozygosity estimate.

PLINK calculates expected homozygosity using allele frequencies estimated from the analyzed dataset. Since the current PLINK dataset contains only one individual, reliable population allele frequencies cannot be estimated.

For this reason, the current `--het` result is retained only as a pipeline test. Heterozygosity will be recalculated and interpreted after the sample is combined with an appropriate multi-sample population reference panel.

## Genome Build

FamilyTreeDNA Family Finder autosomal raw data uses GRCh37 (hg19) genomic coordinates. Therefore, downstream reference datasets are kept in GRCh37 whenever possible to avoid unnecessary coordinate liftover.

**Reference:** [FamilyTreeDNA – Downloading Your Family Finder Data](https://help.familytreedna.com/hc/en-us/articles/14860944283407-Downloading-Your-Family-Finder-Data)


## Population Reference Dataset

Population-level analyses require a reference dataset containing individuals
from known populations. The FamilyTreeDNA autosomal dataset contains only one
individual, so population structure and ancestry cannot be evaluated from the
sample alone.

For this purpose, the 1000 Genomes Project Phase 3 dataset provided through the
official PLINK resources is used as the population reference.

### Why 1000 Genomes Phase 3?

The reference panel contains 2,504 individuals from multiple populations and
provides a population context for downstream analyses such as PCA.

Another important consideration is genome-build compatibility. The
FamilyTreeDNA autosomal data uses GRCh37 coordinates. The selected 1000 Genomes
Phase 3 resource is also based on GRCh37, avoiding an unnecessary coordinate
liftover step.

The reference dataset will not be compared directly using all available
variants. The complete reference contains substantially more variants than the
FamilyTreeDNA SNP array. Only compatible variants shared between the sample and
the reference panel will be retained during the harmonization step.

### Reference download

The reference files are downloaded with:

`scripts/reference_1000genomes.sh`

The following PLINK 2 files are obtained:

- `all_phase3.pgen.zst` — genotype data
- `all_phase3.pvar.zst` — variant information
- `all_phase3.psam` — sample information

The compressed `.pgen.zst` file is decompressed using:

`scripts/decompress_1000genomes.sh`

This produces:

`reference/1kg/all_phase3.pgen`

The `.pvar.zst` file does not need to be decompressed because PLINK 2 can read
the compressed variant file directly.

### Reference validation

The downloaded reference dataset is checked with:

`scripts/check_1000genomes.sh`

PLINK 2 successfully loaded:

- 2,504 individuals
- 84,805,772 variants

Allele frequencies were calculated successfully, confirming that the genotype,
variant and sample files can be read together correctly.

The allele-frequency calculation at this stage is primarily used as a
validation step rather than as a final population analysis.

### Planned use

The reference panel will be used in the following workflow:

1. Convert the FamilyTreeDNA sample to PLINK 2 format.
2. Identify variants shared between the sample and the reference panel.
3. Check genomic positions and allele compatibility.
4. Remove incompatible or ambiguous variants where necessary.
5. Combine the sample with the reference population dataset.
6. Apply population-genetics QC and LD pruning.
7. Perform PCA using the reference populations.
8. Compare the position of the FamilyTreeDNA sample with known population
   clusters.

PCA will be interpreted as a population-genetic similarity analysis rather than
as a direct ancestry-percentage estimate.

### Software

The reference dataset uses the PLINK 2 PGEN format. PLINK 2 is therefore used
for reference processing and subsequent population analyses.

Current version:

`PLINK v2.0.0-a.7.4LM AVX2 Intel (18 Aug 2026)`

Earlier preprocessing steps were initially performed with PLINK 1.9. Both
versions are retained for reproducibility, while downstream population analysis
uses PLINK 2.

### References

- PLINK 2 Resources:
  https://www.cog-genomics.org/plink/2.0/resources

- 1000 Genomes Project Phase 3:
  https://www.internationalgenome.org/data-portal/data-collections/phase3/

- The 1000 Genomes Project Consortium (2015). A global reference for human
  genetic variation. Nature 526, 68–74.
  https://doi.org/10.1038/nature15393

### Heterozygosity

PLINK 2 does not calculate heterozygosity from the current single-sample dataset because reliable allele frequencies cannot be estimated from one individual.

PLINK 2 requires either a sufficiently large sample set or an external allele-frequency reference file for this calculation.

For this reason, heterozygosity analysis is postponed until the FamilyTreeDNA sample has been harmonized with the 1000 Genomes reference panel. This avoids interpreting allele-frequency-dependent statistics from an inappropriate single-sample dataset.

# Shared Variant Identification

Before combining the FamilyTreeDNA sample with the 1000 Genomes reference panel, variants shared between the two datasets are identified.

The FamilyTreeDNA PLINK 2 dataset contains:

```text
612,272 autosomal variants
```

Using `scripts/shared_variants.sh`, these variant IDs are compared against the 1000 Genomes Phase 3 reference panel with PLINK 2.

The reference panel contains:

```text
84,805,772 variants
```

After extracting reference variants whose IDs are present in the FamilyTreeDNA sample, PLINK 2 identified:

```text
586,909 shared variants
```

This corresponds to approximately 95.9% of the autosomal variants in the FamilyTreeDNA sample.

The high overlap indicates that the 1000 Genomes Phase 3 reference panel provides good coverage of the SNPs present in the FamilyTreeDNA array data and is suitable for downstream population-genetic comparison.

The script produces:

```text
results/plink/sample_variants.snplist
results/plink/shared_variants.snplist
```

`sample_variants.snplist` contains the autosomal variant IDs present in the FamilyTreeDNA sample.

`shared_variants.snplist` contains the subset of these variants also found in the 1000 Genomes reference panel.

Variant ID overlap alone is not sufficient for merging the datasets. Before combining the sample with the reference panel, the shared variants must also be checked for:

* chromosome and genomic position agreement;
* allele compatibility;
* strand orientation;
* strand-ambiguous A/T and C/G variants;
* duplicate variant IDs or genomic positions.

These checks are performed before PCA or other population-level analyses to avoid introducing mismatched genotypes into the combined dataset.

### Variant Position Check

Shared variants were checked with:

`scripts/check_variant_match.py`

The script compares chromosome and position between the FamilyTreeDNA sample
and the corresponding 1000 Genomes variants.

Results:

- Position matches: 586,803
- Position mismatches: 106
- Position agreement: ~99.98%

Mismatching variants are saved to:

`results/plink/position_mismatches.txt`

Most mismatches differ by approximately one base pair, likely due to differences
in variant representation or normalization. These variants will be excluded
before downstream harmonization.

The 586,803 position-matched variants are used for the next allele and strand
compatibility check.

### Allele Compatibility and Clean Variant Set

Allele compatibility was checked with:

`scripts/check_alleles.py`

Observed FamilyTreeDNA genotype alleles were compared with the corresponding
1000 Genomes REF/ALT alleles after excluding position mismatches.

Results:

- Compatible alleles: 578,946
- Ambiguous A/T or C/G: 5,099
- Allele mismatches: 0

A/T and C/G variants are strand-ambiguous and are therefore excluded from the
dataset used for population analysis.

The final variant list was created with:

`scripts/clean_variant_list.py`

Starting from 586,909 shared variants, the script removed:

- 106 position-mismatched variants
- 5,187 strand-ambiguous variants

This produced:

`results/plink/clean_variants.snplist`

containing **581,616 variants** for downstream harmonization and population
analysis.

### Clean PLINK Datasets

The filtered variant list was applied to both the FamilyTreeDNA sample and the 1000 Genomes reference panel with:

`scripts/filter_datasets.sh`

The script uses `results/plink/clean_variants.snplist` and creates two PLINK 2 datasets containing the same **581,616 variants**:

* `results/plink/sample_clean.*` — filtered FamilyTreeDNA sample
* `results/plink/1kg_clean.*` — filtered 1000 Genomes reference panel

The reference dataset contains 2,504 individuals, while the FamilyTreeDNA dataset contains one individual.

Using the same filtered variant set on both datasets ensures that downstream harmonization and population analyses are performed on directly comparable loci.

### Dataset Merge

The cleaned FamilyTreeDNA sample and 1000 Genomes reference datasets were merged with:

`scripts/merge_datasets.sh`

Because PLINK 2 non-concatenating merge is still under development, the cleaned PLINK 2 datasets are first converted to BED/BIM/FAM format and merged with PLINK 1.9.

After filtering to biallelic A/C/G/T SNPs, the final merged dataset contains:

- 2,505 individuals
- 581,397 variants
- Genotyping rate: 99.9998%

The merged dataset is stored as:

`results/plink/merged.*`

### LD Pruning

Linkage disequilibrium pruning was performed with:

`scripts/ld_prune.sh`

PLINK was run with:

`--indep-pairwise 50 5 0.2`

LD pruning reduces redundancy by removing highly correlated SNPs. This prevents genomic regions containing many linked variants from having too much influence on PCA.

The parameters mean:

* `50` — analyze variants in windows of 50 SNPs
* `5` — move the window forward by 5 SNPs at each step
* `0.2` — remove one SNP from pairs with linkage disequilibrium above r² = 0.2

Results:

* Variants before pruning: 581,397
* Variants removed: 240,553
* Variants retained: 340,844

The retained SNP list is stored in:

`results/plink/ld_pruned.prune.in`


### Global PCA with 1000 Genomes

Principal Component Analysis (PCA) was performed with:

`scripts/pca.sh`

The analysis used the **340,844 LD-pruned SNPs** from the merged dataset containing **2,504 1000 Genomes reference individuals and one FamilyTreeDNA sample (2,505 individuals total)**.

The first 20 principal components were calculated with:

`--pca 20`

The main outputs are:

- `results/plink/pca.eigenvec` — principal component scores for each individual
- `results/plink/pca.eigenval` — eigenvalues of the principal components

Population and superpopulation labels from the 1000 Genomes metadata were added to the PCA results with:

`scripts/prepare_pca.py`

This produced:

`results/plink/pca_with_populations.tsv`

The global PCA was first visualized by superpopulation with:

`scripts/plot_pca.py`

The reference individuals were grouped into the five 1000 Genomes superpopulations:

- AFR — African
- AMR — Admixed American
- EAS — East Asian
- EUR — European
- SAS — South Asian

A more detailed population-level visualization was then generated with:

`scripts/pca_populations.py`

The script produces three PCA projections:

- PC1 vs PC2
- PC1 vs PC3
- PC2 vs PC3

These plots allow the FamilyTreeDNA sample (`SAMPLE1`) to be compared with the individual 1000 Genomes populations rather than only the broader superpopulation groups.

### Interpretation and Limitation

The global PCA places `SAMPLE1` within the broader West Eurasian part of the genetic variation represented by the 1000 Genomes panel, while the sample does not fall directly within one of the available reference population clusters.

This result should not be interpreted as ancestry proportions. PCA describes genetic similarity and variation relative to the populations included in the reference panel.

In particular, the 1000 Genomes Phase 3 panel does not contain a dedicated Turkish or Anatolian population. Therefore, populations such as Anatolian, Balkan, Caucasian and other Near Eastern groups are not adequately represented in this PCA space.

For this reason, the 1000 Genomes analysis is used primarily as a **global population comparison and validation of the analysis pipeline**, rather than as the final regional ancestry analysis.

The next stage will use a more detailed **West Eurasian reference panel**, with particular emphasis on populations from Anatolia, the Balkans, the Caucasus, Southern Europe and the Near East.

## Regional Reference Panel with AADR

For more detailed ancestry analysis around Anatolia and neighboring regions, the project uses the Allen Ancient DNA Resource (AADR).

The selected release is:

**AADR v66.p1 (June 8, 2026)**

The analysis uses the:

**v66.p1 compatibility Human Origins dataset**

This dataset was selected because it contains modern Human Origins samples from populations relevant to Anatolia, the Balkans, the Caucasus, Iran and the Near East, while remaining compatible with the hg19/GRCh37 coordinate system used by the FamilyTreeDNA sample.

### AADR Data Download

Metadata and SNP information are downloaded with:

`scripts/reference_aadr_metadata.sh`

The script downloads:

- `v66.p1_compatibility_HO.aadr.PUB.anno`
- `v66.p1_compatibility_HO.aadr.patch.PUB.ind`
- `v66.p1_compatibility_HO.aadr.patch.PUB.snp`

The genotype dataset is downloaded separately with:

`scripts/reference_aadr_genotypes.sh`

which downloads:

- `v66.p1_compatibility_HO.aadr.patch.PUB.geno`

The AADR reference files are stored in:

`reference/aadr/`

### Modern Population Inspection

Modern Human Origins populations were inspected with:

`scripts/inspect_aadr_populations.py`

The script reads the AADR `.ind` file and counts samples with the `.HO` suffix.

Relevant populations include groups such as:

- Turkish
- Turkish_Trabzon
- Kurd
- Iranian
- Armenian
- Georgian
- Azeri
- Greek
- Bulgarian
- Cypriot
- Assyrian
- Druze
- Palestinian
- Lebanese
- Syrian
- Jordanian
- Caucasus populations
- Southern European populations
- Central Asian populations

A regional modern panel was then defined with:

`scripts/select_aadr_samples.py`

This selected **579 modern individuals** for the West Eurasian reference panel.

### AADR Format Conversion

AADR distributes the compatibility Human Origins genotype dataset in binary **TGENO** format.

The complete dataset was converted once into PLINK BED/BIM/FAM format with:

`scripts/convert_aadr.sh`

The script uses `convertf` from DReichLab AdmixTools.

The resulting master reference dataset contains:

- 27,594 individuals
- 276,725 SNPs
- overall genotyping rate: 62.3%

The master dataset is stored as:

`results/aadr/aadr_master.*`

The full master dataset is retained so that the same converted reference can later be reused for:

- modern regional ancestry analysis
- ancient Anatolian comparisons
- Caucasus and Iranian ancient populations
- Balkan and Near Eastern comparisons
- other future AADR-based analyses
