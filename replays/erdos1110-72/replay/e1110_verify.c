/* Exact replay of the equations in the staged README. Apple clang, C11 + int128. */
#include <errno.h>
#include <float.h>
#include <inttypes.h>
#include <limits.h>
#include <math.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

_Static_assert(sizeof(float) == 4 && FLT_RADIX == 2 && FLT_MANT_DIG == 24 &&
               FLT_MAX_EXP == 128, "binary32 float required");

enum { MAX_S = 11, MAX_H = 10, MAX_P = 1 << MAX_S, SCALE = 1 << 20 };
typedef __int128 Wide;
typedef enum { STANDARD, LOW_VALUE, LAST_GAMMA, POSITIVE_GAMMA } Rule;
typedef enum { AWAY, EVEN, UP } Rounding;

typedef struct {
    unsigned c, h, length;
    uint8_t alpha[MAX_H], gamma[MAX_H];
    uint64_t value;
} Chain;

typedef struct {
    unsigned s, p, H, window, min_height[MAX_P];
    uint64_t mask, power[MAX_H + 1], inverse[MAX_H + 1], value_power[MAX_H + 1];
    Rule rule;
    Chain *items;
    size_t count, capacity, start[MAX_P + 1];
} Family;

typedef struct {
    uint64_t ties, negative_ties;
    int64_t minimum, maximum;
} RoundStats;

typedef struct {
    const Family *family;
    const int64_t *table, *rows;
    int64_t *drifts;
    bool b_major;
    time_t deadline;
    atomic_uint next_c;
} Sweep;

typedef struct {
    Sweep *sweep;
    int64_t maximum;
    uint64_t states, lookaheads, maximum_count;
    unsigned c, b;
} Worker;

static void fail(const char *message)
{
    fprintf(stderr, "%s\n", message);
    exit(EXIT_FAILURE);
}

static uint64_t natural(const char *input)
{
    char *end;
    errno = 0;
    if (*input < '0' || *input > '9') fail("expected an unsigned integer");
    uint64_t result = strtoull(input, &end, 10);
    if (errno || *end) fail("invalid unsigned integer");
    return result;
}

static int64_t signed_integer(const char *input)
{
    char *end;
    errno = 0;
    int64_t result = strtoll(input, &end, 10);
    if (errno || end == input || *end) fail("invalid signed integer");
    return result;
}

static void *allocate(size_t count, size_t size)
{
    if (size && count > SIZE_MAX / size) fail("allocation size overflow");
    void *memory = malloc(count * size);
    if (!memory) fail("allocation failed");
    return memory;
}

static int64_t narrow(Wide value)
{
    if (value < INT64_MIN || value > INT64_MAX) fail("signed 64-bit overflow");
    return (int64_t)value;
}

static FILE *open_file(const char *path, const char *mode)
{
    FILE *file = fopen(path, mode);
    if (!file) {
        perror(path);
        exit(EXIT_FAILURE);
    }
    return file;
}

static void close_file(FILE *file)
{
    if (fclose(file)) fail("file close failed");
}

static uint64_t odd_inverse(uint64_t n, unsigned bits)
{
    uint64_t inverse = 1;
    for (unsigned bit = 1; bit < bits; ++bit) {
        if ((n * inverse) & (UINT64_C(1) << bit)) inverse |= UINT64_C(1) << bit;
    }
    return inverse;
}

static Rule parse_rule(const char *name)
{
    if (!strcmp(name, "standard")) return STANDARD;
    if (!strcmp(name, "low-value")) return LOW_VALUE;
    if (!strcmp(name, "last-gamma")) return LAST_GAMMA;
    if (!strcmp(name, "positive-gamma")) return POSITIVE_GAMMA;
    fail("unknown transition rule");
    return STANDARD;
}

