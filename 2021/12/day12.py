from collections import defaultdict
from functools import reduce
from itertools import product

def get_input(fname):
    with open(fname, 'r') as f:
        res = defaultdict(lambda: [])
        for line in f.readlines():
            u, v = line.strip().split("-")
            res[u].append(v)
            res[v].append(u)
        return res


def part1(G):
    seen = set()
    to_process = [('start',)]
    res = []

    while to_process:
        path = to_process.pop()

        for v in G[path[-1]]:
            if v in path and v.islower():
                continue

            newpath = path + (v,)
            if newpath in seen:
                continue
            seen.add(newpath)

            if v == 'end':
                res.append(newpath)
            else:
                to_process.append(newpath)

    return len(res)

def part2(G):
    seen = set()
    to_process = [(('start',), True)]
    res = []

    while to_process:
        path, room_for_double = to_process.pop()

        for v in G[path[-1]]:
            if v == 'start':
                continue

            seenv = v in path and v.islower()
            if seenv and not room_for_double:
                continue

            newpath = path + (v,)
            if newpath in seen:
                continue
            seen.add(newpath)

            if v == 'end':
                res.append(newpath)
            else:
                to_process.append((newpath, room_for_double and not seenv))

    return len(res)


# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
