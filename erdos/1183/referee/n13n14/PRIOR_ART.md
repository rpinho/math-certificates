# Prior art (referee job)
See REFEREE.md, section "Sources and public status", for the full list. In brief:
- Live scoreboard: erdosproblems.com/1183 (fetched 2026-11-17 05:29 UTC), no small exact values; forum has 11 comments, none on f(13)/f(14); 1 proof claim (BMB, asymptotic).
- Best published bounds at these n: BMB arXiv:2610.02833 (current tex at anaxia-research/Erdos-1183 2842ef3a) prop:flower and thm:f20 give f(13)>=8, f(14)>=8; the omega institute note gives f(n)>=(n+3)/2 for odd n>=11.
- Public exact values: f(11)=7, f(12)=7 only (anaxia issue #20, rpinho/math-certificates 5d5c78b). No public f(13) or f(14) found on GitHub or arXiv.
- Method credited: closure SAT + DRAT (BMB; ipezygj workflow for #609, as cited by the producer); Birkhoff's representation theorem for the non-SAT check (also used by Chojecki's forum comment).
