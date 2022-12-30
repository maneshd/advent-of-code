def get_input(fname):
    with open(fname, 'r') as f:
        board, directions = f.read().split("\n\n")
        return parse_board(board), parse_directions(directions.strip())

def parse_board(board):
    res = board.split("\n")
    ml = max(len(s) for s in res)
    res = [x + ' '*(ml-len(x)) for x in res]
    return res

def parse_directions(s):
    res = []
    i = 0
    while i < len(s):
        if s[i] in "LR":
            res.append(s[i])
            i += 1
        j = i+1
        while j < len(s) and s[j] not in "LR":
            j += 1
        res.append(int(s[i:j]))
        i = j

    return res

DIRECTIONS = [
        (0, 1),  # right
        (1, 0),  # down
        (0, -1),  # left
        (-1, 0),  # up
]

# FIRST IS ROW, SECOND IS COLUMN

def advance_state(pos, direction, command, board):
    if type(command) is str:
        x, y = direction
        new_direction = (y, -x) if command == "R" else (-y, x)
        return pos, new_direction

    # Command is: go forward "command" units
    for _ in range(command):
        r, c = pos
        dr, dc = direction

        r, c = (r+dr) % len(board), (c+dc) % len(board[0])
        while board[r][c] == " ":
            r, c = (r+dr) % len(board), (c+dc) % len(board[0])

        if board[r][c] == "#":
            return pos, direction

        pos = r, c

    return pos, direction


def part1(inp):
    board, commands = inp
    position = (0, board[0].index("."))
    direction = DIRECTIONS[0]

    for command in commands:
        position, direction = advance_state(position, direction, command, board)

    x, y = position
    x, y = x+1, y+1
    facing = DIRECTIONS.index(direction)

    return 1000*x + 4*y + facing


# Gonna do some hard-coding for part 2 :)

'''
DIAGRAM OF FACES W/ LABELS
  necessary to understand get_face() and step()

- 1 6
- 2 - 
4 3 -
5 - -

'''

FACES = {
        (0, 1): 1,
        (1, 1): 2,
        (2, 1): 3,
        (2, 0): 4,
        (3, 0): 5,
        (0, 2): 6,
}

N = 50

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def get_face(row, col):
    R, C = row // N, col // N
    return (FACES[(R, C)] if (R, C) in FACES else 0)

def rot_pos(direction, command):
    x, y = direction
    return ((y, -x) if command == "R" else (-y, x))

# Get the position that's one step in the direction given. Also gets the new direction, if that changes.
# Still returns the pos + direction if the board is occupied at that point.
def step(pos, direction):
    r, c = pos
    dr, dc = direction
    end_face = get_face(r+dr, c+dc)

    # Case 0: faces are naturally aligned.
    if end_face != 0:
        return (r+dr, c+dc), (direction)

    # ELSE: we need to figure out which face we're moving too and act accordingly...
    start_face = get_face(r, c)
    if start_face == 1:
        if direction == LEFT:
            r = 3*N-1-r
            c = 0
            return (r, c), RIGHT
        elif direction == UP:
            r, c = (3*N + c % 50), 0
            return (r, c), RIGHT
    elif start_face == 2:
        if direction == LEFT:
            r, c = (2*N, r%N)
            return (r, c), DOWN
        elif direction == RIGHT:
            r, c = (N-1, 2*N + r%N)
            return (r, c), UP
    elif start_face == 3:
        if direction == RIGHT:
            r, c = (N-1 - r%N, 3*N-1)
            return (r, c), LEFT
        elif direction == DOWN:
            r, c = (3*N + c%N, N-1)
            return (r, c), LEFT
    elif start_face == 4:
        if direction == UP:
            r, c = (N+c, N)
            return (r, c), RIGHT
        elif direction == LEFT:
            r, c = (N-1 - r%N, N)
            return (r, c), RIGHT
    elif start_face == 5:
        if direction == LEFT:
            r, c = (0, N + r%N)
            return (r, c), DOWN
        elif direction == RIGHT:
            r, c = (3*N-1, N + r%N)
            return (r, c), UP
        elif direction == DOWN:
            r, c = (0, 2*N + c)
            return (r, c), DOWN
    elif start_face == 6:
        if direction == UP:
            r, c = (4*N-1, c%N)
            return (r, c), UP
        elif direction == RIGHT:
            r, c = (3*N-1 - r, 2*N-1)
            return (r, c), LEFT
        elif direction == DOWN:
            r, c = (N + c%N, 2*N-1)
            return (r, c), LEFT

    assert(False)


def part2(inp):
    board, commands = inp
    position = (0, N)
    direction = RIGHT

    for command in commands:
        if type(command) is str:
            direction = rot_pos(direction, command)
            continue

        assert(type(command) is int)
        steps = command
        for _ in range(command):
            (r, c), next_dir = step(position, direction)
            if board[r][c] == "#":
                break
            position, direction = (r, c), next_dir

    x, y = position
    x, y = x+1, y+1
    facing = DIRECTIONS.index(direction)

    return 1000*x + 4*y + facing

inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))

