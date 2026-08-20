#!/bin/bash

mkdir -p ../reference/1kg
cd ../reference/1kg

base_url="http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502"

wget -c "$base_url/integrated_call_samples_v3.20130502.ALL.panel"

for chr in {1..22}
do
    wget -c "$base_url/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz"
done
