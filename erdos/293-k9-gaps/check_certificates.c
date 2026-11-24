/* Standalone checker for the public v9 certificate text format. */
#include <gmp.h>
#include <ctype.h>
#include <errno.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { TERMS = 9 };
static mpz_t denominators[TERMS];
static mpq_t total, unit;

static unsigned long argument(const char *s) {
    char *end;
    errno = 0;
    if (!isdigit((unsigned char)*s)) exit(2);
    unsigned long n = strtoul(s, &end, 10);
    if (errno || *end) exit(2);
    return n;
}

static char *skip_space(char *s) {
    while (isspace((unsigned char)*s)) ++s;
    return s;
}

static const char *validate(char *line, unsigned long *label) {
    if (!isdigit((unsigned char)*line)) return "label";
    char *cursor;
    errno = 0;
    *label = strtoul(line, &cursor, 10);
    if (errno || *label < 2 || *cursor != ':') return "label";
    ++cursor;
    bool member = false;
    for (unsigned i = 0; i < TERMS; ++i) {
        cursor = skip_space(cursor);
        if (!isdigit((unsigned char)*cursor)) return "term_count_or_token";
        char *end = cursor + 1;
        while (isdigit((unsigned char)*end)) ++end;
        if (*end && !isspace((unsigned char)*end)) return "term_token";
        char delimiter = *end;
        *end = 0;
        if (mpz_set_str(denominators[i], cursor, 10) || mpz_cmp_ui(denominators[i], 2) < 0)
            return "term_value";
        *end = delimiter;
        cursor = end;
        for (unsigned j = 0; j < i; ++j)
            if (mpz_cmp(denominators[i], denominators[j]) == 0) return "duplicate_term";
        if (mpz_cmp_ui(denominators[i], *label) == 0) member = true;
    }
    if (*skip_space(cursor)) return "extra_token";
    if (!member) return "label_not_a_denominator";
    mpq_set_ui(total, 0, 1);
    for (unsigned i = 0; i < TERMS; ++i) {
        mpz_set(mpq_denref(unit), denominators[i]);
        mpq_add(total, total, unit);
    }
    return mpq_cmp_ui(total, 1, 1) == 0 ? NULL : "sum";
}

int main(int argc, char **argv) {
    if (argc != 4) return 2;
    unsigned long first = argument(argv[1]), last = argument(argv[2]), absent = argument(argv[3]);
    if (first < 2 || last < first || last >= UINT32_MAX) return 2;
    size_t size = last - first + 1;
    unsigned char *seen = calloc(size, 1);
    unsigned char *seen_term = calloc(size, 1);
    if (!seen || !seen_term) return 2;
    for (unsigned i = 0; i < TERMS; ++i) mpz_init(denominators[i]);
    mpq_inits(total, unit, NULL);
    mpq_set_ui(unit, 1, 1);
    char *line = NULL;
    size_t capacity = 0;
    unsigned long lineno = 0, valid = 0, bad = 0, duplicate_labels = 0;
    unsigned long covered = 0, missing = 0, outside = 0, comments = 0, blanks = 0;
    unsigned long forbidden = 0, out_of_range_low = 0, out_of_range_high = 0;
    ssize_t length;
    while ((length = getline(&line, &capacity, stdin)) >= 0) {
        ++lineno;
        char *s = skip_space(line);
        if (memchr(line, 0, (size_t)length)) {
            ++bad;
            printf("bad line=%lu reason=embedded_nul\n", lineno);
            continue;
        }
        if (*s == '#') { ++comments; continue; }
        if (!*s) { ++blanks; continue; }
        unsigned long m = 0;
        const char *error = validate(s, &m);
        if (error) {
            ++bad;
            printf("bad line=%lu label=%lu reason=%s\n", lineno, m, error);
            continue;
        }
        ++valid;
        for (unsigned i = 0; i < TERMS; ++i) {
            if (mpz_cmp_ui(denominators[i], first) < 0 ||
                mpz_cmp_ui(denominators[i], last) > 0) continue;
            unsigned long n = mpz_get_ui(denominators[i]);
            seen_term[n - first] = 1;
        }
        /* Check denominators even on rows whose index is outside the requested range. */
        if (absent) {
            for (unsigned i = 0; i < TERMS; ++i) {
                if (mpz_cmp_ui(denominators[i], absent) != 0) continue;
                printf("target_found line=%lu label=%lu", lineno, m);
                for (unsigned j = 0; j < TERMS; ++j) gmp_printf(" %Zd", denominators[j]);
                putchar('\n');
                ++forbidden;
            }
        }
        if (m >= first && m <= last) {
            if (seen[m - first]) {
                ++duplicate_labels;
            } else {
                seen[m - first] = 1;
                ++covered;
            }
        } else {
            ++outside;
            if (!out_of_range_low || m < out_of_range_low) out_of_range_low = m;
            if (m > out_of_range_high) out_of_range_high = m;
        }
    }
    bool io_error = ferror(stdin);
    for (unsigned long m = first; m <= last; ++m) {
        if (!seen[m - first]) {
            ++missing;
            printf("missing m=%lu seen_as_term=%u\n", m, seen_term[m - first]);
        }
    }
    printf("first=%lu last=%lu input_lines=%lu comments=%lu blanks=%lu valid=%lu covered=%lu "
           "missing=%lu bad=%lu duplicate_labels=%lu outside=%lu outside_min=%lu outside_max=%lu "
           "target_found=%lu input_error=%d\n",
           first, last, lineno, comments, blanks, valid, covered, missing, bad, duplicate_labels,
           outside, out_of_range_low, out_of_range_high, forbidden, io_error);
    free(line);
    free(seen);
    free(seen_term);
    mpq_clears(total, unit, NULL);
    for (unsigned i = 0; i < TERMS; ++i) mpz_clear(denominators[i]);
    return io_error || ferror(stdout) ? 2 : (bad || forbidden) ? 1 : 0;
}
