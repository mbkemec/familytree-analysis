#!/bin/bash

mkdir -p ../reference/1kg
cd ../reference/1kg

wget -c "https://www.dropbox.com/s/y6ytfoybz48dc0u/all_phase3.pgen.zst?dl=1" \
  -O all_phase3.pgen.zst

wget -c "https://www.dropbox.com/s/odlexvo8fummcvt/all_phase3.pvar.zst?dl=1" \
  -O all_phase3.pvar.zst

wget -c "https://www.dropbox.com/scl/fi/haqvrumpuzfutklstazwk/phase3_corrected.psam?rlkey=0yyifzj2fb863ddbmsv4jkeq6&dl=1" \
  -O all_phase3.psam
