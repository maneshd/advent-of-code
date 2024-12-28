from collections import Counter


def parse_input(file_name):
    with open(file_name, 'r') as f:
        return list(map(int, f.read().strip().split()))


def process_stone(n):
    if n == 0:
        return [1]
    ns = str(n)
    if len(ns) % 2 == 0:
        a, b = ns[:len(ns)//2], ns[len(ns)//2:]
        return [int(a), int(b)]
    return [n*2024]


def blink(d):
    res = Counter()
    for stone, count in d.items():
        for new_stone in process_stone(stone):
            res[new_stone] += count
    return res


def part1(L):
    d = Counter(L)
    for _ in range(25):
        d = blink(d)
    return sum(d.values())


def part2(L):
    d = Counter(L)
    for _ in range(75):
        d = blink(d)
    return sum(d.values())


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))
