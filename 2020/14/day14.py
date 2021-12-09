from collections import defaultdict

def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        for line in f.readlines():
            l, r = line.strip().split(' = ')
            if l == 'mask':
                res.append(('mask', r))
            else:
                i = l.index('[')
                res.append((int(l[i+1:-1]), int(r)))
    return res

inp = get_input("day14.in")


class Mask:

    def __init__(self, x):
        self.andval = int(''.join(i if i == '0' else '1' for i in x), 2)
        self.orval = int(''.join(i if i == '1' else '0' for i in x), 2)

    def apply(self, x):
        return x & self.andval | self.orval

def part1(inp):
    mask = Mask('X'*32)
    res = {}
    for l, r in inp:
        if l == 'mask':
            mask = Mask(r)
            continue
        res[l] = mask.apply(r)

    return sum(v for _, v in res.items())


def get_combos(n):
    res = []
    if n == 0:
        return []

    current = [0]*n
    res.append(current)

    while len(res) < 2**n:
        current = current[:]
        i = current.index(0)
        current[i] = 1
        for j in range(i):
            current[j] = 0
        res.append(current)

    return res



class Mask2:

    def __init__(self, mask):
        self.orval = int(''.join(i if i == '1' else '0' for i in mask), 2)
        self.xs = [x == 'X' for x in mask]
        return

    def apply(self, x):
        tmpl = bin(x | self.orval)[2:]
        # now it's a string '100101001'
        tmpl = '0'*(36-len(tmpl)) + tmpl
        tmpl = ''.join('{}' if isX else t for (t, isX) in zip(tmpl, self.xs))

        numx = len([x for x in self.xs if x])
        return [int(tmpl.format(*x), 2) for x in get_combos(numx)]

def part2(inp):
    mask = Mask2('0'*36)
    res = {}
    for l, r in inp:
        if l == 'mask':
            mask = Mask2(r)
            continue
        for ll in mask.apply(l):
            res[ll] = r

    return sum(v for _, v in res.items())




print("part1: ", part1(inp))
print("part2: ", part2(inp))

# for x in get_combos(3):
#     print(x)



# a = Mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')
# print("mask(11)={}".format(a.apply(11)))
# print("mask(101)={}".format(a.apply(101)))
# print("mask(0)={}".format(a.apply(0)))
