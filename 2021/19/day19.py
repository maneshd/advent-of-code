from itertools import combinations

# Why not roll your own class for a 3x3 matrix?
class Transform:

    def __init__(self, M):
        self.M = list(M)

    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(*map(
                lambda i: sum(a*b for a, b in zip(self.M[i], other.V)),
                range(3)
                ))

        if isinstance(other, Transform):
            A = self.M
            B = list(zip(*other.M))

            M = [[0]*3 for x in range(3)]
            for i in range(3):
                for j in range(3):
                    M[i][j] = sum(a*b for (a, b) in zip(A[i], B[j]))

            return Transform(M)

    def __repr__(self):
        return "{}\n{}\n{}\n".format(*self.M)


class Vec:
    def __init__(self, x, y, z):
        self.V = (x, y, z)

    def __repr__(self):
        return "({}, {}, {})".format(*self.V)

    def __eq__(self, other):
        return self.V == other.V

    def __hash__(self):
        return hash(self.V)

    def __add__(self, other):
        return Vec(*(a+b for a, b in zip(self.V, other.V)))

    def __sub__(self, other):
        return Vec(*(a-b for a, b in zip(self.V, other.V)))



I = Transform([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
rotX = Transform([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
rotY = Transform([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
rotZ = Transform([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

transforms = set()
for T1 in (I, rotY, rotY*rotY, rotY*rotY*rotY, rotZ, rotZ*rotZ*rotZ):
    for T2 in (I, rotX, rotX*rotX, rotX*rotX*rotX):
        transforms.add(T1*T2)


def get_input(fname):
    with open(fname, 'r') as f:
        res = []

        for block in f.read().strip().split("\n\n"):
            lines = block.split("\n")
            beacons = set(Vec(*map(int, line.split(","))) for line in lines[1:])
            res.append(beacons)

        return res


'''
Attempt to align the beacons in B w/ the beacons in A.

If more than 12 beacons can be aligned, then returns two things:
    1) The beacons in B transformed to A's coordinates.
    2) The (x, y, z) coordinates of B's sensor station, in A's coordinates.

Returns (False,False) if it's impossible to align 12 or more beacons between
A and B.
'''
def align(A, B):
    # try every transformation/rotation of B's coordinate system
    for T in transforms:
        B_t = set(T*b for b in B)

        # For every pair of beacons in A and B_t, try aligning them and
        # see how many others align.
        for b in B_t:
            for a in A:
                diff = a - b
                B_candidate = set(x+diff for x in B_t)
                if len(A.intersection(B_candidate)) >= 12:
                    return B_candidate, diff

    return False, False


def solution(inp):
    fixed = [inp[0]]
    to_explore = [inp[0]]
    remaining = inp[1:]
    deltas = [Vec(0, 0, 0)]

    while to_explore and len(fixed) < len(inp):
        A = to_explore.pop()
        new_remaining = []

        for B in remaining:
            B_aligned, delta = align(A, B)
            if B_aligned:
                fixed.append(B_aligned)
                to_explore.append(B_aligned)
                deltas.append(delta)
                print("Num fixed: ", len(fixed))
            else:
                new_remaining.append(B)

        remaining = new_remaining

    # Now 'fixed' should contain all sets of readings from 'inp'
    assert len(fixed) == len(inp)

    res = set()
    for beacons in fixed:
        for beacon in beacons:
            res.add(beacon.V)
    part1 = len(res)

    dist = lambda ab: sum(map(abs, (ab[0]-ab[1]).V))
    part2 = max(map(dist, combinations(deltas, 2)))

    return part1, part2


inp = get_input("input.txt")
#  inp = get_input("test.txt")

print("parts 1 and 2:", solution(inp))

