import bisect
from collections import Counter

def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


def _get_input(f):

    def parse_coord(fragment):
        coord_string = fragment.split("at ")[1]  # "x=123, y=345"
        return tuple(int(x[2:]) for x in coord_string.split(", "))

    def parse_line(line):
        return tuple(parse_coord(s) for s in line.split(":"))

    return list(map(parse_line, f.readlines()))

def dist(p1, p2):
    return sum(abs(a-b) for a, b in zip(p1, p2))

class Ranges1D:
    def __init__(self):
        self.ranges = []  # always sorted

    def add_range(self, rng):
        #  idx = bisect.bisect_left(self.ranges, rng, key=lambda a: a[0])
        idx = bisect.bisect_left([p[0] for p in self.ranges], rng[0])
        self.ranges.insert(idx, rng)

        newRanges = []
        prev = None
        for (i, (xx, yy)) in enumerate(self.ranges):
            if prev is None:
                prev = (xx, yy)
                continue
            x, y = prev
            if xx <= y+1:
                prev = x, max(y, yy)
            else:
                newRanges.append(prev)
                prev = xx, yy
        if prev is not None:
            newRanges.append(prev)
        self.ranges = newRanges



def part1(inp, target_y):
    rng = Ranges1D()

    for (sensor, beacon) in inp:
        maxD = dist(sensor, beacon)
        x, y = sensor[0], target_y
        d = dist(sensor, (x, y))
        if d <= maxD:
            slack = maxD-d
            rng.add_range((x-slack, x+slack))

    res = sum(map(lambda r: r[1]-r[0]+1, rng.ranges))

    # ugh, some beacons might aleady exist in these ranges...
    def in_range(rng, beacon):
        x1, x2 = rng
        x, y = beacon
        return y == target_y and x1 <= x and x <= x2

    def in_any_range(beacon):
        return any(in_range(rng, beacon) for rng in rng.ranges)

    beacons = set(b for (_, b) in inp)
    overlap = sum(map(in_any_range, beacons))
    return res - overlap


MAX_XY = 4000000

'''
CAUTION: SLOW (~1-2 minutes)

This is kind of slow/sad. An even nicer solution might (somehow) keep track of 2D shapes
representing possible beacon locations. For each sensor, you'd subtract out parts of the
existing shapes that are no longer viable, possibly breaking up some of the viable shapes
into smaller ones.
'''
def part2(inp):
    # get possibilities per row lol
    rngs = [Ranges1D() for _ in range(MAX_XY)]

    for (_, beacon) in inp:
        x, y = beacon
        if 0 <= y and y < len(rngs) and 0 <= x and x < MAX_XY:
            rngs[y].add_range((x, x))

    for (i, (sensor, beacon)) in enumerate(inp):
        print(f'progress: {i}/{len(inp)}')
        maxD = dist(sensor, beacon)
        sx, sy = sensor
        for dy in range(maxD+1):
            slack = maxD - dy 
            rng = (max(0, sx-slack), min(sx+slack, MAX_XY))

            rows = (sy-dy, sy+dy) if dy > 0 else (sy, )
            for row in rows:
                if 0 <= row and row < len(rngs):
                    rngs[row].add_range(rng)

    for (i, rng) in enumerate(rngs):
        if len(rng.ranges) > 1:
            return (rng.ranges[0][1]+1) * 4000000 + i


Y_TARGET = 2000000
inp = get_input("input.txt")
print("part 1:", part1(inp, Y_TARGET))
print("part 2:", part2(inp))

