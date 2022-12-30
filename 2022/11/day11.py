from functools import reduce

def get_input(fname):
    with open(fname, 'r') as f:
        return list(_get_input(f))


def _get_input(f):
    def make_monkey(monkey_lines):
        L = monkey_lines.split("\n")
        items = list(map(int, L[1].split(": ")[1].split(", ")))
        op = L[2].split(" = ")[1]
        testDiv = int(L[3].split("divisible by ")[1])
        trueCase = int(L[4][-1])
        falseCase = int(L[5][-1])
        return (items, op, testDiv, trueCase, falseCase)

    return map(make_monkey, f.read().strip().split("\n\n"))


def runXRounds(N, monkeys, run_operation):
    activity = [0]*len(monkeys)

    # make a copy
    def copy_monkey(m):
        res = list(m)
        res[0] = res[0][:]
        return tuple(res)
    monkeys = list(map(copy_monkey, monkeys))

    for x in range(N):
        for (i, monkey) in enumerate(monkeys):
            (items, op, testDiv, trueCase, falseCase) = monkey
            while items:
                activity[i] += 1
                item = items.pop(0)
                item = run_operation(op, item)
                j = trueCase if item % testDiv == 0 else falseCase
                monkeys[j][0].append(item)

    activity.sort()
    return activity[-1] * activity[-2]


def part1(monkeys):
    def run_operation(opString, val):
        a, op, b = opString.split(" ")
        left = (val if a == "old" else int(a))
        right = (val if b == "old" else int(b))
        return (left + right if op == "+" else left*right) // 3
    return runXRounds(20, monkeys, run_operation)


def part2(monkeys):
    lcm = reduce(lambda a, b: a*b, [m[2] for m in monkeys])
    def run_operation(opString, val):
        a, op, b = opString.split(" ")
        left = (val if a == "old" else int(a))
        right = (val if b == "old" else int(b))
        return (left + right if op == "+" else left*right) % lcm
    return runXRounds(10000, monkeys, run_operation)


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
