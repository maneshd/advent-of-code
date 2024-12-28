def get_input(filename):
    with open(filename, 'r') as f:
        return f.read().split("\n")


def positions(B):
    return ((i, j) for i in range(len(B)) for j in range(len(B[0])))


def start_pos(B):
    for (i, j) in positions(B):
        if B[i][j] == "^":
            return (i, j)


turn = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def part1(inp):
    B = [list(x) for x in inp]
    in_bounds = lambda i, j: 0 <= i and 0 <= j and i < len(B) and j < len(B[0])

    (x, y) = start_pos(B)
    dx, dy = (-1, 0)

    while in_bounds(x, y):
        if in_bounds(x+dx, y+dy) and B[x+dx][y+dy] == "#":
            dx, dy = turn[(dx, dy)]
            continue
        B[x][y] = "X"
        x, y = x+dx, y+dy

    count_x = lambda L: sum(1 for ch in L if ch == "X")
    return sum(map(count_x, B))
    

def has_loop(B, start_state):
    seen = {start_state}

    (x, y, dx, dy) = start_state
    
    in_bounds = lambda i, j: 0 <= i and 0 <= j and i < len(B) and j < len(B[0])
    while in_bounds(x, y):
        if in_bounds(x+dx, y+dy) and B[x+dx][y+dy] == "#":
            dx, dy = turn[(dx, dy)]
            seen.add((x, y, dx, dy))
            continue
        x, y = x+dx, y+dy
        if (x, y, dx, dy) in seen:
            return True
        else:
            seen.add((x, y, dx, dy))
    return False


def part2(inp):
    B = [list(x) for x in inp]

    (x, y) = start_pos(B)
    start_state = (x, y, -1, 0)

    res = 0

    for i in range(len(B)):
        for j in range(len(B[0])):
            if B[i][j] == ".":
                B[i][j] = "#"
                if has_loop(B, start_state):
                    res += 1
                B[i][j] = "."
    return res


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))