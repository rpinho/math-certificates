#include <algorithm>
#include <array>
#include <cstdint>
#include <functional>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using Position = std::vector<int>;

// Sorted positive heaps. A move either removes tokens or splits a heap,
// so the sum of squared heap sizes strictly decreases.
class RecursiveSolver {
    std::array<std::vector<std::array<int, 2>>, 256> heap_moves;
    std::unordered_map<uint64_t, bool> memo;

    static uint64_t key(const Position& heaps) {
        const int total = [&] {
            int sum = 0;
            for (int heap : heaps) sum += heap;
            return sum;
        }();
        if (total <= 63) {
            uint64_t bits = 0;
            int boundary = 0;
            for (int heap : heaps) {
                boundary += heap;
                bits |= uint64_t{1} << (boundary - 1);
            }
            return bits;
        }
        if (heaps.size() > 4) throw std::runtime_error("oversize split position");
        uint64_t packed = uint64_t{1} << 63;
        for (size_t index = 0; index < heaps.size(); ++index) {
            packed |= uint64_t(heaps[index]) << (8 * index);
        }
        return packed;
    }

public:
    explicit RecursiveSolver(const std::string& code) {
        for (int size = 1; size <= 255; ++size) {
            for (int removed = 0; removed < int(code.size()) - 1 && removed <= size; ++removed) {
                const int digit = code[removed == 0 ? 0 : removed + 1] - '0';
                const int left = size - removed;
                if (left == 0 && (digit & 1)) heap_moves[size].push_back({0, 0});
                if (left > 0 && (digit & 2)) heap_moves[size].push_back({left, 0});
                if (digit & 4) {
                    for (int second = 1; second <= left / 2; ++second) {
                        heap_moves[size].push_back({left - second, second});
                    }
                }
            }
        }
    }

    bool losing(const Position& heaps) {
        const uint64_t state = key(heaps);
        if (const auto found = memo.find(state); found != memo.end()) return found->second;
        bool has_move = false;
        for (size_t i = 0; i < heaps.size(); ++i) {
            if (i > 0 && heaps[i] == heaps[i - 1]) continue;
            if (heap_moves[heaps[i]].empty()) continue;
            has_move = true;
            Position child;
            child.reserve(heaps.size() + 1);
            for (const auto& move : heap_moves[heaps[i]]) {
                child.assign(heaps.begin(), heaps.begin() + i);
                child.insert(child.end(), heaps.begin() + i + 1, heaps.end());
                for (int heap : move) {
                    if (heap > 0) child.insert(
                        std::lower_bound(child.begin(), child.end(), heap, std::greater<int>()), heap);
                }
                if (losing(child)) {
                    memo.emplace(state, false);
                    return false;
                }
            }
        }
        memo.emplace(state, has_move);
        return has_move;
    }
};

void write_partitions(RecursiveSolver& solver, Position& heaps, int remaining, int maximum) {
    if (remaining == 0) {
        std::cout.put(solver.losing(heaps) ? 'P' : 'N');
        return;
    }
    for (int first = 1; first <= std::min(remaining, maximum); ++first) {
        heaps.push_back(first);
        write_partitions(solver, heaps, remaining - first, first);
        heaps.pop_back();
    }
}

void write_four_heap_grid(RecursiveSolver& solver, int maximum, Position& heaps, int slots) {
    if (slots == 0) {
        std::cout.put(solver.losing(heaps) ? 'P' : 'N');
        return;
    }
    for (int first = 0; first <= maximum; ++first) {
        if (first > 0) heaps.push_back(first);
        write_four_heap_grid(solver, first, heaps, slots - 1);
        if (first > 0) heaps.pop_back();
    }
}

int main(int argc, char** argv) {
    if (argc < 4) throw std::runtime_error("usage: direct CODE table|grid MAX or direct CODE query HEAPS ...");
    std::ios::sync_with_stdio(false);
    RecursiveSolver solver(argv[1]);
    const std::string mode = argv[2];
    Position heaps;
    if (mode == "table") {
        const int max = std::stoi(argv[3]);
        if (max < 0 || max > 63) throw std::runtime_error("table size out of range");
        for (int total = 0; total <= max; ++total) write_partitions(solver, heaps, total, total);
    } else if (mode == "grid") {
        const int max = std::stoi(argv[3]);
        if (max < 0 || max > 255) throw std::runtime_error("grid size out of range");
        write_four_heap_grid(solver, max, heaps, 4);
    } else if (mode == "query") {
        for (int arg = 3; arg < argc; ++arg) {
            std::istringstream values(argv[arg]);
            std::string value;
            heaps.clear();
            int total = 0;
            while (std::getline(values, value, ',')) {
                const int heap = std::stoi(value);
                if (heap < 1 || heap > 63) throw std::runtime_error("invalid heap");
                heaps.push_back(heap);
                total += heap;
            }
            if (total > 63) throw std::runtime_error("query size out of range");
            std::sort(heaps.begin(), heaps.end(), std::greater<int>());
            std::cout.put(solver.losing(heaps) ? 'P' : 'N');
        }
    } else {
        throw std::runtime_error("unknown mode");
    }
}
