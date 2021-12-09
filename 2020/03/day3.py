from functools import reduce

def get_input(fname):
    with open(fname, 'r') as f:
        return [x.strip() for x in f.readlines()]

def count_trees(board, dx, dy):
    x, y = 0, 0
    trees = 0
    while y < len(board):
        if board[y][x] == "#":
            trees += 1
        y+=dy
        x = (x + dx) % len(board[0])
    return trees

board = get_input("day3.in")
print("part 1: ", count_trees(board, 1, 3))

part2_input = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
part2 = reduce((lambda x, y: x * y), [count_trees(board, x, y) for (x, y) in part2_input])

print("part 2: ", part2)
