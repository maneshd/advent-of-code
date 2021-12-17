
# This isn't general... but for our input, an initial x-velocity of 15 gets us
# in bounds in the x-axis for steps 15 and onward.
def part1(inp):
    (xmin, xmax), (ymin, ymax) = inp

    # Based on observations:
    #  1. with initial velocity y, after 2*y+1 steps, we'll be at position y=0
    #     and with velocity -y
    #  2. Taking one more step after that we'll be at position -y-1.
    #  3. The largest y for which that is in bounds is -ymin-1
    target = ymin
    y = -target - 1
    steps = 2*y+2

    return sum(range(y+1))


def isgood(dx, dy, targets):
    x, y = 0, 0
    (xmin, xmax), (ymin, ymax) = targets

    while True:
        x, y = x+dx, y+dy
        dx, dy = max(0, dx-1), dy-1

        if xmin <= x and x <= xmax and ymin <= y and y <= ymax:
            return True

        if x > xmax or y < ymin or (x < xmin and dx == 0):
            return False

def part2(inp):
    (tx0, tx1), (ty0, ty1) = inp

    c = 0
    for y in range(ty0, -ty0):
        for x in range(1, tx1+1):
            c += 1 if isgood(x, y, inp) else 0

    return c

inp = ((119, 176), (-141, -84))
print("Part1: ", part1(inp))
print("Part2: ", part2(inp))
