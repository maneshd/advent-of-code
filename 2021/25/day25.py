def get_input(fname):
    with open(fname, 'r') as f:
        res = {}
        lines = f.readlines()
        for (row, contents) in enumerate(lines):
            for (col, ch) in enumerate(contents.strip()):
                if ch == '.':
                    continue
                res[(row, col)] = ch
        return res, len(lines), len(lines[0].strip())


def step_right(d, cols):
    res, n = {}, 0

    def right(r, c):
        return r, (c+1)%cols

    for ((r, c), ch) in d.items():
        if ch == '>' and right(r, c) not in d:
            res[right(r, c)] = '>'
            n += 1
        else:
            res[(r, c)] = ch

    return res, n


def step_down(d, rows):
    res, n = {}, 0

    def down(r, c):
        return (r+1)%rows, c

    for ((r, c), ch) in d.items():
        if ch == 'v' and down(r, c) not in d:
            res[down(r, c)] = 'v'
            n += 1
        else:
            res[(r, c)] = ch

    return res, n


def step(d, rows, cols):
    d1, n1 = step_right(d, cols)
    d2, n2 = step_down(d1, rows)
    return d2, n1+n2


def part1(d, rows, cols):
    for steps in range(1, 100000):
        d, n = step(d, rows, cols)
        if n == 0:
            return steps


inp = get_input("input.txt")
print("part1: ", part1(*inp))

