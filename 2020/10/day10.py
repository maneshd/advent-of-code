from collections import defaultdict

def get_input(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.readlines()]

def part1(L):
    L.sort()
    res = [0, 0, 0, 1]
    res[L[0]] += 1  # 0 -> L[0] for the outlet
    for a, b in zip(L, L[1:]):
        res[b-a] += 1
    return res[1] * res[3]

def part2(L):
    L = L[:]
    L.append(0)
    L.sort()
    L.reverse()

    R = defaultdict(lambda: 0)
    R[L[0]] = 1
    for i in L[1:]:
        R[i] = R[i+1] + R[i+2] + R[i+3]
    return R[0]

# tinp = get_input("test.in")
# part1(get_input("test.in"))

inp = get_input("day10.in")
print("part1:", part1(inp))
# print("part2 test:", part2(tinp))
print("part2:", part2(inp))
