import re


s = "\n".join((
"Button A: X\+(\d+), Y\+(\d+)",
"Button B: X\+(\d+), Y\+(\d+)",
"Prize: X=(\d+), Y=(\d+)"))


def parse_input(file_name):
    def parse_block(text):
        m = re.search(s, text)
        assert(m)
        res = (m[1], m[2], m[3], m[4], m[5], m[6])
        return tuple(map(int, res))

    with open(file_name, 'r') as f:
        return list(map(parse_block, f.read().strip().split("\n\n")))


def solve(x1, y1, x2, y2, x, y):
    A = (y - x*y2/x2) / (y1 - x1*y2/x2)
    B = (x - A*x1)/x2
    return (A, B)


def is_valid(a, b, x1, y1, x2, y2, x, y):
    a, b = round(a), round(b)
    return a >= 0 and b >= 0 and a*x1+b*x2 == x and a*y1+b*y2 == y


def part1(inp):
    solns_w_probs = map(lambda x: (solve(*x), x), inp)
    valid_solns = [soln for (soln, prob) in solns_w_probs if is_valid(*soln, *prob)]
    As, Bs = zip(*valid_solns)
    return round(3*sum(As) + sum(Bs))


def part2(inp):
    fix_target = lambda n: 10000000000000 + n
    def fix_problem(p):
        x1, y1, x2, y2, x, y = p
        return x1, y1, x2, y2, fix_target(x), fix_target(y)
    fixed_problems = map(fix_problem, inp)
    return part1(fixed_problems)


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))