static Family new_family(uint64_t s, uint64_t H, uint64_t window, Rule rule)
{
    if (s < 1 || s > MAX_S || H < 1 || H > MAX_H || window > MAX_H)
        fail("unsupported family parameters");
    Family family = {.s = (unsigned)s, .p = 1u << s, .H = (unsigned)H,
                     .window = (unsigned)window, .rule = rule};
    family.mask = (UINT64_C(1) << (3 * s)) - 1;
    uint64_t inverse_seven = odd_inverse(7, 3 * family.s);
    uint64_t term = rule == POSITIVE_GAMMA ? 7 : inverse_seven;
    family.power[0] = family.inverse[0] = family.value_power[0] = 1;
    for (unsigned h = 1; h <= H; ++h) {
        family.power[h] = 7 * family.power[h - 1];
        family.inverse[h] = (inverse_seven * family.inverse[h - 1]) & family.mask;
        family.value_power[h] = (term * family.value_power[h - 1]) & family.mask;
    }
    for (unsigned c = 0; c < family.p; ++c) family.min_height[c] = UINT_MAX;
    return family;
}

static void append(Family *family, const Chain *chain)
{
    if (family->count == family->capacity) {
        size_t capacity = family->capacity ? 2 * family->capacity : 1024;
        if (capacity < family->capacity || capacity > SIZE_MAX / sizeof(Chain))
            fail("chain count overflow");
        Chain *items = realloc(family->items, capacity * sizeof(Chain));
        if (!items) fail("chain allocation failed");
        family->items = items;
        family->capacity = capacity;
    }
    family->items[family->count++] = *chain;
}

static void enumerate(Family *family, Chain chain, unsigned a0, unsigned g0)
{
    chain.c = (unsigned)(chain.value & (family->p - 1));
    append(family, &chain);
    if (chain.h < family->min_height[chain.c]) family->min_height[chain.c] = chain.h;
    for (unsigned a = a0; a < family->s; ++a) {
        for (unsigned g = g0; g < family->H; ++g) {
            Chain child = chain;
            child.alpha[child.length] = (uint8_t)a;
            child.gamma[child.length++] = (uint8_t)g;
            child.h = g + 1;
            child.value = (chain.value + (family->value_power[g] << a)) & family->mask;
            enumerate(family, child, a + 1, g + 1);
        }
    }
}

static int compare_chains(const void *left, const void *right)
{
    const Chain *a = left, *b = right;
    if (a->c != b->c) return a->c < b->c ? -1 : 1;
    for (unsigned i = 0; i < a->length && i < b->length; ++i) {
        if (a->alpha[i] != b->alpha[i]) return a->alpha[i] < b->alpha[i] ? -1 : 1;
        if (a->gamma[i] != b->gamma[i]) return a->gamma[i] < b->gamma[i] ? -1 : 1;
    }
    return (int)a->length - (int)b->length;
}

static void index_and_validate(Family *family)
{
    qsort(family->items, family->count, sizeof(Chain), compare_chains);
    size_t cursor = 0;
    for (unsigned c = 0; c < family->p; ++c) {
        family->start[c] = cursor;
        while (cursor < family->count && family->items[cursor].c == c) {
            if (cursor && compare_chains(&family->items[cursor - 1], &family->items[cursor]) == 0)
                fail("duplicate chain");
            ++cursor;
        }
        if (family->start[c] == cursor) {
            fprintf(stderr, "uncovered residue %u\n", c);
            exit(EXIT_FAILURE);
        }
    }
    family->start[family->p] = cursor;
    if (cursor != family->count) fail("residue outside state space");
}

static void make_chains(Family *family)
{
    enumerate(family, (Chain){0}, 0, 0);
    size_t kept = 0;
    for (size_t i = 0; i < family->count; ++i) {
        Chain chain = family->items[i];
        if (chain.h <= family->min_height[chain.c] + family->window)
            family->items[kept++] = chain;
    }
    family->count = kept;
    index_and_validate(family);
}

static void write_chains(const Family *family, const char *path)
{
    FILE *file = open_file(path, "w");
    for (size_t i = 0; i < family->count; ++i) {
        const Chain *chain = &family->items[i];
        fprintf(file, "%u %u", chain->c, chain->length);
        for (unsigned j = 0; j < chain->length; ++j)
            fprintf(file, " %u %u", chain->alpha[j], chain->gamma[j]);
        fputc('\n', file);
    }
    if (ferror(file)) fail("chain write failed");
    close_file(file);
}

