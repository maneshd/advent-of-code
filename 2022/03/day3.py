
def get_input(fname):
    with open(fname, "r") as f:
        return [x.strip() for x in f.readlines()]

def split_string(s):
    n = len(s)
    return (s[:n//2], s[n//2:])

def points(ch):
    return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(ch) + 1

def by3(L):
    for i in range(0, len(L), 3):
        yield L[i:i+3]

def part1(data):
    res = 0
    for L, R in map(split_string, data):
        item = list(set(L).intersection(set(R)))[0]
        res += points(item)
    return res

def part2(data):
    res = 0
    for A, B, C in by3(data):
        item = list(set(A).intersection(set(B)).intersection(set(C)))[0]
        res += points(item)
    return res

d = get_input("input.txt")
print("part1: ", part1(d))
print("part2: ", part2(d))

