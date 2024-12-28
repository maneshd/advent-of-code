TURN_COST = 1000
MOVE_COST = 1

def parse_input(file_name):
    with open(file_name, 'r') as f:
        return f.read().split("\n")


def find_char(M, ch):
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] == ch:
                return (i, j)


def get_neighbors(M, state, rev=False):
    x, y, dx, dy = state

    if dx == 0:
        yield (x, y, 1, 0), TURN_COST
        yield (x, y, -1, 0), TURN_COST
    else:
        yield (x, y, 0, 1), TURN_COST
        yield (x, y, 0, -1), TURN_COST

    i, j = (x-dx, y-dy) if rev else (x+dx, y+dy)
    if M[i][j] != "#":
        yield (i, j, dx, dy), MOVE_COST


def get_shortest_paths(M, sources, rev=False):
    scores = {}
    d = {s:0 for s in sources}

    while d:
        score, state = min((v, k) for k, v in d.items())  # sad priority queue
        scores[state] = score
        del d[state]

        for state, cost in get_neighbors(M, state, rev=rev):
            nscore = score+cost
            if state in scores:
                continue
            d[state] = min(d[state], nscore) if state in d else nscore
    return scores

def part1(M):
    i, j = find_char(M, "S")
    ti, tj = find_char(M, "E")
    SP = get_shortest_paths(M, ((i, j, 0, 1),))
    return min(SP[(ti, tj, dx, dy)] for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0)))


def part2(M):
    i, j = find_char(M, "S")
    ti, tj = find_char(M, "E")
    targets = [(ti, tj, dx, dy) for (dx, dy) in ((1,0), (-1,0), (0,1), (0,-1))]
    SP = get_shortest_paths(M, targets, rev=True)

    tiles = {(i, j), (ti, tj)}
    memo = {}

    def F(pos):
        (x, y, dx, dy) = pos
        if pos in memo:
            return memo[pos]
        elif (x, y) == (ti, tj):
            return 1
        
        res = 0
        for b, cost in get_neighbors(M, (x, y, dx, dy)):
            if SP[b] + cost == SP[pos]:
                tiles.add((b[0], b[1]))
                res += F(b)
        memo[pos] = res
        return res
    
    F((i, j, 0, 1))

    return len(tiles)


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))