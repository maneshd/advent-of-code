from collections import defaultdict

# Parse the input file. Returns a list of tuples where the first entry the
# 'action' and the second entry is the 'value'. For example, if the file
# contians two entries, 'W1' and 'F91', get_input returns [('W', 1), ('F', 11)].
def get_input(fname):
    with open(fname, 'r') as f:
        return [(x[0], int(x[1:])) for x in f.readlines()]

inp = get_input("day12.in")

# A dict representing the 'unit' action to take for each instruction in terms of
# (x, y, theta). Note that the action 'F', i.e. 'Forward', is absent and should
# be handled separately.
inst_d = {
    'N': (0, 1, 0),
    'S': (0, -1, 0),
    'E': (1, 0, 0),
    'W': (-1, 0, 0),
    'L': (0, 0, 1),
    'R': (0, 0, -1),
}

# A dict mapping an angle to one of the four cardinal directions.
f_d = {
    0: 'E',
    90: 'N',
    180: 'W',
    270: 'S',
}

# Inputs:
#  p: a 3-tuple (x, y, theta)
#  inst:
def apply_instruction(p, inst):
    x, y, theta = p
    c, val = inst

    if c == 'F':
        c = f_d[theta]

    dx, dy, dtheta = inst_d[c]
    return x + val*dx, y + val*dy, (theta + val*dtheta) % 360


def part1(inp):
    p = (0, 0, 0)

    for d in inp:
        p = apply_instruction(p, d)

    return abs(p[0]) + abs(p[1])


def rotate(x, y, val):
    if val == 0:
        return x, y
    elif val == 90:
        return -y, x
    elif val == 180:
        return -x, -y
    elif val == 270:
        return y, -x

    print("Something has gone wrong!")
    exit()


debug = False

def part2(inp):
    p = (0, 0)
    wp = (10, 1)

    df = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}

    if debug:
        print("ship: ({}, {})  Waypoint: ({}, {})".format(p[0], p[1], wp[0], wp[1]))

    for c, val in inp:
        if debug:
            print("{}{} -> ".format(c, val))
        if c in df:
            dx, dy = df[c]
            wpx, wpy = wp
            wp = wpx + dx*val, wpy + dy*val
        elif c == 'F':
            px, py = p
            wpx, wpy = wp
            p = px + val*wpx, py + val*wpy
        elif c in 'LR':
            if c == 'R':
                val = (-val) % 360
            wp = rotate(wp[0], wp[1], val)

        if debug:
            print("ship: ({}, {})  Waypoint: ({}, {})".format(p[0], p[1], wp[0], wp[1]))

    return abs(p[0]) + abs(p[1])



print("part1:", part1(inp))
print("part2:", part2(inp))
