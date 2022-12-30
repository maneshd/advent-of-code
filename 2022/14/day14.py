def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


def _get_input(f):

    def parse_pair(pair):
        return tuple(int(x) for x in pair.split(","))

    def parse_line(line):
        return list(parse_pair(x) for x in line.split(" -> "))

    return list(map(parse_line, f.readlines()))


def _unit_dxdy(x1, y1, x2, y2):
    dx, dy = x2-x1, y2-y1
    return tuple( d//abs(d) if d != 0 else d for d in (dx, dy))


def _points_on_line(p1, p2):
    x, y = p1
    dx, dy = _unit_dxdy(*p1, *p2)
    while (x, y) != p2:
        yield (x, y)
        x, y = x+dx, y+dy
    yield (x, y)


def make_map(inp):
    res = set()
    for line in inp:
        for p1, p2 in zip(line, line[1:]):
            for p in _points_on_line(p1, p2):
                res.add(p)
    return res

# Num squares:  642
# Bounding box: (490, 14), (563, 162)
MAX_DEPTH = 162

def get_stats(m):
    print("Num squares: ", len(m))
    xmin = min(x[0] for x in m)
    xmax = max(x[0] for x in m)
    ymin = min(x[1] for x in m)
    ymax = max(x[1] for x in m)
    print(f'Bounding box: {(xmin, ymin)}, {(xmax, ymax)}')

def drop_sand(m):
    x, y = 500, 0

    while y <= MAX_DEPTH+3 and (500, 0) not in m:
        if (x, y+1) not in m:
            y = y+1
        elif (x-1, y+1) not in m:
            x, y = x-1, y+1
        elif (x+1, y+1) not in m:
            x, y = x+1, y+1
        else:
            m.add((x, y))
            return True

    return False


def part1(m):
    m = m.copy()

    c = 0
    while drop_sand(m):
        c += 1
    return c


def part2(m):
    m = m.copy()
    for x in range (1000):
        m.add((x, MAX_DEPTH+2))

    c = 0
    while drop_sand(m):
        c += 1
    return c


inp = get_input("input.txt")
m = make_map(inp)
print("part 1:", part1(m))
print("part 2:", part2(m))
