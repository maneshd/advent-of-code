from collections import defaultdict
from functools import reduce


def get_input(fname):

    def map_line(line):
        return tuple(line.strip().split())

    def map_chunk(chunk):
        return list(map(map_line, chunk.strip().split("\n")))

    with open(fname, 'r') as f:
        return list(map(map_chunk, f.read().strip().split("inp w\n")[1:]))


class ALU:

    ops = {
            'add': lambda a,b: a+b,
            'mul': lambda a,b: a*b,
            'div': lambda a,b: a//b,
            'mod': lambda a,b: a%b,
            'eql': lambda a,b: 1 if a==b else 0,
            }

    @staticmethod
    def make_ALUs(instruction_blocks):
        return list(map(lambda x: ALU(x), instruction_blocks))

    def __init__(self, instructions):
        self.instructions = instructions

    def run(self, inp, x, y, z):
        v = [inp, x, y, z]

        def get(c):
            return v['wxyz'.index(c)] if c in 'wxyz' else int(c)

        for (op, v1, v2) in self.instructions:
            v['wxyz'.index(v1)] = self.ops[op](get(v1), get(v2))

        return tuple(v)


'''
This solution uses a pretty slow dynamic-programming approach. It's
likely there's a much faster way to do this, but oh well!

note: rangefn should return either 0..9 or 9..0 depending on if we
want the min/max result, respectively.
'''
def solution(inp, rangefn):
    alus = ALU.make_ALUs(inp)

    # F(epoch, z) = highest/lowest input digit such that F(epoch, z') can
    # succeed OR false if not possible.
    # NOTE: this relies on registers x and y always being reset to 0.
    def F(epoch, z, memo={}):
        if (epoch, z) in memo:
            return memo[(epoch, z)]

        for w in rangefn():
            # Show the current status.
            if epoch == 0:
                print("trying: {}...".format(w))
            elif epoch == 1:
                print("trying: x{}...".format(w))

            z2 = alus[epoch].run(w, 0, 0, z)[3]
            last_epoch = epoch == len(alus)-1
            if (
                    (last_epoch and z2 == 0) or
                    (not last_epoch and F(epoch+1, z2))):
                memo[(epoch, z)] = w
                return w
        memo[(epoch, z)] = False
        return False

    memo = {}
    res = []
    d = 0
    z = 0

    for (i, alu) in enumerate(alus):
        d = F(i, z, memo)
        z = alu.run(d, 0, 0, z)[3]
        res.append(d)

    return ''.join(str(x) for x in res)


def part1(inp):
    return solution(inp, lambda: range(9, 0, -1))


def part2(inp):
    return solution(inp, lambda: range(1, 10))


inp = get_input("input.txt")


print("part1: ", part1(inp))  # 91699394894995
print("part2: ", part2(inp))  # 51147191161261

