def get_input(fname):
    with open(fname, 'r') as f:
        return list(_get_input(f))

def _get_input(f):
    M = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
    def map_line(l):
        return [M[x] for x in l.strip().split(' ')]
    return map(map_line, f.readlines())


def part1(data):
    def points(a, b):
        if a == b:
            return 3 + b
        elif (a + 1) % 3 == b % 3:
            return 6 + b
        else:
            return b
    return sum(map(lambda ab: points(*ab), data))

def part2(data):
    def t(ab):
        a, b = ab
        if b == 1:
            return [a, 3 if a == 1 else a-1]
        elif b == 2:
            return [a, a]
        else:
            return [a, 1 if a == 3 else a+1]
    return part1(map(t, data))


inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))
