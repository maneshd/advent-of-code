from collections import defaultdict

inp1 = [14,1,17,0,3,20]

def part1(inp):
    i = 1
    d = {}

    # setup
    for x in inp:
        d[x] = i
        i += 1

    cur = 0
    # while i < 2020:
    while i < 30000000:
        # 30 000 000
        # cur is the i-th thing.
        nxt = 0 if cur not in d else i - d[cur]
        d[cur] = i

        # advance
        cur = nxt
        i += 1

    return cur


# print(part1([1, 3, 2]))
# print(part1([2, 1, 3]))
print("part1: ", part1(inp1))
# print("part2: ", part2(inp))
