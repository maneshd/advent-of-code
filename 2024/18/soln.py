from collections import deque, defaultdict


L, W = 70, 70


def parse_input(fname):
    with open(fname, 'r') as f:
        return [tuple(map(int, r.split(","))) for r in f.read().split("\n")]


def bfs(corrupted):
    s, t = (0, 0), (L, W)

    neighbors = lambda x, y: ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
    in_bounds = lambda x, y: 0 <= x and 0 <= y and x <= W and y <= L

    d = defaultdict(lambda: float('infinity'))
    d[s] = 0
    q = deque([s])

    while q:
        u = q.popleft()
        for v in neighbors(*u):
            if in_bounds(*v) and v not in d and v not in corrupted:
                d[v] = d[u]+1
                q.append(v)
    return d[t]


def part1(inp):
    corrupted = set(inp[:1024])
    return bfs(corrupted)


def part2(L):
    lo, hi = 0, len(L)+1

    # Invariant: there's a working solution in [lo, hi)
    while (hi-lo) > 1:
        mid = (lo+hi)//2
        path_exists = bfs(set(L[:mid])) != float('infinity')
        (lo, hi) = (mid, hi) if path_exists else (lo, mid)
    return L[(hi+lo)//2]


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print(f"part 1: {part1(inp)}")
    print(f"part 2: {part2(inp)}")