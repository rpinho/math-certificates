#include <assert.h>
#include <errno.h>
#include <gmp.h>
#include <inttypes.h>
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef __uint128_t Wide;
typedef uint64_t Word;
enum { MAX_K = 9, MAX_FACTORS = 32, SIEVE_LIMIT = 13000000 };
enum { M1 = 1, M2 = 2, M5 = 4, M6 = 8, LOWER = 16 };

typedef struct { Word prime; unsigned exponent; } Factor;
typedef struct { Factor item[MAX_FACTORS]; unsigned size; } Factors;
typedef struct { Wide p, q; } Fraction;
typedef struct { Word lo, hi; } Bounds;
typedef struct {
    Word m, prefix[MAX_K], nodes[MAX_K + 1], probes, solutions;
    unsigned k, mutant, max_q_bits, max_b_bits;
    Word mandatory_power, max_prefix;
    bool emit, control;
} Search;

static uint32_t *spf;
static uint32_t *primes;
static size_t prime_count;
static const Wide wide_max = (Wide)-1;
static mpz_t zq, zd, za, zb;

static void require(bool condition, const char *message) {
    if (!condition) {
        fprintf(stderr, "skipped=1 invariant=%s\n", message);
        exit(2);
    }
}

static Word read_word(const char *s) {
    require(s[0] >= '0' && s[0] <= '9', "unsigned decimal input");
    char *end;
    errno = 0;
    Word n = strtoull(s, &end, 10);
    require(!errno && !*end, "machine-word input");
    return n;
}

static void print_wide(Wide n) {
    char digits[40];
    unsigned length = 0;
    do {
        digits[length++] = '0' + n % 10;
        n /= 10;
    } while (n);
    while (length) putchar(digits[--length]);
}

static inline Wide div_exact_or_floor(Wide a, Wide b) {
    return (a | b) <= UINT64_MAX ? (Word)a / (Word)b : a / b;
}

static inline Wide rem(Wide a, Wide b) {
    return (a | b) <= UINT64_MAX ? (Word)a % (Word)b : a % b;
}

static Word gcd_word(Word a, Word b) {
    while (b) {
        Word r = a % b;
        a = b;
        b = r;
    }
    return a;
}

static void init_sieve(void) {
    spf = calloc(SIEVE_LIMIT + 1, sizeof(*spf));
    /* Every prime above 2 is odd. This allocation is an upper bound. */
    primes = malloc((SIEVE_LIMIT / 2 + 1) * sizeof(*primes));
    require(spf && primes, "sieve allocation");
    for (uint32_t p = 2; p <= SIEVE_LIMIT; ++p) {
        if (spf[p]) continue;
        spf[p] = p;
        primes[prime_count++] = p;
        if (p > SIEVE_LIMIT / p) continue;
        for (uint32_t n = p * p; n <= SIEVE_LIMIT; n += p)
            if (!spf[n]) spf[n] = p;
    }
}

static void adjust(Factors *f, Word prime, int difference) {
    unsigned i = 0;
    /* Descending order puts the largest prime at the top of divisor DFS. */
    while (i < f->size && f->item[i].prime > prime) ++i;
    if (i < f->size && f->item[i].prime == prime) {
        int exponent = (int)f->item[i].exponent + difference;
        require(exponent >= 0, "factor exponent");
        if (exponent) {
            f->item[i].exponent = (unsigned)exponent;
        } else {
            --f->size;
            memmove(f->item + i, f->item + i + 1, (f->size - i) * sizeof(Factor));
        }
        return;
    }
    require(difference > 0 && f->size < MAX_FACTORS, "factor insertion");
    memmove(f->item + i + 1, f->item + i, (f->size - i) * sizeof(Factor));
    ++f->size;
    f->item[i] = (Factor){prime, (unsigned)difference};
}

