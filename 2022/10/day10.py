def get_input(fname):
    with open(fname, 'r') as f:
        return list(_get_input(f))

def _get_input(f):
    def map_line(l):
        l = l.strip()
        return l if l == "noop" else int(l.split(" ")[1])
    return map(map_line, f.readlines())

CYCLES = [20, 60, 100, 140, 180, 220]

def getXPerCycle(lines):
    Xs = []
    x = 1

    for line in lines:
        if line == "noop":
            Xs.append(x)
        else:
            Xs.append(x)
            Xs.append(x)
            x += line 
    return Xs

def part1(lines):
    Xs = getXPerCycle(lines)
    return sum(map(lambda cycle: cycle*Xs[cycle-1], CYCLES))


def part2(lines):
    Xs = getXPerCycle(lines)

    screen = []
    for (i, x) in enumerate(Xs):
        i = i % 40
        ch = "#" if (x-1 <= i and i <= x+1) else "."
        screen.append(ch)
    res = []
    for i in range(0, 240, 40):
        res.append(''.join(screen[i:i+40]))

    return "\n" + "\n".join(res)


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
