import ast  # this feels like cheating
from functools import cmp_to_key

def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


# Get the grid, and replace the start/end w/ their elevations.
def _get_input(f):
    pairs = f.read().strip().split("\n\n")
    return [
            [ast.literal_eval(x) for x in pair.split("\n")]
            for pair in pairs
            ]

def compare(A, B):
    if type(A) is int and type(B) is int:
        return 0 if A == B else (-1 if A < B else 1)
    if type(A) is int:
        return compare([A], B)
    if type(B) is int:
        return compare(A, [B])

    # A and B are lists
    for (a, b) in zip(A, B):
        r = compare(a, b)
        if r != 0:
            return r

    return 0 if len(A) == len(B) else (-1 if len(A) < len(B) else 1)


def part1(pairs):
    return sum(i+1 for i in range(len(pairs)) if compare(*pairs[i]) == -1)


def part2(pairs):
    lines = [line for pair in pairs for line in pair]
    dividers = [[[2]], [[6]]]
    lines.extend(dividers)
    lines.sort(key=cmp_to_key(compare))
    return (lines.index(dividers[0])+1) * (lines.index(dividers[1])+1)


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