static void factor_adjust(Factors *f, Word n, int sign) {
    if (n > SIEVE_LIMIT) {
        for (size_t i = 0; i < prime_count; ++i) {
            Word p = primes[i];
            if (p > n / p) break;
            int exponent = 0;
            while (n % p == 0) {
                ++exponent;
                n /= p;
            }
            if (exponent) adjust(f, p, sign * exponent);
            if (n <= SIEVE_LIMIT) break;
        }
        if (n > SIEVE_LIMIT) {
            require(n / primes[prime_count - 1] < primes[prime_count - 1],
                    "sieve covers the square root of the unfactored cofactor");
            adjust(f, n, sign);
            return;
        }
    }
    while (n > 1) {
        Word p = spf[n];
        int exponent = 0;
        do {
            ++exponent;
            n /= p;
        } while (spf[n] == p);
        adjust(f, p, sign * exponent);
    }
}

static void check_factors(const Factors *f, Wide q) {
    Wide product = 1;
    for (unsigned i = 0; i < f->size; ++i) {
        const Factor factor = f->item[i];
        for (unsigned e = 0; e < factor.exponent; ++e)
            require(!__builtin_mul_overflow(product, (Wide)factor.prime, &product),
                    "factor product overflow");
    }
    require(product == q, "factorization multiply-back");
}

static Fraction subtract_unit(Fraction z, Word n, Factors *f) {
    Word g = gcd_word((Word)rem(z.q, n), n);
    Word scale = n / g;
    Wide q0 = div_exact_or_floor(z.q, g);
    require(z.q <= div_exact_or_floor(wide_max, scale), "prefix rational overflow");
    Wide p = z.p * scale - q0;
    Wide q = z.q * scale;
    Word cancel = gcd_word((Word)rem(p, g), g);
    if (f) {
        factor_adjust(f, scale, 1);
        factor_adjust(f, cancel, -1);
    }
    return (Fraction){div_exact_or_floor(p, cancel), div_exact_or_floor(q, cancel)};
}

static Bounds bounds(const Search *s, Fraction z, unsigned left, Word previous) {
    if (!z.p) return (Bounds){1, 0};
    require(z.q <= div_exact_or_floor(wide_max, left), "next-denominator bound overflow");
    Wide hi = div_exact_or_floor(left * z.q - 1, z.p);
    if (s->mandatory_power && !rem(z.q, s->mandatory_power)) {
        Wide reduced_q = div_exact_or_floor(z.q, s->mandatory_power);
        if (z.p > reduced_q) {
            Wide cap = div_exact_or_floor((left - 1) * z.q, z.p - reduced_q);
            if (cap < hi) hi = cap;
        }
    }
    Wide lo = div_exact_or_floor(z.q, z.p) + (s->mutant & LOWER ? 2 : 1);
    if (lo <= previous) lo = (Wide)previous + 1;
    if (lo > hi) return (Bounds){1, 0};
    require(hi < UINT64_MAX, "next denominator exceeds word range");
    return (Bounds){(Word)lo, (Word)hi};
}

static void set_wide(mpz_t out, Wide n) {
    Word words[] = {(Word)n, (Word)(n >> 64)};
    mpz_import(out, 2, -1, sizeof(Word), 0, 0, words);
}

static bool permitted(const Search *s, Wide a, const mpz_t b, unsigned depth) {
    if (!(s->mutant & M2) && (a == s->m || mpz_cmp_ui(b, s->m) == 0)) return false;
    if ((s->mutant & M5) && mpz_sizeinbase(b, 2) > 64) return false;
    if (!(s->mutant & M6) || !s->m) return true;
    if ((a && !rem(a, s->m)) || mpz_divisible_ui_p(b, s->m)) return true;
    for (unsigned i = 0; i < depth; ++i)
        if (s->prefix[i] % s->m == 0) return true;
    return false;
}

