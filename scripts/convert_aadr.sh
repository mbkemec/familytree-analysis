#!/usr/bin/env bash
set -euo pipefail

AADR="../reference/aadr"
OUT="../results/aadr"
CONVERTF="$HOME/AdmixTools/bin/convertf"

GENO="$AADR/v66.p1_compatibility_HO.aadr.patch.PUB.geno"
SNP="$AADR/v66.p1_compatibility_HO.aadr.patch.PUB.snp"
IND="$AADR/v66.p1_compatibility_HO.aadr.patch.PUB.ind"

mkdir -p "$OUT"

echo "Convert full AADR Human Origins dataset"
echo "Input GENO: $GENO"
echo "Input SNP : $SNP"
echo "Input IND : $IND"
echo

cat > "$OUT/convert_aadr.par" <<EOF
genotypename:    $GENO
snpname:         $SNP
indivname:       $IND
outputformat:    PACKEDPED
genotypeoutname: $OUT/aadr_master.bed
snpoutname:      $OUT/aadr_master.bim
indivoutname:    $OUT/aadr_master.fam
familynames:     NO
EOF

"$CONVERTF" -p "$OUT/convert_aadr.par"



ls -lh \
    "$OUT/aadr_master.bed" \
    "$OUT/aadr_master.bim" \
    "$OUT/aadr_master.fam"

echo
echo "PLINK validation"

plink \
    --bfile "$OUT/aadr_master" \
    --freq \
    --out "$OUT/aadr_master_check"

echo "AADR master dataset successfully converted and validated."
