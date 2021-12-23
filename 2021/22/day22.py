from collections import defaultdict
from functools import reduce


def get_input(fname):
    def mapline(ln):
        onoff, r = ln.strip().split(" ")

        xyz = map(
                lambda rng: tuple(int(a) for a in rng[2:].split("..")),
                r.split(",")
                )
        return (onoff, Block(*xyz))

    with open(fname, 'r') as f:
        return list(map(mapline, f.readlines()))


class Block:

    def __init__(self, xs, ys, zs):
        self.x0, self.x1 = xs
        self.y0, self.y1 = ys
        self.z0, self.z1 = zs

        self.p0 = (self.x0, self.y0, self.z0)
        self.p1 = (self.x1, self.y1, self.z1)

    def __repr__(self):
        return "({}, {}), ({}, {}), ({}, {})".format(
                self.x0, self.x1, self.y0, self.y1, self.z0, self.z1)

    def area(self):
        return (self.x1+1-self.x0)*(self.y1+1-self.y0)*(self.z1+1-self.z0)

    # Split the block on the given axis into (a0, num-1) and (num, a1)
    def split(self, axis, num):
        assert self.p0[axis] < num <= self.p1[axis]

        p1, p2 = list(self.p1), list(self.p0)
        p1[axis] = num-1
        p2[axis] = num
        return [
                Block(*zip(self.p0, p1)),
                Block(*zip(p2, self.p1))
                ]


    # Subtract out block B from self. Return a list of blocks representing all
    # cubes in self but not in B.
    def __sub__(self, B):
        # We will slowy "split" off blocks from A until A is the
        # the intersection of "self" and "B".
        res = []
        A = self

        # No intersection
        if (
                (A.x1 < B.x0 or B.x1 < A.x0) or
                (A.y1 < B.y0 or B.y1 < A.y0) or
                (A.z1 < B.z0 or B.z1 < A.z0)):
            return [self]

        # B contains A
        if (
                B.x0 <= A.x0 <= A.x1 <= B.x1 and
                B.y0 <= A.y0 <= A.y1 <= B.y1 and
                B.z0 <= A.z0 <= A.z1 <= B.z1):
            return []

        # split on Xs
        if A.x0 < B.x0:
            left, A = A.split(0, B.x0)
            res.append(left)
        if B.x1 < A.x1:
            A, right = A.split(0, B.x1+1)
            res.append(right)

        # Split on Ys
        if A.y0 < B.y0:
            left, A = A.split(1, B.y0)
            res.append(left)
        if B.y1 < A.y1:
            A, right = A.split(1, B.y1+1)
            res.append(right)

        # Split on Zs
        if A.z0 < B.z0:
            left, A = A.split(2, B.z0)
            res.append(left)
        if B.z1 < A.z1:
            A, right = A.split(2, B.z1+1)
            res.append(right)

        # A should be completely contained in B
        assert (
                B.x0 <= A.x0 <= A.x1 <= B.x1 and
                B.y0 <= A.y0 <= A.y1 <= B.y1 and
                B.z0 <= A.z0 <= A.z1 <= B.z1)

        # self should be the union of block A and the blocks in res.
        assert self.area() == sum(x.area() for x in res) + A.area()

        return res


# Flatten a list of lists of elements into a list of elements.
def flatten(L):
    res = []
    for item in L:
        res.extend(item)
    return res


def solution(inp):
    on_blocks = []

    for onoff, block in inp:
        on_blocks = flatten(
                map(lambda s: s-block, on_blocks))
        if onoff == 'on':
            on_blocks.append(block)

    return sum(map(lambda s: s.area(), on_blocks))


def part1(inp):
    def block_filter(sh):
        return all(abs(x) <= 50 for x in (sh.x0, sh.x1, sh.y0, sh.y1, sh.z0, sh.z1))

    return solution(filter(lambda x: block_filter(x[1]), inp))


inp = get_input("input.txt")

print("part1: ", part1(inp))
print("part2: ", solution(inp))

