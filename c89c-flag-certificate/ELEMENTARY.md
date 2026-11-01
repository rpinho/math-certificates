# Elementary baselines for C89c

Candidate calculations, unrefereed. All methods in this note are classical; no novelty is claimed for them. The stronger computer-assisted result is in PROOF.md. The exact arithmetic below is independently replayed by `verify_baselines.py`.

## Normalization

Let M_k(G) be the number of monochromatic k-subsets in a red/blue colouring of K_n. We use c_k=lim_n min_G M_k(G)/binomial(n,k). This agrees with the live PR #279 for k=6 and #277 for k=5. The denominator is not n^k, and no factor 2^(binomial(k,2)-1) is built into c_k.

## Averaging and vertex deletion

Suppose R(k,k)<=R. Every R-subset contains a monochromatic K_k, so counting pairs (S,C), where |S|=R and C is a monochromatic k-subset of S, yields

    M_k(G) binomial(n-k,R-k) >= binomial(n,R).

Divide by binomial(n,k), use the factorial identity, and obtain c_k>=1/binomial(R,k).

For a stronger finite statement, start with any m>=R vertices. Find a monochromatic k-subset and delete one of its vertices. Repeat while at least R vertices remain. This finds m-R+1 distinct monochromatic k-subsets: after a chosen vertex is deleted, its clique cannot appear in any later step. Hence every m-subset has at least m-R+1 such cliques. Averaging gives

    c_k >= (m-R+1)/binomial(m,k) = f(m).

There is no unproved randomness or graph-density approximation in this step. For all m>=R,

    f(m+1)/f(m)
      = [(m-R+2)/(m-R+1)] [(m+1-k)/(m+1)].

All denominators are positive. Subtracting the right cross-products shows f(m+1)>=f(m) exactly when

    k(R-2)+1 - (k-1)m >= 0.

This proves the global maximum over every integer m>=R, with two adjacent maxima only in the equality case. In particular:

| k | R | maximizing m | exact deletion bound | approximate value |
|---|---|---|---|---|
| 6 | 252 | 301 | 5/98240568426 | 5.0895470986e-11 |
| 6 | 165 | 196 | 1/2277727907 | 4.3903400267e-10 |
| 5 | 46 | 56 | 1/347256 | 2.8797198609e-6 |

These reproduce the unverified lead, but do not exhaust known elementary methods.

## De Caen's stronger hypergraph argument, with every step supplied

This reproduces the classical de Caen bound, quoted in Keevash's survey section 9. We give the proof because simply reporting a stronger number would conceal the existing public method.

Let J be an r-uniform hypergraph on n vertices with no independent set of size R, where n>=R>=r. Its edges will ultimately be the monochromatic K_r vertex sets. Write e=|E(J)| and p=e/binomial(n,r). Call a vertex set independent if it contains no edge of J, and let I_j count independent j-subsets. Every set of size r-1 is independent, so I_{r-1}=binomial(n,r-1)>0. Also I_r=binomial(n,r)-e and I_R=0.

We first prove the following inequality for k>=r whenever I_{k-1}>0:

    (k-r+1)(k+1) I_{k+1}
      >= k^2 I_k^2/I_{k-1} - [(r-1)(n-k)+k] I_k.            (A)

Count ordered pairs (S,T) of k-subsets such that S is independent, T is not, and |S intersect T|=k-1. Denote their number by P. For each independent (k-1)-set C, let a_C be the number of independent k-sets containing it. Then sum_C a_C=k I_k, since every independent k-set has exactly k such subsets. Once C=S intersect T is fixed, there are a_C choices for S and n-k+1-a_C choices for T. Therefore

    P = sum_C a_C(n-k+1-a_C)
      <= (n-k+1) k I_k - k^2 I_k^2/I_{k-1}.                 (B)

The last inequality follows by expanding

    sum_C (a_C - (k I_k/I_{k-1}))^2 >= 0.

