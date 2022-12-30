from collections import deque

def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


def _get_input(f):
    return [tuple(int(x) for x in line.split(",")) for line in f.readlines()]


def neighbors(x, y, z):
    for d in (1, -1):
        yield x+d, y, z
        yield x, y+d, z
        yield x, y, z+d

def part1(inp):
    cubes = set(inp)
    res = 0
    for cube in cubes:
        res += 6
        for n in neighbors(*cube):
            if n in cubes:
                res -= 1

    return res


def bounding_box(inp):
    xs, ys, zs = zip(*inp)
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def in_bounds(pt):
    return all(dim >= -1 and dim <= 20 for dim in pt)

def part2(inp):
    res = 0
    cubes = set(inp)

    low, hi = bounding_box(inp)
    s = tuple(x-1 for x in low)

    low = min(low) - 1
    hi = max(hi) + 1
    def in_bounds(pt):
        return all(dim >= low and dim <= hi for dim in pt)

    #  s = (-1, -1, -1)
    seen = set([s])
    to_process = [s]

    while to_process:
        u = to_process.pop()

        for v in neighbors(*u):
            if not in_bounds(v) or v in seen:
                continue
            if v in cubes:
                res += 1
                continue
            seen.add(v)
            to_process.append(v)

    return res






inp = get_input("input.txt")
print(inp[:2])
#  inp = get_input("test.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))

