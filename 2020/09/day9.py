def get_input(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.readlines()]

inp = get_input("day9.in")

def is_sum_of_2(xs, y):
    need = set()
    for x in xs:
        if x in need:
            return True
        need.add(y-x)
    return False

def part1(inp):
    for i in range(25, len(inp)):
        if not is_sum_of_2(inp[i-25:i], inp[i]):
            return inp[i]

print("part1:", part1(inp))

target = part1(inp)

def part2(inp, target):
    i, j = 0, 0
    c = inp[0]

    while i < len(inp):
        while c < target:
            j += 1
            if j >= len(inp):
                print("something went wrong?")
                exit()
            c += inp[j]
        if c == target:
            nums = inp[i:j+1]
            return min(nums) + max(nums)
            # print("i=", i, "j=", j)
            # print("inp[i] + inp[j] = ", inp[i], "+", inp[j], "=", inp[i]+inp[j])
            # print("sum(inp[i:j+1] =", sum(inp[i:j+1]))
            # print("target=", target)
            # return inp[i] + inp[j]
        # if i < 10:
        # print("i=", i, "j=", j, "sum=", c, "target=", target, "len(inp)=", len(inp))
        c -= inp[i]
        i += 1

print("part2:", part2(inp, target))