static void solution(Search *s, Wide a, const mpz_t b, unsigned depth) {
    if (!permitted(s, a, b, depth)) return;
    ++s->solutions;
    unsigned bits = (unsigned)mpz_sizeinbase(b, 2);
    if (bits > s->max_b_bits) s->max_b_bits = bits;
    if (!s->emit) return;
    fputs("S", stdout);
    unsigned i = 0;
    bool included = s->m == 0;
    for (; i < depth; ++i) {
        if (!included && s->m <= s->prefix[i]) {
            printf(" %" PRIu64, s->m);
            included = true;
        }
        printf(" %" PRIu64, s->prefix[i]);
    }
    if (a) {
        if (!included && s->m <= a) {
            printf(" %" PRIu64, s->m);
            included = true;
        }
        putchar(' ');
        print_wide(a);
    }
    if (!included && mpz_cmp_ui(b, s->m) >= 0) {
        printf(" %" PRIu64, s->m);
        included = true;
    }
    gmp_printf(" %Zd", b);
    if (!included) printf(" %" PRIu64, s->m);
    putchar('\n');
}

typedef struct {
    Search *search;
    const Factors *factors;
    Fraction z;
    Wide min, max;
    unsigned depth;
} Tail;

static inline void test_divisor(Tail *tail, Wide d) {
    if (d < tail->min) return;
    Search *s = tail->search;
    ++s->probes;
    Wide sum = tail->z.q + d;
    if (rem(sum, tail->z.p)) return;
    Wide a = div_exact_or_floor(sum, tail->z.p);
    if (a == s->m && !(s->mutant & M2)) return;
    /* b=a*q/d. GMP keeps the full product and the full last denominator. */
    set_wide(za, a);
    set_wide(zq, tail->z.q);
    set_wide(zd, d);
    mpz_mul(zb, za, zq);
    /* gcd(p,q)=1 and d divides q^2 imply d divides a*q. */
    require(mpz_divisible_p(zb, zd), "divisor-generated candidate is integral");
    mpz_divexact(zb, zb, zd);
    require(mpz_cmp(zb, za) > 0, "divisor bound enforces strict order");
    solution(s, a, zb, tail->depth);
}

static void divisors(Tail *tail, unsigned index, Wide product) {
    if (index == tail->factors->size) {
        test_divisor(tail, product);
        return;
    }
    Factor f = tail->factors->item[index];
    Wide limit = div_exact_or_floor(tail->max, f.prime);
    unsigned exponent = 0;
    for (;;) {
        divisors(tail, index + 1, product);
        if (exponent == 2 * f.exponent || product > limit) break;
        product *= f.prime;
        ++exponent;
    }
}

static void two_terms(Search *s, Fraction z, const Factors *f, unsigned depth) {
    Wide lower = depth ? (Wide)s->prefix[depth - 1] + (s->mutant & M1 ? 2 : 1) : 2;
    if (s->mutant & LOWER) {
        Wide lo = div_exact_or_floor(z.q, z.p) + 2;
        if (lo > lower) lower = lo;
    }
    require(z.q <= wide_max / 2, "two-term bound overflow");
    if (lower > div_exact_or_floor(2 * z.q - 1, z.p)) return;
    Wide pa = z.p * lower;
    Wide min = pa > z.q ? pa - z.q : 1;
    Tail tail = {s, f, z, min, z.q - 1, depth};
    divisors(&tail, 0, 1);
}

static void search(Search *s, Fraction z, const Factors *f, unsigned depth,
                   unsigned left, Word shard_lo, Word shard_hi) {
    ++s->nodes[left];
    check_factors(f, z.q);
    Word upper_half = (Word)(z.q >> 64);
    unsigned bits = upper_half ? 128 - __builtin_clzll(upper_half) : 64 - __builtin_clzll((Word)z.q);
    if (bits > s->max_q_bits) s->max_q_bits = bits;
    if (left == 2) {
        if (z.p) two_terms(s, z, f, depth);
        return;
    }
    if (left == 1) {
        Word previous = depth ? s->prefix[depth - 1] : 1;
        if (z.p == 1 && z.q > previous && (z.q != s->m || (s->mutant & M2))) {
            set_wide(zb, z.q);
            solution(s, 0, zb, depth);
        }
        return;
    }
    Word previous = depth ? s->prefix[depth - 1] : 1;
    Bounds range = bounds(s, z, left, previous);
    if (range.lo < shard_lo) range.lo = shard_lo;
    if (range.hi > shard_hi) range.hi = shard_hi;
    for (Word n = range.lo; n <= range.hi; ++n) {
        if (n == s->m) continue;
        if (!s->control) require(n <= SIEVE_LIMIT, "main prime-factor source bound");
        Factors next = *f;
        s->prefix[depth] = n;
        if (n > s->max_prefix) s->max_prefix = n;
        Fraction rest = subtract_unit(z, n, &next);
        search(s, rest, &next, depth + 1, left - 1, 0, UINT64_MAX);
    }
}

