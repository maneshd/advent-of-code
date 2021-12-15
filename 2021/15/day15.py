from collections import defaultdict

def get_input(fname):
    with open(fname, 'r') as f:
        return [[int(x) for x in row.strip()] for row in f.readlines()]


def neighbors(G, i, j):
    for (di, dj) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ii, jj = i+di, j+dj
        if ii >= 0 and jj >= 0 and ii < len(G) and jj < len(G[0]):
            yield (ii, jj)


# More or less Dijkstra's SP alg.
def part1(inp):
    G = inp
    start = (0, 0)
    goal = (len(inp)-1, len(inp[0])-1)

    # SP=known shortest paths; C=candidates
    SP = {}
    C = {start: 0}

    while C:
        d, (i, j) = min((v, k) for (k, v) in C.items())
        if (i, j) == goal:
            return d

        del C[(i, j)]
        SP[(i, j)] = d

        for (ii, jj) in neighbors(G, i, j):
            if (ii, jj) in SP:
                continue
            C[(ii, jj)] = min(C.get((ii, jj), float('inf')), d + G[ii][jj])


def part2(G):
    h, w = len(G), len(G[0])
    G2 = [[0]*(w*5) for x in range(h*5)]

    for i in range(len(G2)):
        for j in range(len(G2[0])):
            c = i // h + j // w
            G2[i][j] = ((G[i%h][j%w] - 1 + c) % 9) + 1

    return part1(G2)

# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
