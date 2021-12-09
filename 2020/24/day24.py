from collections import deque, defaultdict

def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        for l in f.readlines():
            res.append([])
            l = l.strip()
            i = 0
            while i < len(l):
                if l[i] in 'ns':
                    res[-1].append(l[i:i+2])
                    i += 2
                else:
                    res[-1].append(l[i])
                    i += 1
    return res


M = {
  'e': (2, 0),
  'se': (1, -1),
  'ne': (1, 1),
  'w': (-2, 0),
  'sw': (-1, -1),
  'nw': (-1, 1),
}

def part1(inp):
    flipped = defaultdict(lambda: False)

    for steps in inp:
        x, y = (0, 0)
        for step in steps:
            dx, dy = M[step]
            x += dx
            y += dy
        flipped[(x, y)] = not flipped[(x, y)]

    return set(k for k, v in flipped.items() if v)


def run_step(flipped):
    res = set()
    candidates = set(flipped)
    for x, y in flipped:
        for dx, dy in M.values():
            candidates.add((x+dx, y+dy))

    for x, y in candidates:
        c = sum(1 for dx, dy in M.values() if (x+dx, y+dy) in flipped)
        if ((x, y) in flipped and c in (1, 2)) or ((x, y) not in flipped and c == 2):
            res.add((x, y))

    return res


# t1 = set([(0, 0), (2, 0)])
# print(t1)
# t1 = run_step(t1)
# print(t1)
# t1 = run_step(t1)
# print(t1)
# t1 = run_step(t1)
# print(t1)




def part2(flipped):
    # flipped are the black tles
    # print("day 0:", len(flipped))
    # print("day 0:", flipped)
    for i in range(100):
        flipped = run_step(flipped)
        # print("day {}: {}".format(i+1, len(flipped)))
        # print("day {}: {}".format(i+1, flipped))

    return len(flipped)




inp = get_input("day24.in")
# inp = get_input("test.in")
tiles = part1(inp)
print("part1:", len(tiles))
print("part2:", part2(tiles))
