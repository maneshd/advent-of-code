from collections import deque

def parse_input(fname):
    with open(fname, 'r') as f:
        return f.read().split("\n")


indices = lambda M: ((i,j) for i in range(len(M)) for j in range(len(M[0])))
find_chars = lambda M, ch: ((i,j) for (i,j) in indices(M) if M[i][j] in ch)
find_char = lambda M, ch: list(find_chars(M,ch))[0]
in_bounds = lambda M, i, j: 0<=i and 0<=j and i<len(M) and j<len(M[0])


def bfs(M, s):
    SP, Q = {s:0}, deque([s])

    while Q:
        i,j = Q.popleft()
        for (i2,j2) in ((i,j+1),(i,j-1),(i+1,j),(i-1,j)):
            if in_bounds(M,i,j) and M[i][j] != "#" and (i2,j2) not in SP:
                SP[(i2,j2)] = SP[(i,j)]+1
                Q.append((i2,j2))
    return SP


# Yields all points within a manhattan distance of d
def cheat_dests(i, j, d):
    for di in range(-d, d+1, 1):
        for dj in range(-d, d+1, 1):
            if abs(di) + abs(dj) <= d:
                yield (i+di, j+dj)


def soln(M, cheat_length):
    s, t = find_char(M, 'S'), find_char(M, 'E')
    DS, DE = bfs(M, s), bfs(M, t)
    cheats = {}  # cheat -> savings

    for i,j in find_chars(M, '.S'):
        for i2,j2 in cheat_dests(i,j,cheat_length):
            if not in_bounds(M, i2, j2) or M[i2][j2] == '#':
                continue
            cost = DS[(i,j)] + abs(i2-i) + abs(j2-j) + DE[(i2,j2)]
            savings = DS[t] - cost
            if savings > 0:
                cheats[((i,j),(i2,j2))] = savings
    return sum(1 for v in cheats.values() if v >= 100)


if __name__ == "__main__":
    M = parse_input("inp.txt")
    print("part 1:", soln(M,2))
    print("part 2:", soln(M,20))