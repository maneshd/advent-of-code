from collections import deque

def get_input(fname):
    res = [[], []]
    idx = 0
    with open(fname, 'r') as f:
        for l in f.readlines():
            l = l.strip()
            if "Player" in l:
                continue
            if l == '':
                idx = 1
                continue
            res[idx].append(int(l))
    return res

def part1(inp):
    A, B = deque(inp[0]), deque(inp[1])

    while A and B:
        a, b = A.popleft(), B.popleft()
        if a > b:
            A.extend((a, b))
        else:
            B.extend((b, a))

    w = A if A else B

    return sum((i+1)*v for i, v in enumerate(reversed(w)))


# memo: (A, B) -> (end A, end B)
MEMO = {}

def part2(inp):
    A, B = get_winner(*inp)
    w = A if A else B
    return sum((i+1)*v for i, v in enumerate(reversed(w)))

def get_winner(p1, p2):
    start = (tuple(p1), tuple(p2))
    if start in MEMO:
        return MEMO[start]

    A, B = deque(p1), deque(p2)

    seen = set()
    state = start

    while A and B and state not in seen:
        seen.add(state)
        a, b = A.popleft(), B.popleft()

        if a <= len(A) and b <= len(B):
            reca, recb = get_winner(tuple(A)[:a], tuple(B)[:b])
            if not reca:
                B.extend((b, a))
            else:
                A.extend((a, b))
        elif a < b:
            B.extend((b, a))
        else:
            A.extend((a, b))

        state = (tuple(A), tuple(B))
        if state in MEMO:
            return MEMO[state]

    res = (tuple(A), tuple(B))
    MEMO[start] = res
    return res


inp = get_input("day22.in")
# print("part1:", part1(inp))
print("part2:", part2(inp))
print("solved {} subproblems!".format(len(MEMO)))
