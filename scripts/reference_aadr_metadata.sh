#!/bin/bash

mkdir -p ../reference/aadr
cd ../reference/aadr

wget -c "https://dataverse.harvard.edu/api/access/datafile/13994525" \
  -O v66.p1_compatibility_HO.aadr.PUB.anno

wget -c "https://dataverse.harvard.edu/api/access/datafile/13994523" \
  -O v66.p1_compatibility_HO.aadr.patch.PUB.ind

wget -c "https://dataverse.harvard.edu/api/access/datafile/13994524" \
  -O v66.p1_compatibility_HO.aadr.patch.PUB.snp
