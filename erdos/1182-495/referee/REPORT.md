Shipped: I independently verified the Erdős #1182 upper bound F(n) ≤ floor(99n/20) − 1 for every integer n ≥ 450000.

I obtained a strict combined probability upper bound of 0.357093479729 at 450000 and proved that it decreases thereafter. My 192-bit replay checked all 11,011 leaves and rejected all 14 named mutations. The closest rate upper bound was below −0.00150154465578. I confirmed the integer subtraction against the official definition. [Referee report](REFEREE_REPORT.md) · [Verifier](referee_verify.py) · [Sources and baseline reproduction](PRIOR_ART.md)

Did I find something new? No. I verified the submitted improvement on the supplied 5n−1 comparison. I corrected two references and documented the positive unrestricted-rate witness. Historical priority, optimality, and the producer's estimated crossing points lie outside my verdict.

CONTROLS: No. I rejected 14 mutations in the command below, including removing Case I occupancy on the rational witness's record 873. I documented the unsuccessful preliminary specimen in my referee report.

CONTRADICTING: No. I reproduced positive unrestricted rates above 0.00336352695 and 0.01436464953 in positive_witness() and checked all 366,656 near cells and 11,458 tail decisions.

LABELS: No. I reconstructed 11,008 splits, proved emptiness on 39 leaves, and recomputed all applicable rate bounds in referee_verify.py.

To reproduce my verdict from this directory, run

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  nice -n 10 /Users/ricardo/dev/open-science/.venv/bin/python -Bu referee_verify.py
~~~

My next editorial step would be to correct the BEFRS80 citation and the Nikiforov–Rousseau pagination in the producer's prior-art note. The theorem and its certificates are ready for the owner's review.
