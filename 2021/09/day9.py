
def get_input(fname):
    with open(fname, 'r') as f:
        return [[int(x) for x in s.strip()] for s in f.readlines()]

def in_bounds(B, i, j):
    return i >= 0 and j >= 0 and i < len(B) and j < len(B[0])

def neighbors(B, i, j):

    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ii, jj = i+di, j+dj
        if in_bounds(B, ii, jj):
            yield (ii, jj)


def part1(inp):
    B = inp
    res = 0

    for i, row in enumerate(inp):
        for j, val in enumerate(row):
            # print("trying ({}, {})".format(i, j))
            if all(val < B[x][y] for (x, y) in neighbors(B, i, j)):
                res += val+1
    return res


def basin_size(B, i, j):

    visited = set([(i, j)])
    to_process = [(i, j)]

    while to_process:
        x, y = to_process.pop()

        for xx, yy in neighbors(B, x, y):
            if B[xx][yy] == 9:
                continue
            if (xx, yy) not in visited:
                visited.add((xx, yy))
                to_process.append((xx, yy))

    # print(visited)
    return len(visited)



def part2(inp):
    B = inp

    lows = []

    for i, row in enumerate(inp):
        for j, val in enumerate(row):
            # print("trying ({}, {})".format(i, j))
            if all(val < B[x][y] for (x, y) in neighbors(B, i, j)):
                lows.append((i, j))

    # for i, j in lows:
    #     print("({}, {}) => {}".format(i, j, basin_size(B, i, j)))
    bsizes = [basin_size(B, i, j) for (i, j) in lows]
    bsizes.sort()
    return bsizes[-1]*bsizes[-2]*bsizes[-3]



# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