static void read_chains(Family *family, const char *path)
{
    FILE *file = open_file(path, "r");
    Chain chain;
    int fields;
    while ((fields = fscanf(file, "%u %u", &chain.c, &chain.length)) == 2) {
        if (chain.c >= family->p || chain.length > family->H) fail("invalid chain header");
        chain.value = chain.h = 0;
        for (unsigned j = 0; j < chain.length; ++j) {
            unsigned a, g;
            if (fscanf(file, "%u %u", &a, &g) != 2) fail("incomplete chain");
            if (a >= family->s) fail("alpha outside block");
            if (g >= family->H) fail("height exceeds H");
            if (j && a == chain.alpha[j - 1]) fail("duplicate alpha");
            if (j && (a < chain.alpha[j - 1] || g <= chain.gamma[j - 1]))
                fail("pairs do not form a chain");
            chain.alpha[j] = (uint8_t)a;
            chain.gamma[j] = (uint8_t)g;
            chain.h = g + 1;
            chain.value = (chain.value + (family->value_power[g] << a)) & family->mask;
        }
        if ((chain.value & (family->p - 1)) != chain.c) fail("chain residue mismatch");
        append(family, &chain);
    }
    if (fields != EOF || ferror(file)) fail("malformed chain list");
    close_file(file);
    index_and_validate(family);
}

static Rounding parse_rounding(const char *name)
{
    if (!strcmp(name, "away")) return AWAY;
    if (!strcmp(name, "even")) return EVEN;
    if (!strcmp(name, "up")) return UP;
    fail("unknown rounding");
    return AWAY;
}

static bool parse_layout(const char *name)
{
    if (!strcmp(name, "cb")) return false;
    if (!strcmp(name, "bc")) return true;
    fail("unknown layout");
    return false;
}

static int64_t *read_table(const Family *family, const char *path,
                           Rounding rounding, RoundStats *stats)
{
    size_t count = (size_t)family->p * family->p;
    int64_t *table = allocate(count, sizeof(*table));
    FILE *file = open_file(path, "rb");
    *stats = (RoundStats){.minimum = INT64_MAX, .maximum = INT64_MIN};
    // This bound leaves room for all candidates, their sum, the subtraction,
    // and the strict threshold products. The inner SIMD loops need no traps.
    const int64_t limit = INT64_MAX / (4 * family->p) - family->H * SCALE;
    for (size_t i = 0; i < count; ++i) {
        unsigned char bytes[4];
        if (fread(bytes, 1, sizeof(bytes), file) != sizeof(bytes)) fail("short table");
        uint32_t bits = (uint32_t)bytes[0] | (uint32_t)bytes[1] << 8 |
                        (uint32_t)bytes[2] << 16 | (uint32_t)bytes[3] << 24;
        float value;
        memcpy(&value, &bits, sizeof(value));
        double scaled = ldexp((double)value, 20);
        if (!isfinite(scaled) || fabs(scaled) >= (double)limit)
            fail("non-finite or out-of-range table entry");
        int64_t integer = llround(scaled);
        if (scaled - floor(scaled) == 0.5) {
            ++stats->ties;
            if (scaled < 0) ++stats->negative_ties;
            if ((rounding == EVEN && integer % 2 != 0) ||
                (rounding == UP && scaled < 0))
                integer += scaled < 0 ? 1 : -1;
        }
        table[i] = integer;
        if (integer < stats->minimum) stats->minimum = integer;
        if (integer > stats->maximum) stats->maximum = integer;
    }
    if (fgetc(file) != EOF || ferror(file)) fail("table length mismatch");
    close_file(file);
    return table;
}

