from collections import deque

def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


# Get the grid, and replace the start/end w/ their elevations.
def _get_input(f):

    lines = f.readlines()
    start, end = None, None

    for (i, line) in enumerate(lines):
        if 'S' in line:
            start = (i, line.index('S'))
        if 'E' in line:
            end = (i, line.index('E'))

    grid = map(lambda s: s.replace('S', 'a').replace('E', 'z'), lines)
    return list(grid), start, end


def _neighbor_candidates(grid, i, j):
    return map(
            lambda d: (i+d[0], j+d[1]),
            ((-1, 0), (1, 0), (0, -1), (0, 1))
    )

def _in_bounds(grid, i, j):
    return 0 <= i and i < len(grid) and 0 <= j  and j < len(grid[0])


def get_neighbors1(grid, i, j):
    def is_good(neighbor):
        ii, jj = neighbor
        return _in_bounds(grid, *neighbor) and ord(grid[ii][jj]) <= ord(grid[i][j])+1

    candidates = _neighbor_candidates(grid, i, j)
    return filter(is_good, candidates)


def get_neighbors2(grid, i, j):
    def is_good(neighbor):
        ii, jj = neighbor
        return _in_bounds(grid, *neighbor) and ord(grid[ii][jj]) + 1 >= ord(grid[i][j])
    candidates = _neighbor_candidates(grid, i, j)
    return filter(is_good, candidates)


def part1(grid, start, end):
    dist = {start: 0}
    to_process = deque([start])

    while to_process:
        u = to_process.popleft()

        for v in get_neighbors1(grid, *u):
            if v not in dist:
                dist[v] = dist[u] + 1
                to_process.append(v)
                if v == end:
                    return dist[v]

    return "NOT FOUND"

def part2(grid, _, end):
    dist = {end: 0}
    to_process = deque([end])

    while to_process:
        u = to_process.popleft()
        for v in get_neighbors2(grid, *u):
            if v not in dist:
                dist[v] = dist[u] + 1
                to_process.append(v)

    return min([v for ((i, j), v) in dist.items() if grid[i][j] == 'a'])


inp = get_input("input.txt")
print("part 1:", part1(*inp))
print("part 2:", part2(*inp))
