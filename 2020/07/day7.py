

def parse_line(l):
    l = l.strip()
    u, right = l.split(" bags contain ")
    ns = []
    for v in right.split(","):
        v = v.strip()
        if v.count('bag') > 1:
            print("!!!! Found multiple bags!")
            exit()
        v = v.replace('.', '')
        v = v.replace(' bags', '')
        v = v.replace(' bag', '')
        if v.startswith('no'):
            ns.append((0, ''))
            continue
        i = v.index(' ')
        ns.append((int(v[:i]), v[i+1:]))
    return ((1, u), ns)


def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        return [parse_line(x) for x in f.readlines()]


def part1(inp):
    # TODO: make a graph from color -> bag-which-can-contain-it
    G = {}  # default dict would have been better!
    for ((_, t), ns) in inp:
        for (_, s) in ns:
            if not s in G:
                G[s] = [t]
                continue
            if not t in G[s]:
                G[s].append(t)

    seen = set(['shiny gold'])
    to_process = ['shiny gold']

    while to_process:
        u = to_process.pop()
        if u not in G:
            continue
        for v in G[u]:
            if v in seen:
                continue
            seen.add(v)
            to_process.append(v)

    return len(seen) - 1

def part2(inp):
    G = {}
    for ((_, t), ns) in inp:
        G[t] = ns


    r = {}
    return part2_recursive(G, 'shiny gold', r)

def part2_recursive(inp, color, R):
    # R[color -> # of bags needed inside.]

    if color in R:
        return R[color]

    r = 0
    for (c, v) in inp[color]:
        if c == 0:
            break
        r += c
        if v not in R:
            part2_recursive(inp, v, R)
        r += c*R[v]

    R[color] = r
    return r








a = get_input('day7.in')
print("part1: ", part1(a))
print("part2: ", part2(a))
# print(a)
