def parse_input(file_name):
    with open(file_name, 'r') as f:
        L, R = f.read().split("\n\n")
        M = [[ch for ch in line] for line in L.split("\n")]
        moves = R.replace("\n", "")
        return M, moves


def widen_map(M):
    charmap = { ".": "..", "#": "##", "O": "[]", "@": "@."}
    def widen_row(r):
        return [x for x in ''.join(charmap[ch] for ch in r)]
    return [widen_row(r) for r in M]


def coords_of(M, ch):
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] == ch:
                yield (i, j)


def find_start(M):
    return list(coords_of(M, "@"))[0]


diffs = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}


def execute_move(M, start_pos, move):
    dx, dy = diffs[move]
    x, y = start_pos[0]+dx, start_pos[1]+dy

    if M[x][y] == "#":
        return start_pos
    if M[x][y] == ".":
        return (x, y)

    # Part 1 boxes
    if M[x][y] == "O":
        ox, oy = x, y  # Object x/y
        # Keep going till we hit a wall or an empty space
        while M[ox][oy] == "O":
            ox, oy = ox+dx, oy+dy
        if M[ox][oy] == "#":
            return start_pos
        assert M[ox][oy] == ".", "Unexpected character (part 1)"
        M[ox][oy] = "O"
        M[x][y] = "."
        return (x, y)

    # Part 2 boxes
    assert M[x][y] in "[]", f"M[x][y]={M[x][y]}"
    def box_at(x, y):
        return ((x, y), (x, y+1)) if M[x][y] == "[" else ((x, y-1), (x, y))
    box = box_at(x, y)
    to_process = [box]
    boxes = set([box])

    # Check the space we're pushing the box into for more boxes, and repeat :)
    while to_process:
        # Handle each box half one at a time (they can push separate boxes)
        for (ox, oy) in to_process.pop():
            ox, oy = ox+dx, oy+dy
            if M[ox][oy] == "#":
                return start_pos
            if M[ox][oy] in "[]":
                box = box_at(ox, oy)
                if box not in boxes:
                    to_process.append(box)
                    boxes.add(box)

    # Move the boxes! Zero out their original positions first.
    for ((a, b), (c, d)) in boxes:
        M[a][b], M[c][d] = ".", "."
    for ((a, b), (c, d)) in boxes:
        M[a+dx][b+dy], M[c+dx][d+dy] = "[", "]"
    return x, y


def part1(inp):
    M, moves = inp
    (i, j) = find_start(M)
    M[i][j] = "."
    
    for move in moves:
        (i, j) = execute_move(M, (i, j), move)
    
    return sum(100*x+y for x, y in coords_of(M, "O"))


def part2(inp):
    M, moves = inp
    M = widen_map(M)
    (i, j) = find_start(M)
    M[i][j] = "."

    for move in moves:
        (i, j) = execute_move(M, (i, j), move)
    
    return sum(100*x+y for x, y in coords_of(M, "["))


if __name__ == "__main__":
    print("part 1:", part1(parse_input("inp.txt")))
    print("part 2:", part2(parse_input("inp.txt")))
