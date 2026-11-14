#!/bin/sh
# usage: solve.sh NAME [cadical time limit s]; solves cnf/NAME.cnf, proof to proofs/NAME.drat, logs to logs/
cd "$(dirname "$0")"
T=${2:-7200}
nice -n 10 /usr/bin/time -l tools/cadical/build/cadical -t $T cnf/$1.cnf proofs/$1.drat > logs/$1.solve 2> logs/$1.solve.time
echo "exit $?" >> logs/$1.solve
