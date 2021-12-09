from collections import defaultdict

def get_input(fname):
    active = set()
    # x = 0
    z = 0

    with open(fname, 'r') as f:
        for x, line in enumerate(f.readlines()):
            for y, letter in enumerate(line.strip()):
                if letter == '#':
                    active.add((x, y, z))
    return active


def get_neighbors_4d(pt):
    w, x, y, z = pt
    res = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                        continue
                    res.append((w+dw, x+dx, y+dy, z+dz))
    return res


def get_neighbors(pt):
    if len(pt) == 4:
        return get_neighbors_4d(pt)
    x, y, z = pt
    res = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                res.append((x+dx, y+dy, z+dz))
    return res


def advance(active):
    res = set()
    seen = set()

    for p in active:
        # if 2 or 3 neighbors are active, remain active.
        active_neighbors = sum(1 for n in get_neighbors(p) if n in active)
        if active_neighbors in (2, 3):
            res.add(p)

        for n in get_neighbors(p):
            if n in active or n in seen:
                continue
            seen.add(n) # not really necessary, but whatevs
            if sum(1 for nn in get_neighbors(n) if nn in active) == 3:
                res.add(n)

    return res

def part1(inp):
    res = inp
    for i in range(6):
        res = advance(res)
    return len(res)

def part2(inp):
    res = {(w, x, y, 0) for w, x, y in inp}
    for i in range(6):
        res = advance(res)
    return len(res)



inp = get_input("day17.in")
print("part1:", part1(inp))
print("part2:", part2(inp))
