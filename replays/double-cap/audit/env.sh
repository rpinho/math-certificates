JOB="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
M="$JOB/deps/third_party/mathlib4-db584cd6d46c"
TC="$JOB/toolchain/toolchains/leanprover--lean4---v4.33.0/bin"
export PATH="$TC:$PATH" TMPDIR="$JOB/tmp" MATHLIB_CACHE_DIR="$JOB/tmp/mathlib-cache" XDG_CACHE_HOME="$JOB/tmp/cache" ELAN_HOME="$JOB/toolchain"
export LEAN_NUM_THREADS=2 LAKE_JOBS=2 RAYON_NUM_THREADS=2 GIT_CONFIG_NOSYSTEM=1 GIT_TERMINAL_PROMPT=0
