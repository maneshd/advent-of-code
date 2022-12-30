def get_input(fname):
    with open(fname, 'r') as f:

        def handle_line(line):
            line = line.strip()
            L, R = line.split(": ")
            name = L
            for op in "+-*/":
                if op in R:
                    return (L, op, tuple(x for x in R.split(f' {op} ')))
            return (L, None, int(R))

        monkeys = map(handle_line, f.readlines())
        return {name: (op, val) for (name, op, val) in monkeys}

OPS = {
        "+": lambda a, b: a+b,
        "-": lambda a, b: a-b,
        "*": lambda a, b: a*b,
        "/": lambda a, b: a/b,
        }


def part1(inp):
    def get_val(name, memo={}):
        if name in memo:
            return memo[name]
        op, val = inp[name]

        res = val if op is None else OPS[op](get_val(val[0]), get_val(val[1]))
        memo[name] = res
        return res

    return int(get_val("root"))


def do_op(op, L, R):
    if type(L) is not tuple and type(R) is not tuple:
        return OPS[op](L, R)

    if type(L) is tuple:
        # (ax + b) OP c
        a, b = L
        c = R
        if op == "+":
            return a, b+c
        elif op == "-":
            return a, b-c
        elif op == "*":
            return a*c, b*c
        else:
            return a/c, b/c

    a, b = R
    c = L
    # c OP (ax + b)
    if op == "+":
        return a, b+c
    elif op == "-":
        return -a, c-b
    elif op == "*":
        return a*c, b*c
    else:
        # lol, hope we don't get here :)
        print("UH OH LOL")
        exit()


'''
Note: this only works because we have a polytree/directed tree.
'''
def part2(inp):
    deps = {}

    op, vals = inp["root"]
    inp["root"] = ("-", vals)
    inp["humn"] = (None, (1, 0))

    def get_val(name, memo={}):
        if name in memo:
            return memo[name]
        op, val = inp[name]

        if op is None:
            memo[name] = val
            return val
        else:
            v1, v2 = val
            res = do_op(op, get_val(v1), get_val(v2))
            memo[name] = res
            return res

    a, b = get_val("root")
    return int(round(-b/a))


inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))