static void write_table(const int64_t *table, size_t count, const char *path)
{
    FILE *file = open_file(path, "wb");
    for (size_t i = 0; i < count; ++i) {
        uint64_t bits = (uint64_t)table[i];
        unsigned char bytes[8];
        for (unsigned j = 0; j < 8; ++j) bytes[j] = (unsigned char)(bits >> (8 * j));
        if (fwrite(bytes, 1, sizeof(bytes), file) != sizeof(bytes)) fail("table write failed");
    }
    close_file(file);
}

static int64_t get(const Sweep *sweep, unsigned c, unsigned b)
{
    unsigned p = sweep->family->p;
    return sweep->table[sweep->b_major ? b * p + c : c * p + b];
}

static unsigned exponent(const Family *family, unsigned h)
{
    return family->rule == LAST_GAMMA && h ? h - 1 : h;
}

static uint64_t base_transition(const Family *family, unsigned b, const Chain *chain)
{
    // z-v = P*(b - floor(v/P) + P*u), since the two low digits agree.
    uint64_t high_value = family->rule == LOW_VALUE ? 0 : chain->value >> family->s;
    uint64_t difference = (uint64_t)b - high_value;
    return (difference * family->power[exponent(family, chain->h)]) &
           (family->mask >> family->s);
}

static int64_t *make_rows(const Sweep *sweep)
{
    const Family *family = sweep->family;
    unsigned p = family->p;
    int64_t *rows = allocate((size_t)(family->H + 1) * p * (2 * p), sizeof(*rows));
    for (unsigned h = 0; h <= family->H; ++h) {
        uint64_t multiplier = family->power[exponent(family, h)];
        int64_t cost = (int64_t)h * SCALE;
        for (unsigned c = 0; c < p; ++c) {
            int64_t *row = rows + ((size_t)h * p + c) * (2 * p);
            for (unsigned u = 0; u < p; ++u) {
                unsigned b = (unsigned)((multiplier * u) & (p - 1));
                row[u] = row[u + p] = get(sweep, c, b) + cost;
            }
        }
    }
    return rows;
}

static int64_t fast_state(const Sweep *sweep, unsigned c, unsigned b)
{
    const Family *family = sweep->family;
    unsigned p = family->p;
    int64_t minima[MAX_P];
    for (unsigned u = 0; u < p; ++u) minima[u] = INT64_MAX;
    for (size_t i = family->start[c]; i < family->start[c + 1]; ++i) {
        const Chain *chain = &family->items[i];
        uint64_t packed = base_transition(family, b, chain);
        unsigned next_c = (unsigned)(packed & (p - 1));
        uint64_t inverse = family->inverse[exponent(family, chain->h)];
        unsigned offset = (unsigned)(((packed >> family->s) * inverse) & (p - 1));
        const int64_t *row = sweep->rows + ((size_t)chain->h * p + next_c) * (2 * p) + offset;
        for (unsigned u = 0; u < p; ++u)
            minima[u] = minima[u] < row[u] ? minima[u] : row[u];
    }
    int64_t sum = 0;
    for (unsigned u = 0; u < p; ++u) sum += minima[u];
    return narrow((Wide)sum - (Wide)p * get(sweep, c, b));
}

static int64_t direct_state(const Sweep *sweep, unsigned c, unsigned b)
{
    const Family *family = sweep->family;
    unsigned p = family->p;
    size_t start = family->start[c], stop = family->start[c + 1];
    int64_t sum = 0;
    for (unsigned u = 0; u < p; ++u) {
        int64_t minimum = INT64_MAX;
        for (size_t i = start; i < stop; ++i) {
            const Chain *chain = &family->items[i];
            uint64_t multiplier = family->power[exponent(family, chain->h)];
            uint64_t packed = base_transition(family, b, chain) + multiplier * u * p;
            unsigned next_c = (unsigned)(packed & (p - 1));
            unsigned next_b = (unsigned)((packed >> family->s) & (p - 1));
            int64_t candidate = narrow((Wide)chain->h * SCALE + get(sweep, next_c, next_b));
            if (candidate < minimum) minimum = candidate;
        }
        sum = narrow((Wide)sum + minimum);
    }
    return narrow((Wide)sum - (Wide)p * get(sweep, c, b));
}

