from collections import defaultdict

def get_input(filename):
    with open(filename, 'r') as f:
        L, R = f.read().split("\n\n")
        def parse_constraint(line):
            return tuple(int(x) for x in line.split("|"))
        constraints = list(map(parse_constraint, L.split("\n")))
        def parse_update(line):
            return tuple(int(x) for x in line.split(","))
        updates = list(map(parse_update, R.split("\n")))
        return constraints, updates


def build_constraints(constraints):
    res = defaultdict(lambda: [])
    for (a, b) in constraints:
        res[a].append(b)
    return res


def check_update(update, C):
    for i, n in enumerate(update):
        if any(x in C[n] for x in update[:i]):
            return False
    return True

def correct_update(U, C):
    U = list(U)
    for i, n in enumerate(U):
        for j in range(i):
            if U[j] in C[n]:
                # swap backwards
                while i > j:
                    U[i], U[i-1] = U[i-1], U[i]
                    i -= 1
                return correct_update(U, C) # might be more :)
    return U


def part1(constraints, updates):
    C = build_constraints(constraints)
    valid = [u for u in updates if check_update(u, C)]
    return sum(L[len(L)//2] for L in valid)


def part2(constraints, updates):
    C = build_constraints(constraints)
    invalid = [u for u in updates if not check_update(u, C)]
    fixed = [correct_update(U, C) for U in invalid]
    return sum(L[len(L)//2] for L in fixed)


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(*inp))
    print("part 2:", part2(*inp))