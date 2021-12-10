from functools import reduce

def get_input(fname):
    with open(fname, 'r') as f:
        return [s.strip() for s in f.readlines()]


PARENS = ['()', '[]', '{}', '<>']
LTR = {p[0]:p[1] for p in PARENS}
RTL = {p[1]:p[0] for p in PARENS}
LPARENS = [p[0] for p in PARENS]
RPARENS = [p[1] for p in PARENS]

# Get the matching paren
def get_match(paren):
    return LTR[paren] if paren in LPARENS else RTL[paren]

# returns '' if not corrupted.
def get_corrupted_char(line):
    stack = []
    for c in line:
        if c in LPARENS:
            stack.append(c)
            continue
        # c is a right paren
        if not stack:
            print("This shouldn't happen!")
            return ''

        if get_match(c) != stack.pop():
            return c
    return ''

# returns '' if corrupted or complete
def get_completion(line):
    stack = []
    for c in line:
        if c in LPARENS:
            stack.append(c)
            continue

        if not stack:
            print("This shouldn't happen!")
            exit()

        if get_match(c) != stack.pop():
            return ''

    return ''.join(map(get_match, reversed(stack)))


def part1(inp):
    POINTS = {')': 3, ']':57, '}': 1197, '>': 25137}
    return sum(POINTS[ch] for ch in map(get_corrupted_char, inp) if ch != '')

def part2(inp):
    points = {')':1, ']':2, '}':3, '>':4}
    def score(parens):
        return reduce(lambda prev, cur: prev*5 + points[cur], parens, 0)
    scores = [score(p) for p in map(get_completion, inp) if p != '']
    scores.sort()
    return scores[len(scores)//2]


# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
