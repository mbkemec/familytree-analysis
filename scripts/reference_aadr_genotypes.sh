#!/bin/bash

mkdir -p ../reference/aadr
cd ../reference/aadr

wget -c "https://dataverse.harvard.edu/api/access/datafile/13994522" \
  -O v66.p1_compatibility_HO.aadr.patch.PUB.geno
