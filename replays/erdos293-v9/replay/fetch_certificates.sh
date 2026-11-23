#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
release='https://api.github.com/repos/EconLearn/erdos293-check/releases/tags/v9-certificates'
/usr/bin/curl --disable -fsSL --max-time 30 "$release" |
    jq -er '.assets[] | select(.name | test("^v9_certificates_[0-9]+_to_[0-9]+\\.txt\\.xz$")) | [.name, .size, .browser_download_url, .digest, .id] | @tsv' > data/release-assets.tsv
test "$(wc -l < data/release-assets.tsv)" -eq 3
while IFS=$'\t' read -r name size url digest asset_id; do
    remaining=$(( $(cat deadline.epoch) - $(date +%s) ))
    test "$remaining" -gt 0
    limit=$((remaining < 900 ? remaining : 900))
    if ! test -f "data/$name"; then
        if ! /usr/bin/curl --disable -fL --silent --show-error --retry 2 --max-time "$limit" -o "data/$name.part" "$url"; then
            remaining=$(( $(cat deadline.epoch) - $(date +%s) ))
            test "$remaining" -gt 0
            limit=$((remaining < 900 ? remaining : 900))
            /usr/bin/curl --disable -fL --silent --show-error --max-time "$limit" -H 'Accept: application/octet-stream' \
                -o "data/$name.part" "https://api.github.com/repos/EconLearn/erdos293-check/releases/assets/$asset_id?download=$(date +%s)"
        fi
        mv "data/$name.part" "data/$name"
    fi
    test "$(stat -f %z "data/$name")" = "$size"
    printf '%s  %s\n' "${digest#sha256:}" "data/$name" | shasum -a 256 -c
done < data/release-assets.tsv