static void *work(void *argument)
{
    Worker *worker = argument;
    Sweep *sweep = worker->sweep;
    unsigned p = sweep->family->p;
    worker->maximum = INT64_MIN;
    for (;;) {
        unsigned c = atomic_fetch_add_explicit(&sweep->next_c, 1, memory_order_relaxed);
        if (c >= p) break;
        if (time(NULL) >= sweep->deadline) fail("sweep deadline reached");
        for (unsigned b = 0; b < p; ++b) {
            int64_t drift = fast_state(sweep, c, b);
            if (sweep->drifts) sweep->drifts[c * p + b] = drift;
            if (drift > worker->maximum) {
                worker->maximum = drift;
                worker->maximum_count = 0;
                worker->c = c;
                worker->b = b;
            }
            if (drift == worker->maximum) ++worker->maximum_count;
            ++worker->states;
            worker->lookaheads += p;
        }
    }
    return NULL;
}

static uint64_t state_number(const Worker *worker)
{
    return (uint64_t)worker->c * worker->sweep->family->p + worker->b;
}

static Worker full_sweep(Sweep *sweep, unsigned threads)
{
    pthread_t ids[5];
    Worker workers[6] = {{0}};
    for (unsigned i = 0; i < threads; ++i) workers[i].sweep = sweep;
    for (unsigned i = 1; i < threads; ++i)
        if (pthread_create(&ids[i - 1], NULL, work, &workers[i])) fail("pthread_create failed");
    work(&workers[0]);
    Worker result = workers[0];
    for (unsigned i = 1; i < threads; ++i) {
        if (pthread_join(ids[i - 1], NULL)) fail("pthread_join failed");
        Worker worker = workers[i];
        result.states += worker.states;
        result.lookaheads += worker.lookaheads;
        if (worker.maximum > result.maximum) {
            result.maximum = worker.maximum;
            result.maximum_count = 0;
            result.c = worker.c;
            result.b = worker.b;
        }
        if (worker.maximum == result.maximum) {
            result.maximum_count += worker.maximum_count;
            if (worker.maximum_count && state_number(&worker) < state_number(&result)) {
                result.c = worker.c;
                result.b = worker.b;
            }
        }
    }
    unsigned p = sweep->family->p;
    if (result.states != (uint64_t)p * p || result.lookaheads != (uint64_t)p * p * p)
        fail("incomplete sweep");
    return result;
}

static bool passes_threshold(const Family *family, int64_t drift)
{
    Wide power = 1;
    for (unsigned i = 0; i < 26; ++i) power *= 7;
    Wide rhs = (Wide)26 * family->s * family->p * SCALE;
    return power < ((Wide)1 << 73) && (Wide)73 * drift < rhs;
}

static void print_stats(const Family *family, const RoundStats *stats)
{
    printf("\"finite\":%u,\"ties\":%" PRIu64 ",\"negative_ties\":%" PRIu64
           ",\"positive_ties\":%" PRIu64 ",\"minimum\":%" PRId64
           ",\"maximum_table_value\":%" PRId64,
           family->p * family->p, stats->ties, stats->negative_ties,
           stats->ties - stats->negative_ties, stats->minimum, stats->maximum);
}

static void probe(Sweep *sweep, const char *path, const char *delta_arg, int64_t *table)
{
    FILE *file = open_file(path, "r");
    unsigned p = sweep->family->p, c, b;
    int fields;
    bool first = true;
    int64_t delta = delta_arg ? signed_integer(delta_arg) : 0;
    printf("[");
    while ((fields = fscanf(file, "%u %u", &c, &b)) == 2) {
        if (c >= p || b >= p) fail("probe outside state space");
        size_t index = sweep->b_major ? b * p + c : c * p + b;
        int64_t original = table[index];
        int64_t changed = narrow((Wide)original + delta);
        int64_t limit = INT64_MAX / (4 * p) - sweep->family->H * SCALE;
        if (changed < -limit || changed > limit) fail("out-of-range corruption");
        table[index] = changed;
        int64_t drift = direct_state(sweep, c, b);
        table[index] = original;
        printf("%s[%u,%u,%" PRId64 ",%s]", first ? "" : ",", c, b, drift,
               passes_threshold(sweep->family, drift) ? "true" : "false");
        first = false;
    }
    if (fields != EOF || ferror(file) || first) fail("invalid probe list");
    close_file(file);
    puts("]");
}

