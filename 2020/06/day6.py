
def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        return [x.strip() for x in f.readlines()]

def part1(inp):
    res = []
    s = set()
    for row in inp:
        if not row and s:
            res.append(s)
            s = set()
            continue
        for c in row:
            s.add(c)

    if s:
        res.append(s)

    return sum(len(s) for s in res)



def part2(inp):
    groups = []
    groups.append([])
    for row in inp:
        if row:
            groups[-1].append(set(x for x in row))
        else:
            groups.append([])

    res = 0
    for g in groups:
        s = g[0]
        for t in g[1:]:
            s = s & t
        res += len(s)

    return res




# def part2(inp):
#     res = []
#     ss = set()
#     for x in 'abcdefghijklmnopqrstuvwxyz':
#         ss.add(x)
#     s = set(ss)
#     for row in inp:
#         if not row:
#             if s:
#                 res.append(s)
#             s = set(ss)
#         t = set()
#         for c in row:
#             t.add(c)
#         s = s & t
#
#     if s:
#         res.append(s)
#
#     for s in res:
#         print("size=", len(s), " -- ", s)
#
#     return sum(len(s) for s in res)


inp = get_input("day6.in")
# inp = get_input("test.in")
print("part1: ", part1(inp))
print("part2: ", part2(inp))
