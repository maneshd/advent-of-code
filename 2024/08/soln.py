from collections import defaultdict

def parse_input(file_name):
    with open(file_name, 'r') as f:
        return f.read().split("\n")


def get_pairs(L):
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            yield (L[i], L[j])


def get_antinodes1(M, x1, y1, x2, y2):
    yield (2*x2 - x1, 2*y2 - y1)
    yield (2*x1 - x2, 2*y1 - y2)



def get_antinodes2(M, x1, y1, x2, y2):
    in_bounds = lambda x, y: 0 <= x and 0 <= y and x < len(M) and y < len(M[0])
    dx, dy = x2-x1, y2-y1
    x, y = x2, y2
    while in_bounds(x, y):
        yield (x, y)
        (x, y) = (x+dx, y+dy)
    x, y = x2-dx, y2-dy
    while in_bounds(x, y):
        yield (x, y)
        (x, y) = (x-dx, y-dy)
    



def solution(M, get_antinodes):
    X, Y = len(M), len(M[0])
    towers = defaultdict(lambda: [])
    for (i, j) in ((i, j) for i in range(X) for j in range(Y)):
        if M[i][j] == ".":
            continue
        towers[M[i][j]].append((i, j))

    antinodes = set()
    for locations in towers.values():
        for (x1, y1), (x2, y2) in get_pairs(locations):
            for (x, y) in get_antinodes(M, x1, y1, x2, y2):
                if 0 <= x and 0 <= y and x < X and y < Y:
                    antinodes.add((x, y))

    return len(antinodes)




if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", solution(inp, get_antinodes1))
    print("part 2:", solution(inp, get_antinodes2))
