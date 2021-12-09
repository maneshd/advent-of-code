
def get_input(fname):
    with open(fname, 'r') as f:
        nums = []
        boards = []
        cur_board = []

        for ln in f.readlines():
            if not nums:
                nums = [int(y) for y in ln.strip().split(",")]
                continue

            if ln.strip() == "":
                if cur_board:
                    boards.append(cur_board)
                    cur_board = []
                continue

            cur_board.append([int(x) for x in ln.strip().split()])
        if cur_board:
            boards.append(cur_board)

        return nums, boards


def mark_board(board, num):
    for row in board:
        while num in row:
            row[row.index(num)] = "X"

def check_board(board):
    for row in board:
        if all(item == "X" for item in row):
            return True
    for col in zip(*board):
        if all(item == "X" for item in col):
            return True
    return False

def sum_board(board):
    r = 0
    for row in board:
        r += sum(x for x in row if x != "X")
    return r

# if __name__ == "__main__"
def part1(inp):
    nums, boards = inp

    for num in nums:
        for board in boards:
            mark_board(board, num)
            if check_board(board):
                return sum_board(board) * num

    # print(nums)
    # for x in boards[-2]:
        # print(x)
    # print(boards[:2])
    return "doop"
    # return sum(1 for (x, y) in zip(L, L[1:]) if x < y)

def part2(inp):
    nums, boards = inp
    boards_ranking = []

    for num in nums:
        for idx, board in enumerate(boards):
            if idx in boards_ranking:
                continue

            mark_board(board, num)
            if check_board(board):
                boards_ranking.append(idx)
                if len(boards) == len(boards_ranking):
                    return num*sum_board(board)



inp = get_input("day4.in")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
