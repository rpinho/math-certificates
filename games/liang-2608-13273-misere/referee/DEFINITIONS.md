# Definitions used (quoted from inputs/sources/2608.13273v2.txt, line numbers of that file)

## Octal move rules, §3.2 (lines 357–390)

> Octal games are represented by codes of the form d0.d1d2d3 . . . in octal notation …, where each ds indicates the legal moves when removing s tokens:
> 0 no legal move removing s tokens · 1 remove an entire heap of exactly s tokens · 2 remove s tokens, leaving a nonempty remainder · 3 both 1 and 2 are legal · 4 remove s tokens, split the remainder into two nonempty heaps · 5 both 1 and 4 are legal · 6 both 2 and 4 are legal · 7 1, 2, and 4 are all legal
> … We require that the first digit d0 of the code can only be 0 or 4 (splitting a heap into two heaps without removing any tokens)

> heaps can be regarded as commutative. Moreover, empty heaps of size 0 are always unable to move, and adding or removing any number of empty heaps has no effect on the position.

Partizan codes `L:R` (lines 467–489): labelled positions (θ; u); "move according to the rule corresponding to the label, while simultaneously flipping the label". Used only for the 0.04:0.03 control.

## Misère convention, §2.1 Def. 2.2 (lines 140–142) and §3.4.2 (lines 748–753)

> o−(u) = P ⇐⇒ (∄u′ ∈ next(u), o−(u′) = N) and u ∉ T ;
> o−(u) = N ⇐⇒ (∃u′ ∈ next(u), o−(u′) = P) or u ∈ T .

> (1−) T ⊆ WN . (3−) (WN − T) ⊆ prev(WP). That is, terminal positions are N-positions

(The spec's "§3.4.2" exists; there is no separate §2.1 misère paragraph beyond Def. 2.2 above.)

## Grouped-digit notation, §3.5.2 (lines 909–912)

> We adopt the shorthand notation for octal game codes from [25]:
> ˙d := d, d + 1;  ¨d := d, d + 2;  ¯d := d, d + 1, d + 2, d + 3.

So 0.2˙6¯0 = {0.260–0.263, 0.270–0.273}, 0.72¯4 = {0.724–0.727}, 4.¨0˙6 = {4.06, 4.07, 4.26, 4.27}, 0.32˙6 = {0.326, 0.327}, etc. The 25 table entries expand to 55 codes; WITNESSES.tsv covers all 55 (plus 4 codes from 2611.29198).

## Definition 3.4 (lines 1130–1148)

> We say that a game is algebraically periodic if there exist natural numbers p1, p2 ∈ N and positive integers t1, t2 ∈ N+, such that for every position (with heaps sorted in non-increasing order) with largest heap a1 sufficiently large, i.e., a1 ≥ p1 + t1, u = (a1, a2, . . . , an) ∈ U, a1 ≥ a2 ≥ . . . ≥ an, it can always be reduced to a smaller position in one of the following two ways:
> (1) Single-heap reduction: if the second-largest heap a2 < p2 + t2 (in particular, when n = 1 we regard a2 = 0 < p2 + t2), then o−(u) = o−(a1 − t1, a2, . . . , an).
> (2) Two-heap reduction: if a2 ≥ p2 + t2, then o−(u) = o−(a1 − t2, a2 − t2, a3 . . . , an).
> We call the lexicographically smallest tuple (p1, t1, p2, t2) the parameters of algebraic periodicity

What a printed tuple predicts: for every sorted u with a1 ≥ p1+t1, u and its branch-(1) or branch-(2) reduct have the same misère outcome. One sorted position with different outcomes from its reduct refutes the tuple. Tuples are the p.27 table, transcribed from inputs/sources/page27.png (same as the text extraction).

## Other printed claims the witness rows use

- p.27–28 single-heap rows: "the periodicity of outcomes of single-heap positions (starting from size 1, assuming algebraic periodicity holds)" (lines 1194–1196) and the rows of lines 1336–1413.
- p.27 explicit 0.73˙4 P-sets Pcor, Pinn, Pout (lines 1177–1189).
- 2611.29198 Definition 4.2 (slice version of Def 3.4 with two fixed heaps a, b), Conjecture 4.1 (o(2,2,x,y) in 0.3122 depends only on x mod 7, y mod 7, [|x−y| ≤ 4]) and Conjecture 4.4 (folding a fixed heap by the period *fails* in general).

## Reading each witness row needs

| comparison | reading |
|---|---|
| Def. 3.4 branch 1 / 2 (50 rows) | sort the original position; check a1 ≥ p1+t1, choose branch by a2 vs p2+t2, apply it; the reduct must equal the other position; outcomes must differ. |
| outcome template, p.28 (108 rows) | the printed row read from heap size 1 as the caption says; the "mismatching" position's printed letter must differ from its true outcome. Delicate: for 0.2˙6¯0 and 4.¨0˙6 the whole printed row is exactly right if read from size 0, so those rows depend on the caption's "size 1". |
| outcome template, explicit P formula (4 rows, 0.73˙4) | membership in Pcor ∪ Pinn ∪ Pout vs the true outcome. |
| Definition 4.2 branch 2 (2 rows, 0.3102) | prefix (a,b) fixed, variable pair reduced by t2 with Remark 4.5's tuple (46,5,12,5) as the producer read it. |
| residue key / published counterexample (9 rows, 0.3122) | same key (x mod 7, y mod 7, [|x−y|≤4]) for the two variable heaps of (2,2,x,y), different outcomes. |
| fixed heap folding (4 rows) | Conjecture 4.4 says folding fails; an inequality is consistent with it, so these are not refutations. |
