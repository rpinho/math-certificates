CC = clang
CFLAGS = -O3 -std=c17 -D_DARWIN_C_SOURCE -Wall -Wextra -Werror
GMP = $(shell pkg-config --cflags --libs gmp)

.PHONY: all
all: build/solver build/enumerator build/check_certificates

build:
	mkdir -p build

build/solver: solver.c | build
	$(CC) $(CFLAGS) $< $(GMP) -o $@

build/enumerator: enumerator.c | build
	$(CC) $(CFLAGS) $< $(GMP) -o $@

build/check_certificates: check_certificates.c | build
	$(CC) $(CFLAGS) $< $(GMP) -o $@
