from collections import Counter


def get_input(filename):
    with open(filename, 'r') as f:
        def process_line(line):
            return [int(x) for x in line.split()]
        return list(map(process_line, f.readlines()))


def part1(inp):
    xs, ys = zip(*inp)
    L = zip(sorted(xs), sorted(ys))
    return sum(abs(x-y) for x, y in L)


def part2(inp):
    xs, ys = zip(*inp)
    c = Counter(ys)
    score = lambda x: x*c[x]
    return sum(map(score, xs))


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))