For an independent k-set S, let b_S be the number of independent (k+1)-sets containing it. Exactly n-k-b_S vertices x outside S have S union {x} nonindependent. For each such x, some edge E of J is contained in S union {x}; since S is independent, x belongs to E, so E\{x} is an (r-1)-subset of S. Deleting any y in S\(E\{x}) leaves a nonindependent k-set T=S union {x}\{y}. There are k-r+1 such y. Each (S,x,y) specifies a distinct pair (S,T). Also sum_S b_S=(k+1) I_{k+1}. Thus

    P >= (k-r+1) [(n-k) I_k - (k+1) I_{k+1}].             (C)

Combining (B) and (C), moving terms and simplifying gives (A): the coefficient of I_k on the right after simplification is (r-1)(n-k)+k.

Now let s be the largest size of an independent set, so r-1<=s<=R-1. For r<=j<=s+1 define

    d_j = (n-j+1) - j I_j/I_{j-1}.

All denominators are positive: every subset of a largest independent set is independent. Counting extensions also shows j I_j<=(n-j+1)I_{j-1}, so d_j>=0. At the first and last indices,

    d_r=(n-r+1)p,       d_{s+1}=n-s.

If s=r-1, these two expressions already imply p=1, and the desired bound follows. Otherwise divide (A) by I_k>0 for k=r,...,s, rearrange, and obtain

    (k+1) I_{k+1}/I_k
       >= [k (k I_k/I_{k-1}) - ((r-1)(n-k)+k)]/(k-r+1),
    d_{k+1} <= [k/(k-r+1)] d_k.                            (D)

The simplification in (D) uses k(n-k+1)-[(r-1)(n-k)+k]=(k-r+1)(n-k). Iteration gives

    n-s = d_{s+1}
        <= [product_{k=r}^s k/(k-r+1)] d_r
         = binomial(s,r-1) (n-r+1) p.

Since s<=R-1, n-s>=n-R+1 and binomial(s,r-1)<=binomial(R-1,r-1). All quantities being divided by are positive. Consequently

    e/binomial(n,r)
      >= (n-R+1)/[(n-r+1) binomial(R-1,r-1)].               (E)

Apply (E) to the hypergraph of monochromatic K_r sets in a red/blue complete graph. Ramsey's theorem with R(r,r)<=R supplies precisely the required independence-number hypothesis. Let n tend to infinity:

    c_r >= 1/binomial(R-1,r-1).                            (F)

For r=6, R=165 this is

    1/binomial(164,5) = 1/929632032 = 1.0756944313...e-9.

For the fully self-contained classical input R=252 it is

    1/binomial(251,5) = 1/7975914050 = 1.2537747946...e-10.

These are the strongest elementary numerical baselines established in this job, not a claim of optimality among all elementary proofs. De Caen (1983) receives credit for the method.

## Ramsey inputs and dependencies

The classical R(a,b)<=binomial(a+b-2,a-1) follows by induction from R(1,b)=R(a,1)=1 and R(a,b)<=R(a-1,b)+R(a,b-1). To verify the recursion, at a vertex of K_{A+B}, with A=R(a-1,b), B=R(a,b-1), at least A red neighbors or B blue neighbors exist; otherwise their sum would be at most A+B-2 instead of A+B-1. Apply the appropriate smaller Ramsey statement in that neighborhood, and, where necessary, adjoin the vertex. Pascal's identity finishes the induction. Hence R(6,6)<=binomial(10,5)=252 requires no external computational assumption.

The R(6,6)<=165 input is Mackey's 1994 published PhD thesis, *Combinatorial Remedies*, cited by Radziszowski's Small Ramsey Numbers revision 18 (2026), p.8 and reference [Mac]. The thesis computation has not been replayed in this job; this baseline depends on that published theorem. The alternative 252 version is proved above. The survey's newer R(6,6)<=160 is attributed to a personal communication [AnM3] and is excluded here as requested. No candidate SOS result depends on any of these Ramsey inputs.

For C89b, the elementary bounds are far below the published PPSS2024 c5>0.001524. The table's omission problem is therefore specific to C89c in this audit. Conlon 2012's explicit recurrence and the current C89b source are documented in PRIOR_ART.md.