static Word prime_power(const Factors *f) {
    Word largest = 0;
    for (unsigned i = 0; i < f->size; ++i) {
        Word power = 1;
        for (unsigned e = 0; e < f->item[i].exponent; ++e) power *= f->item[i].prime;
        if (power > largest) largest = power;
    }
    return largest;
}

static void run_line(char *line, bool emit, unsigned mutant) {
    Word input[2 + MAX_K + 2];
    unsigned count = 0;
    for (char *tok = strtok(line, " \t\r\n"); tok; tok = strtok(NULL, " \t\r\n")) {
        require(count < sizeof(input) / sizeof(*input), "task size");
        input[count++] = read_word(tok);
    }
    if (!count) return;
    require(count >= 4 && input[1] >= 3 && input[1] <= MAX_K && input[0] != 1, "task header");
    unsigned depth = count - 4;
    Search s = {.m = input[0], .k = (unsigned)input[1], .emit = emit, .mutant = mutant,
                .control = input[0] != 13856993 || input[1] != 9};
    unsigned total = s.k - (s.m != 0);
    require(depth < total, "prefix leaves at least one term");
    Fraction z = s.m ? (Fraction){s.m - 1, s.m} : (Fraction){1, 1};
    Factors f = {0};
    if (s.m) factor_adjust(&f, s.m, 1);
    check_factors(&f, z.q);
    s.mandatory_power = prime_power(&f);
    Word previous = 1;
    for (unsigned i = 0; i < depth; ++i) {
        Word n = input[i + 2];
        require(n > previous && n != s.m, "ordered valid prefix");
        require((Wide)n > div_exact_or_floor(z.q, z.p), "positive prefix remainder");
        if (!s.control) require(n <= SIEVE_LIMIT, "main prefix factor bound");
        s.prefix[i] = previous = n;
        z = subtract_unit(z, n, &f);
        check_factors(&f, z.q);
        s.max_prefix = n;
    }
    Word lo = input[count - 2], hi = input[count - 1];
    require(lo <= hi, "shard bounds");
    if (total - depth < 3) require(lo == 0 && hi == UINT64_MAX, "tail shard bounds");
    search(&s, z, &f, depth, total - depth, lo, hi);
    printf("R %" PRIu64 " %u %" PRIu64 " %" PRIu64 " 0", s.m, s.k, s.solutions, s.probes);
    for (unsigned i = 1; i <= MAX_K; ++i) printf(" %" PRIu64, s.nodes[i]);
    printf(" %u %u %" PRIu64 "\n", s.max_q_bits, s.max_b_bits, s.max_prefix);
    fflush(stdout);
}

int main(int argc, char **argv) {
    require(argc == 3, "usage: solver EMIT MUTANT_MASK < tasks");
    bool emit = read_word(argv[1]) != 0;
    unsigned mutant = (unsigned)read_word(argv[2]);
    init_sieve();
    mpz_inits(zq, zd, za, zb, NULL);
    char *line = NULL;
    size_t capacity = 0;
    while (getline(&line, &capacity, stdin) >= 0) run_line(line, emit, mutant);
    require(!ferror(stdin), "task input read");
    free(line);
    mpz_clears(zq, zd, za, zb, NULL);
    free(primes);
    free(spf);
    return 0;
}
