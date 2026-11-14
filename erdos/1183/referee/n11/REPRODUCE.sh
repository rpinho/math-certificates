#!/bin/sh
# Run from the job directory after building the pins in BUILD_COMMANDS.txt.
# Set REFEREE_PYTHON to the Python interpreter to use. Standard library only.
set -eu
referee_python=${REFEREE_PYTHON:-python3}
mkdir -p replay
nice -n 10 "$referee_python" check_data.py > replay/data_check.txt
nice -n 10 "$referee_python" published_lower.py > replay/published_lower.log
nice -n 10 "$referee_python" rank_lattices.py > replay/rank_lattices.log
for colour in 0 1
do
    stem="replay/c${colour}_k8"
    nice -n 10 "$referee_python" encode.py "$colour" 8 "$stem.cnf" > "$stem.encode"
    solver_exit=0
    nice -n 10 tools/cadical/build/cadical "$stem.cnf" "$stem.drat" > "$stem.solve" || solver_exit=$?
    test "$solver_exit" -eq 20
    nice -n 10 tools/drat-trim/drat-trim "$stem.cnf" "$stem.drat" > "$stem.check"
done
nice -n 10 "$referee_python" encode.py 0 7 replay/c0_k7.cnf > replay/c0_k7.encode
solver_exit=0
nice -n 10 tools/cadical/build/cadical replay/c0_k7.cnf > replay/c0_k7.solve || solver_exit=$?
test "$solver_exit" -eq 10
nice -n 10 "$referee_python" check_data.py replay/c0_k7.cnf replay/c0_k7.solve > replay/c0_k7.modelcheck
checker_exit=0
nice -n 10 tools/drat-trim/drat-trim replay/c0_k8.cnf certificates/corrupt.drat > replay/corrupt.check || checker_exit=$?
test "$checker_exit" -eq 1
printf '%s\n' 'Reproduced both upper proofs, the lower checks, the weighted-poset check, and both controls.'
