"""Independently reproduce the n=11 portion of the omega note and BMB paper.
The constructions below are mathematical data transcribed from those sources.
No upstream code is used. Closure is checked using Python sets.
"""
import itertools
import json
from pathlib import Path

def lattice(family):
    assert len(family) == len(set(family))
    f = set(family)
    assert all(a|b in f and a&b in f for a in f for b in f)

def prefix(r):
    return frozenset(range(r))

omega_masks = [
 [0,7,56,63,448,455,504,511],
 [3,31,227,255,1795,1823,2019,2047],
 [1,15,113,127,897,911,1009,1023],
 [0,1,30,31,480,481,510,511],
 [0,7,120,127,1920,1927,2040,2047],
 [0,7,56,63,1984,1991,2040,2047],
 [0,3,7,63,963,967,1023],
 [1,7,15,127,1927,1935,2047],
 [0,3,31,127,899,927,1023],
 [1,3,31,481,483,511,2047]]
omega = [[frozenset(i for i in range(11) if mask & (1<<i)) for mask in f] for f in omega_masks]
for f in omega:
    lattice(f)
    assert len(f) >= 7

balanced = diamond = residual = 0
for word in itertools.product((0,1), repeat=12):
    if sum(word) != 6: continue
    balanced += 1
    witness = None
    for c in (0,1):
        ranks = [r for r in range(12) if word[r] == c]
        for a,b,d in zip(ranks,ranks[1:],ranks[2:]):
            if a+d == 2*b:
                witness = [prefix(r) for r in ranks] + [prefix(a) | frozenset(range(b,d))]
                lattice(witness)
                assert len(witness) == 7 and all(word[len(s)] == c for s in witness)
                break
        if witness: break
    if witness:
        diamond += 1
    else:
        assert any(len({word[len(s)] for s in f}) == 1 for f in omega)
        residual += 1
assert (balanced,diamond,residual) == (924,874,50)
print('OMEGA BASE CASE VERIFIED:',balanced,'balanced words;',diamond,'diamond;',residual,'ten-family cover')

# Table of the current paper: each tuple is the block lengths of one chain.
rows = [('RRR',((1,),(1,))), ('RBRBR',((2,),(2,))),
 ('RBBRBBR',((3,),(3,))), ('RRBBRRBBR',((1,3),(4,))),
 ('RBRRBRBBR',((2,3),(3,))), ('RRBRBBRRBR',((3,),(3,),(3,))),
 ('RBRRBBRRBR',((3,),(3,),(3,))), ('RBBRRBRBBR',((3,),(3,),(3,)))]
variants = []
for word, chains in rows:
    family = [frozenset()]
    offset = 0
    for chain in chains:
        factor = [frozenset()]
        acc = frozenset()
        for length in chain:
            acc = acc | frozenset(range(offset,offset+length))
            offset += length
            factor.append(acc)
        family = [a|b for a in family for b in factor]
    assert offset == len(word)-1
    lattice(family)
    assert len(family) > word.count('R')
    assert all(word[len(s)] == 'R' for s in family)
    ground = frozenset(range(offset))
    for reverse in (False,True):
        w = word[::-1] if reverse else word
        f = [ground-s for s in family] if reverse else family
        for swap in (False,True):
            v = w.translate(str.maketrans('RB','BR')) if swap else w
            variants.append((v,f,'B' if swap else 'R'))

covered = 0
for letters in itertools.product('RB',repeat=12):
    word = ''.join(letters)
    hit = next(((v,f,c,word.index(v)) for v,f,c in variants if v in word),None)
    assert hit, word
    v,f,c,a = hit
    b = a+len(v)-1
    family = [prefix(i) for i in range(12) if (i<a or i>b) and word[i]==c]
    family += [prefix(a) | frozenset(a+x for x in s) for s in f]
    lattice(family)
    assert all(word[len(s)] == c for s in family)
    assert len(family) > word.count(c)
    assert max(len(family),12-word.count(c)) >= 7
    covered += 1
print('BMB EIGHT-GADGET BASE CASE VERIFIED: 8 gadgets;',covered,'rank words; red-blue total >= 13')
Path('certificates/published_lower.json').write_text(json.dumps(dict(
    omega_balanced=balanced,omega_diamond=diamond,omega_residual=residual,
    bmb_gadgets=8,bmb_words=covered),indent=2)+'\n')