int main(int argc, char **argv)
{
    if (argc >= 2 && !strcmp(argv[1], "check") && argc == 5) {
        Family family = new_family(natural(argv[2]), natural(argv[3]), 0, STANDARD);
        read_chains(&family, argv[4]);
        printf("{\"chains\":%zu,\"residues\":%u}\n", family.count, family.p);
        free(family.items);
        return 0;
    }
    if (argc < 7) fail("usage: chains, round, full, or probe (see REPORT.md)");
    const char *action = argv[1];
    Family family = new_family(natural(argv[2]), natural(argv[3]), natural(argv[4]),
                               parse_rule(argv[5]));
    if (!strcmp(action, "chains") && argc == 7) {
        make_chains(&family);
        write_chains(&family, argv[6]);
        printf("{\"chains\":%zu,\"residues\":%u}\n", family.count, family.p);
        free(family.items);
        return 0;
    }
    if (!strcmp(action, "round") && argc == 9) {
        RoundStats stats;
        int64_t *table = read_table(&family, argv[6], parse_rounding(argv[7]), &stats);
        write_table(table, (size_t)family.p * family.p, argv[8]);
        printf("{");
        print_stats(&family, &stats);
        puts("}");
        free(table);
        return 0;
    }
    bool full = !strcmp(action, "full") && (argc == 11 || argc == 12);
    bool direct = !strcmp(action, "probe") && (argc == 10 || argc == 11);
    if (!full && !direct) fail("invalid arguments");
    bool b_major = parse_layout(argv[7]);
    Rounding rounding = parse_rounding(argv[8]);
    uint64_t threads = full ? natural(argv[9]) : 1;
    uint64_t deadline = full ? natural(argv[10]) : 0;
    if (full && (threads < 1 || threads > 6 || deadline > INT64_MAX ||
                 time(NULL) >= (time_t)deadline))
        fail("invalid thread count or expired deadline");
    make_chains(&family);
    RoundStats stats;
    int64_t *table = read_table(&family, argv[6], rounding, &stats);
    Sweep sweep = {.family = &family, .table = table, .b_major = b_major,
                   .deadline = (time_t)deadline, .next_c = ATOMIC_VAR_INIT(0)};
    if (direct) {
        probe(&sweep, argv[9], argc == 11 ? argv[10] : NULL, table);
    } else {
        sweep.rows = make_rows(&sweep);
        size_t count = (size_t)family.p * family.p;
        if (argc == 12) sweep.drifts = allocate(count, sizeof(*sweep.drifts));
        Worker result = full_sweep(&sweep, (unsigned)threads);
        if (sweep.drifts) {
            write_table(sweep.drifts, count, argv[11]);
            free(sweep.drifts);
        }
        printf("{\"s\":%u,\"H\":%u,\"window\":%u,\"rule\":\"%s\","
               "\"layout\":\"%s\",\"rounding\":\"%s\","
               "\"threads\":%" PRIu64 ",\"chains\":%zu,\"residues\":%u,"
               "\"states\":%" PRIu64 ",\"lookaheads\":%" PRIu64 ","
               "\"maximum\":%" PRId64 ",\"argmax\":[%u,%u],\"argmax_count\":%" PRIu64
               ",\"passes_threshold\":%s,",
               family.s, family.H, family.window, argv[5], argv[7], argv[8],
               threads, family.count, family.p, result.states, result.lookaheads,
               result.maximum, result.c, result.b, result.maximum_count,
               passes_threshold(&family, result.maximum) ? "true" : "false");
        print_stats(&family, &stats);
        puts("}");
        free((void *)sweep.rows);
    }
    free(table);
    free(family.items);
    return 0;
}
