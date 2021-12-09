
def get_input(fname):
    with open(fname, 'r') as f:
        res = []
        mx = 0
        for line in f.readlines():
            l, r = line.split(' -> ')
            l = l.split(',')
            r = r.split(',')

            x1, y1 = int(l[0]), int(l[1])
            x2, y2 = int(r[0]), int(r[1])
            mx = max(mx, x1, y1, x2, y2)
            res.append(((x1, y1), (x2, y2)))
        print("Max:", mx)
        return res

def part1(inp):
    board = [[0 for x in range(1000)] for y in range(1000)]

    for ((x1, y1), (x2, y2)) in inp:

        if x1 != x2 and y1 != y2:
            pass

        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2+1):
                board[x1][y] += 1
            continue

        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2+1):
                board[x][y1] += 1
            continue

    return sum(sum(1 for x in row if x > 1) for row in board)

def print_board(board):
    for x in zip(*board):
        x = [str(y) if y != 0 else '.' for y in x]
        print(''.join(x))
    print()



def part2(inp):
    board = [[0 for x in range(1000)] for y in range(1000)]
    # board = [[0 for x in range(10)] for y in range(10)]

    for ((x1, y1), (x2, y2)) in inp:
        # print_board(board)
        # print(x1, y1, x2, y2)
        # print('({}, {}) => ({}, {})'.format((x1, y1, x2, y2)))
        # print()

        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2+1):
                board[x1][y] += 1
            continue

        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2+1):
                board[x][y1] += 1
            continue

        # now we have to do thiiiiiis!
        dx = 1 if x1 < x2 else -1
        dy = 1 if y1 < y2 else -1

        x, y = x1, y1
        board[x][y] += 1
        while x != x2:
            x += dx
            y += dy
            board[x][y] += 1

    return sum(sum(1 for x in row if x > 1) for row in board)






inp = get_input("test.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))

inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
