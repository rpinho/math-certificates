#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
xz -T1 -dc -- \
    data/v9_certificates_2_to_3000000.txt.xz \
    data/v9_certificates_3000001_to_10000000.txt.xz \
    data/v9_certificates_10000001_to_20000000.txt.xz |
    /usr/bin/time -l build/check_certificates 2 13856992 13856993
