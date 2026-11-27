#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

// Independent forward evaluation. Within a given token total, partitions
// are traversed in increasing lexicographic order on descending heap lists.
// A zero-token split strictly decreases that order.
class PartitionTable {
    std::array<int, 256> copies{};
    std::array<int, 256> positive{};
    std::vector<int> permission;
    std::unordered_map<uint64_t, char> outcomes;
    int largest_seen;

    uint64_t boundary_mask(int total) const {
        if (total > 63) {
            uint64_t high = uint64_t{1} << 63;
            int shift = 0;
            for (int h = largest_seen; h > 0; --h) {
                for (int occurrence = 0; occurrence < copies[h]; ++occurrence) {
                    if (shift == 32) throw std::runtime_error("too many heaps for large grid");
                    high |= uint64_t(h) << shift;
                    shift += 8;
                }
            }
            return high;
        }
        uint64_t marks = 0;
        for (int h = 1; h <= largest_seen; ++h) {
            for (int occurrence = 0; occurrence < copies[h]; ++occurrence) {
                marks |= uint64_t{1} << (total - 1);
                total -= h;
            }
        }
        return marks;
    }

    char evaluate(int total, int parts) {
        bool legal = false;
        for (int i = 0; i < parts; ++i) {
            const int h = positive[i];
            if (i > 0 && positive[i - 1] == h) continue;
            --copies[h];
            for (int k = 0; k < int(permission.size()) && k <= h; ++k) {
                const int rest = h - k;
                // Split the remainder into two ordered slots. Zero slots
                // count as absent heaps, so the bit selects 0, 1 or 2 heaps.
                for (int left = 0; left <= rest / 2; ++left) {
                    const int right = rest - left;
                    const int survivors = int(left > 0) + int(right > 0);
                    if (!(permission[k] & (1 << survivors))) continue;
                    legal = true;
                    ++copies[left];
                    ++copies[right];
                    const char child = outcomes.at(boundary_mask(total - k));
                    --copies[right];
                    --copies[left];
                    if (child == 'P') {
                        ++copies[h];
                        return 'N';
                    }
                }
            }
            ++copies[h];
        }
        return legal ? 'P' : 'N';
    }

    void emit(int total, int parts) {
        const uint64_t state = boundary_mask(total);
        const char result = evaluate(total, parts);
        if (!outcomes.emplace(state, result).second) throw std::runtime_error("duplicate partition");
        std::cout.put(result);
    }

    void partitions(int total, int remaining, int maximum, int parts) {
        if (remaining == 0) {
            emit(total, parts);
            return;
        }
        for (int next = 1; next <= maximum && next <= remaining; ++next) {
            positive[parts] = next;
            ++copies[next];
            partitions(total, remaining - next, next, parts + 1);
            --copies[next];
        }
    }

    void grid(int maximum, int slots, int total, int parts) {
        if (slots == 0) {
            emit(total, parts);
            return;
        }
        for (int next = 0; next <= maximum; ++next) {
            if (next == 0) {
                grid(0, slots - 1, total, parts);
            } else {
                positive[parts] = next;
                ++copies[next];
                grid(next, slots - 1, total + next, parts + 1);
                --copies[next];
            }
        }
    }

public:
    PartitionTable(const std::string& code, int limit) : largest_seen(limit) {
        for (char symbol : code) {
            if (symbol != '.') permission.push_back(symbol - '0');
        }
    }

    void table() {
        for (int total = 0; total <= largest_seen; ++total) partitions(total, total, total, 0);
    }

    void four_heap_grid() {
        for (int digit : permission) {
            if (digit & 4) throw std::runtime_error("grid is eligible only for games without splitting");
        }
        grid(largest_seen, 4, 0, 0);
    }
};

int main(int argc, char** argv) {
    if (argc != 4) throw std::runtime_error("usage: checker CODE table|grid MAX");
    std::ios::sync_with_stdio(false);
    const std::string mode = argv[2];
    const int limit = std::stoi(argv[3]);
    if (limit < 0 || limit > (mode == "table" ? 63 : 255)) throw std::runtime_error("out of range");
    PartitionTable table(argv[1], limit);
    if (mode == "table") table.table();
    else if (mode == "grid") table.four_heap_grid();
    else throw std::runtime_error("unknown mode");
}
