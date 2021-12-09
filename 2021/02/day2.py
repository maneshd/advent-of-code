
def get_input(fname):
    with open(fname, 'r') as f:
        def map_line(ln):
            dr, n = ln.split(' ')
            return (dr, int(n))
        return [map_line(x.strip()) for x in f.readlines()]

# if __name__ == "__main__"
def part1(L):
    dr = {'forward': (1, 0), 'down': (0, 1), 'up': (0, -1)}
    x, y = (0, 0)
    for d, n in L:
        # print(d, n)
        dx, dy = dr[d]
        dx, dy = dx*n, dy*n
        x, y = x + dx, y + dy
        # print('({}, {})'.format((x, y)))

    return x*y

def part2(L):
    x, y, aim = (0, 0, 0)

    for d, n in L:
        if d == 'down':
            aim += n
        elif d == 'up':
            aim -= n
        else:
            x += n
            y += n*aim

    return x*y


in2 = get_input("day2.in")
# in2 = get_input("test.in")
print("part 1:", part1(in2))
print("part 2:", part2(in2))
