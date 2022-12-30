def get_input(fname):
    with open(fname, 'r') as f:
        return list(_get_input(f))

def _get_input(f):
    def map_line(l):
        direction, n = l.split(" ")
        return direction, int(n)
    return map(map_line, f.readlines())

dirmap = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}

def move_head(hx, hy, direction):
    dx, dy = dirmap[direction]
    return hx+dx, hy+dy

def correct_tail(hx, hy, tx, ty):
    dx = hx - tx
    dy = hy - ty

    if abs(dx) <= 1 and abs(dy) <= 1:
        return (tx, ty)
    
    dx = 0 if dx == 0 else dx // abs(dx)
    dy = 0 if dy == 0 else dy // abs(dy)
    return (tx + dx, ty + dy)


def part1(data):

    H = (0, 0)
    T = (0, 0)
    visited = set([T])

    for direction, count in data:
        for i in range(count):
            H = move_head(*H, direction)
            T = correct_tail(*H, *T)
            visited.add(T)

    return len(visited)

def part2(data):
    rope = [(0, 0)]*10
    visited = set([(0, 0)])

    for direction, count in data:
        for i in range(count):
            rope[0] = move_head(*rope[0], direction)
            for i in range(9):
                rope[i+1] = correct_tail(*rope[i], *rope[i+1])
            visited.add(rope[9])

    return len(visited)


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
