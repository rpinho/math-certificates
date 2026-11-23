/* Enumerate all representations of 1 without fixing any denominator.
 * The last two terms are found by scanning a, then testing the residual.
 * This code shares neither the solver's rational arithmetic nor its pruning.
 */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint64_t Number;
typedef __uint128_t Product;
static Number terms[7];
static unsigned length;
static Number count;

static Number gcd(Number a, Number b) {
    return b ? gcd(b, a % b) : a;
}

static void visit(Number numerator, Number denominator, unsigned depth) {
    Number previous = depth ? terms[depth - 1] : 1;
    unsigned remaining = length - depth;
    if (remaining == 1) {
        if (numerator != 1 || denominator <= previous) return;
        terms[depth] = denominator;
        ++count;
        for (unsigned i = 0; i < length; ++i)
            printf("%s%" PRIu64, i ? " " : "", terms[i]);
        putchar('\n');
        return;
    }
    Number lower = denominator / numerator + 1;
    if (lower <= previous) lower = previous + 1;
    Product bound = ((Product)remaining * denominator - 1) / numerator;
    if (bound >= UINT64_MAX) exit(2);
    for (Number a = lower; a <= (Number)bound; ++a) {
        Product p = (Product)numerator * a - denominator;
        Product q = (Product)denominator * a;
        if (q > UINT64_MAX) exit(2);
        terms[depth] = a;
        if (remaining == 2) {
            if (q % p == 0 && q / p > a)
                visit(1, (Number)(q / p), depth + 1);
        } else {
            Number reduction = gcd((Number)p, (Number)q);
            visit((Number)p / reduction, (Number)q / reduction, depth + 1);
        }
    }
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    length = (unsigned)atoi(argv[1]);
    if (length < 3 || length > 7) return 2;
    visit(1, 1, 0);
    fprintf(stderr, "k=%u count=%" PRIu64 "\n", length, count);
    return ferror(stdout) ? 2 : 0;
}
