from collections import defaultdict

DIRS = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0),
}

PERIOD = 700  # lol, shoudn't hard-code. But also, this wasn't necessary.


def get_input(fname):
    with open(fname, 'r') as f:
        blizzards = defaultdict(list)
        for r, line in enumerate(f.readlines()):
            for c, ch in enumerate(line.strip()):
                if ch in "<>^v":
                    blizzards[(r, c)].append(DIRS[ch])
        rows, cols = zip(*blizzards.keys())
        return blizzards, max(rows), max(cols)


def advance_blizzards(blizzards, N, M):
    res = defaultdict(list)
    for (pos, dpos_list) in blizzards.items():
        for (dr, dc) in dpos_list:
            r, c = pos
            r, c = r+dr, c+dc
            if r == N+1:
                r = 1
            elif r == 0:
                r = N
            elif c == 0:
                c = M
            elif c == M+1:
                c = 1

            res[(r, c)].append((dr, dc))

    return res

def get_neighbors(pos, N, M):
    yield pos
    S, T = (0, 1), (N+1, M)
    for (dr, dc) in DIRS.values():
        r, c = pos
        r, c = r+dr, c+dc
        if r > 0 and c > 0 and r <= N and c <= M:
            yield r, c
        if (r, c) in (S, T):
            yield r, c


def find_path(blizzards, N, M, source, target):
    s = (source, 0)  # position at time = 0

    to_process = [s]
    seen = set([s])

    for t in range(1000000):
        next_to_process = []
        blizzards = advance_blizzards(blizzards, N, M)

        for (pos, tt) in to_process:
            assert(t == tt)

            for v in get_neighbors(pos, N, M):
                if v in blizzards:
                    continue
                if (v, (t+1) % PERIOD) in seen:
                    continue
                seen.add((v, (t+1) % PERIOD))
                next_to_process.append((v, t+1))
                if v == target:
                    return t+1, blizzards

        to_process = next_to_process

        if not to_process:
            return "D'OH!"


def part1(inp):
    blizzards, N, M = inp
    return find_path(blizzards, N, M, (0, 1), (N+1, M))[0]


def part2(inp):
    blizzards, N, M = inp
    p1, blizzards = find_path(blizzards, N, M, (0, 1), (N+1, M))
    p2, blizzards = find_path(blizzards, N, M, (N+1, M), (0, 1))
    p3, blizzards = find_path(blizzards, N, M, (0, 1), (N+1, M))
    return p1+p2+p3

inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))

