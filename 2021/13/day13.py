
def get_input(fname):
    with open(fname, 'r') as f:
        dots = []
        for ln in f:
            if ln == "\n":
                break
            dots.append(tuple(int(x) for x in ln.strip().split(",")))

        folds = []
        for ln in f:
            a, b = ln.strip().split("=")
            folds.append((a[-1], int(b)))

        return dots, folds


def foldleft(point, x0):
    x, y = point
    x = x if x <= x0 else x0 - (x - x0)
    return x, point[1]

def foldright(point, y0):
    x, y = point
    y = y if y <= y0 else y0 - (y - y0)
    return x, y


def part1(inp):
    dots, folds = inp
    return len(set(foldleft(p, folds[0][1]) for p in dots))

def part2(G):
    dots, folds = G

    for dir, thresh in folds:
        f = foldleft if dir == 'x' else foldright
        dots = set(f(p, thresh) for p in dots)

    Xs, Ys = zip(*dots)

    # Uncomment to get the magic numbers used for sizing 'res' :)
    # Xs, Ys = zip(*dots)
    # print("Mins: ", min(Xs), min(Ys))
    # print("Maxs: ", max(Xs), max(Ys))

    res = [[' ']*40 for x in range(8)]
    for x, y in dots:
        res[y][x] = 'X'

    return "\n" + "\n".join(''.join(x) for x in res)

# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
