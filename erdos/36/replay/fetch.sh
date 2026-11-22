mkdir -p dl inputs/unktok inputs/wetch
git clone https://github.com/unktok/erdos-36-lower-bound.git dl/unktok
git -C dl/unktok checkout cb2f01237c2867a704739f6864075e0ce4e67f07
cp dl/unktok/RESULT.md dl/unktok/UPSTREAM.json inputs/unktok/
mkdir inputs/unktok/proof && cp -R dl/unktok/proof/MANIFEST.json dl/unktok/proof/data inputs/unktok/proof/

W=27b1cba5f929da7182e97d2e8c42c78c5ee5d4a8
P=outputs/minimum-overlap-hybrid106-radius-pypy627425-v1-checkpoint
for f in central-certificate.json outer-certificate.json; do
  curl -fsSL -o inputs/wetch/$f "https://raw.githubusercontent.com/justinwetch/erdos-36-minimum-overlap/$W/$P/$f"
done
