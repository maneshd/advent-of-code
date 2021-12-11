from itertools import product

def get_input(fname):
    with open(fname, 'r') as f:
        return [[int(x) for x in s.strip()] for s in f.readlines()]


def neighbors(B, i, j):
    def in_bounds(i, j):
        return i >= 0 and j >= 0 and i < len(B) and j < len(B[0])

    deltas = [ij for ij in product((-1, 0, 1), (-1, 0, 1)) if ij != (0, 0)]
    candidates = [(i+di, j+dj) for (di, dj) in deltas]
    return filter(lambda x: in_bounds(*x), candidates)

# return # of flashes
def step(B):
    to_flash = set()
    flashed = set()

    for i, row in enumerate(B):
        for j, _ in enumerate(row):
            B[i][j] += 1
            if B[i][j] > 9:
                to_flash.add((i, j))

    while to_flash:
        (i, j) = to_flash.pop()
        flashed.add((i, j))
        for ii, jj in neighbors(B, i, j):
            B[ii][jj] += 1
            if B[ii][jj] > 9 and (ii, jj) not in flashed:
                to_flash.add((ii, jj))

    for (i, j) in flashed:
        B[i][j] = 0

    return len(flashed)

def part1(B):
    return sum(step(B) for i in range(100))

def part2(B):
    i = 1
    while step(B) != 100:
        i += 1
    return i


# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))

inp = get_input("input.txt")
print("part 2:", part2(inp))
