# Retro

This repo indexes seven results from October 13 to 23, 2026. Bounds on C42, C44, C68, C70, C82 and C86 from Terence
Tao's [optimization-constants table](https://teorth.github.io/optimizationproblems/), and a cylinder cover for
[problem 100](https://github.com/openai/math/blob/main/lean/docs/100.md) of OpenAI's math release. Each has an exact
certificate and checkers. The work was done with AI models under my direction. None of it is refereed.

## Update, October 30

We went back to the table and filed three new bounds. All three are open pull requests, unrefereed, with the asterisk.

- **C86 ≤ 1.80697883** ([#298](https://github.com/teorth/optimizationproblems/pull/298)). Ours had been passed. Smith's
  criterion does not need the auxiliary polynomials to have real roots, so we allowed nonreal ones. The two doing most
  of the work come from Flammang (2009) and McKee (2011).
- **C44 ≤ 4.1225323803** ([#294](https://github.com/teorth/optimizationproblems/pull/294)), down from our 4.3576549226.
  It changes two steps in Wellens's recurrence and keeps Épi's certificates.
- **C68 ≥ 0.44667** ([#299](https://github.com/teorth/optimizationproblems/pull/299)). It sits directly on David
  Niedbala Giraudin's 0.446 ([#274](https://github.com/teorth/optimizationproblems/pull/274)), which is still open and
  should be credited first.

I also filed [#300](https://github.com/teorth/optimizationproblems/pull/300), which records two C10a bounds by other
people. Those are not mine.

Notes for all three are submitted to Hexagon and are not public yet.

None of this changes what is below. Each one still extends someone else's work, and C42 is still passed. No second
party has checked any of them, so the asterisks stay. For the new C44, a different AI agent wrote a third checker from
the proof text alone. That is better than what I describe below, but it is not a person.

## What we did

I came in through [openai/math](https://github.com/openai/math) in early October, and the crowd around its
integer-multiplication bound. [Rohan Arun](https://x.com/RohanArun) and [Doug Colkitt](https://x.com/0xdoug) posted
community progress and a prompt anyone could run. Then Tao's table, which takes a checkable bound from anyone. I
had not published a paper in about ten years. It was fun to do it again.

At least 11 problems got a real attempt. Seven gave a public bound. Two (C51, C59) gave gains too small to publish.
Two gave nothing. Tao merged six of the pull requests.

## What broke

**Starting from scratch did not work.** Every result that worked extended a published method. C86 added seven small polynomials to the construction of Orloski and Talebizadeh Sardari
([arXiv:2304.10021](https://arxiv.org/abs/2304.10021)), and went from 1.8216 to 1.8117251. C82 builds mostly on
[Épi](https://github.com/BakeLab/Epi-results) from BakeLab. C42 refines Griego, Röhrig and Plata. C44 uses Wellens
and Épi. C70 optimizes Patankar's construction. C68 uses Wikström's moment duality. I do not think any of these has
a new idea in it.

**The gains do not last.** Dennis Koshta posted C86 at most 1.8084990
([#262](https://github.com/teorth/optimizationproblems/pull/262)) five days after ours merged. Same method, 19
polynomials, "in the certificate format of [Pin26]", which is my note. His C42 bound came a day after mine, and
they merged one second apart.

**Novelty was as hard to check as correctness.** My first C82 claim was not a record. Épi had already done it, in a
results repo the table did not list yet.

**The checkers check arithmetic, not the reasoning around it.** C42, C44, C68 and C70 rest on written arguments
that still need a mathematician. For C44 and C70 both checkers came from the same AI model. Nothing is in Lean. On
Hexagon I declared "human understanding: some parts", because that is true.

## What I would do differently

Search the results repos and threads for prior art before claiming a record, not after.

Get a second party on the certificate early. Carlos Toledo replayed C86 and C82 from the published bytes, in two
implementations sharing no code with mine ([#242](https://github.com/teorth/optimizationproblems/pull/242)). That
is worth more than the bound.

And pick problems where a specialist might want to co-own the result. That is what decides whether it becomes
anything.

## Publishing

arXiv got 40,363 submissions in September 2026, about twice September 2024
([arXiv blog](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/)). Since October 1 it allows two new
submissions a month per submitter. Without an institutional email you need a personal endorser. My #100 note went
to arXiv on October 17 and was still on hold when I last checked.

[Hexagon](https://hexagonmath.org/about) is what made this publishable. Mathematicians opened it on September 28.
Its founder [wrote](https://antieau.github.io/2026/10/05/hexagon.html) that arXiv's leadership told them arXiv
would not be the home for these results. It takes AI-generated work, labels human understanding on every record,
and says acceptance "is not a judgment about its correctness, quality, or novelty." All seven notes are there.

I also asked people I know. The authors of the C86 method have not answered my email. A mathematician endorsed me for arXiv math within a day and pointed me to Hexagon. Later he said he would put AI papers only there. Another said
not to put C86 on arXiv, where the author vouches that the work is correct. "Reviewed at summary level" does not
meet that bar. An astrophysicist said his colleagues look at AI papers with a lot of distrust, mostly over volume
and review load.

None of that was about my notes. It is the AI slop backlash, and I think it has a role. It is what pushed the
venues and the labs to build ways to check this stuff.

On October 26 Tao held Toledo's replay and changed the rule. Removing an asterisk now takes a second party, because
"a marker that one party can clear across the whole repository stops distinguishing anything." I think he is right.
The same week OpenAI called its manuscripts "raw research data" and gave each result to outside experts to
shepherd, seeking no academic credit. Anthropic put its 3-SAT paper on Hexagon with the same label as mine. That is
the answer the mathematicians gave me. AI output needs someone in the field to own it.

## Where I think this is going

Finding and certifying a small improvement on a public problem is easy now. Making it count is hard. Most of the
credit belongs to whoever built the construction, and the number may last a week.

For results like these I think the honest end point is a certificate, credit by name, a true human-understanding
label, a table row with its asterisk, and Hexagon. arXiv or a journal should wait for a specialist who has checked
it and wants to co-own it.

The bottleneck is not search anymore. It is people who can check a result and explain it.

## Still open

- Whether any of these should become a refereed paper, and with whom. I have not asked a specialist yet.
- Whether someone independent confirms Toledo's replays, so the C86 and C82 asterisks can come off.
- In mid-October I guessed this was a six-month window before models do it alone. I still do not know.
