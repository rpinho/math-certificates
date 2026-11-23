"""Project a checked SAT assignment to its equal-distance classes."""
import argparse
from collections import defaultdict

from encoder import Encoding


def projection(n, model):
    enc = Encoding(n, 0)
    truth = set(map(int, open(model).read().split()))
    ranks = [sum(enc.lt(j,i) in truth for j in range(enc.m) if i != j) for i in range(enc.m)]
    classes = defaultdict(list)
    for rank, edge in zip(ranks, enc.edges, strict=True):
        classes[rank].append(edge)
    return [classes[rank] for rank in sorted(classes)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("model")
    args = parser.parse_args()
    for group in projection(args.n, args.model):
        print(" ".join(f"{a}-{b}" for a,b in group))
