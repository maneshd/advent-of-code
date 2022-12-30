def get_input(fname):
    with open(fname, 'r') as f:
        return list(map(
                lambda line: [int(x) for x in line.strip().split("\n")],
                f.read().split("\n\n")))

def part1(data):
    return max(map(sum, data))

def part2(data):
    return sum(sorted(map(sum, data), reverse=True)[0:3])


inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))
