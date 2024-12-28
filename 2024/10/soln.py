
def parse_input(file_name):
    with open(file_name, 'r') as f:
        parse_line = lambda l: [int(x) for x in l]
        return list(map(parse_line, f.read().split("\n")))


def find_nines(M, i, j, memo):
    n = M[i][j]
    if n == 9:
        return {(i, j)}
    if (i, j) in memo:
        return memo[(i, j)]

    in_bounds = lambda i, j: 0 <= i and 0 <= j and i < len(M) and j < len(M[0])

    res = set()
    for (a, b) in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
        if in_bounds(a, b) and M[a][b] == n+1:
            res = res.union(find_nines(M, a, b, memo))
    memo[(i, j)] = res
    return res


def calc_rating(M, i, j, memo):
    n = M[i][j]
    if n == 9:
        return 1
    if (i, j) in memo:
        return memo[(i, j)]

    in_bounds = lambda i, j: 0 <= i and 0 <= j and i < len(M) and j < len(M[0])

    res = sum(
        calc_rating(M, a, b, memo)
        for (a, b) in ((i+1, j), (i-1, j), (i, j+1), (i, j-1))
        if in_bounds(a, b) and M[a][b] == n+1
    )
    memo[(i, j)] = res
    return res


def part1(M):
    memo = {}
    res = 0
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] == 0:
                res += len(find_nines(M, i, j, memo))
    return res


def part2(M):
    memo = {}
    return sum(
        calc_rating(M, i, j, memo)
        for i in range(len(M)) for j in range(len(M[0]))
        if M[i][j] == 0
    )


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))
