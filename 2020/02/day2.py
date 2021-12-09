from collections import namedtuple

PW = namedtuple("password", ["low", "high", "char", "pwd"])

def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        for l in f.readlines():
            nums, char, pwd = l.strip().split()
            low, high = nums.split('-')
            char = char[0]
            res.append(PW(int(low), int(high), char, pwd))
    return res

def is_good(pwd):
    c = sum(1 for x in pwd.pwd if x == pwd.char)
    return pwd.low <= c and c <= pwd.high

a = get_input("day2.in")

good_count = sum(1 for x in a if is_good(x))
print("part 1: ", good_count)

def is_part2_good(p):
    a, b = p.pwd[p.low-1], p.pwd[p.high-1]
    return (a == p.char and b != p.char) or (a != p.char and b == p.char)

part2 = sum(1 for x in a if is_part2_good(x))
print("part 2: ", part2)
