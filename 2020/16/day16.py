from collections import defaultdict

def get_input(fname):
    constraints = []
    yours = []
    tickets = []
    state = 'constraints'
    with open(fname, 'r') as f:
        for line in f.readlines():
            l = line.strip()
            if not l:
                continue
            if l == 'your ticket:':
                state = 'yours'
                continue
            if l == 'nearby tickets:':
                state = 'tickets'
                continue

            if state == 'constraints':
                name, right = l.split(':')
                bounds = []
                for bound in right.split(' or '):
                    x, y = bound.split('-')
                    bounds.append((int(x), int(y)))
                constraints.append((name, bounds))
                continue

            ll = yours if state == 'yours' else tickets
            ll.append([int(x) for x in l.split(',')])

    return constraints, yours[0], tickets


def valid_for_some_constraint(constraints, v):
    for name, constraint in constraints:
        for low, high in constraint:
            if low <= v and v <= high:
                return True
    return False

def part1(inp):
    constraints, mytick, tickets = inp

    res = 0

    for ticket in tickets:
        res += sum(x for x in ticket if not valid_for_some_constraint(constraints, x))

    return res

def is_valid(constraint, v):
    for low, high in constraint[1]:
        if low <= v and v <= high:
            return True
    return False

def is_valid_assignment(constraint, tickets, i):
    # is the ith field in constraints the jth field in the tickets?
    return all(is_valid(constraint, ticket[i]) for ticket in tickets)


# print("is_valid_assignment")
# constraint = ("", [(1, 2), (4, 5)])
# tickets = [[1, 2], [3, 4], [5, 5]]
# print(is_valid_assignment(constraint, tickets, 0))
# print(is_valid_assignment(constraint, tickets, 1))


def part2(inp):
    constraints, mytick, tickets = inp

    tickets = [
        x for x in tickets
        if all(valid_for_some_constraint(constraints, v) for v in x)]
    # print("constraints:")
    for k, v in constraints:
        print(k, v)
    # print("valid tickets:", tickets)

    N = len(constraints)
    G = {k:[] for k in range(N)}
    # possible_matches = [[] for x in range(N)]

    for i in range(N):
        for j in range(N):
            if is_valid_assignment(constraints[i], tickets, j):
                G[i].append(j)

    # return possible_matches
    res = simple_matches(G)
    idxs = []
    real_res = 1
    for i, (name, _) in enumerate(constraints):
        if name.startswith("departure"):
            idx = res[i]
            real_res *= mytick[idx]

    return real_res



def simple_matches(m):
    # I'm sad we can get away w/ the greedy approach...
    # m = {k:v for k, v in enumerate(m)}
    print("initial m:")
    print("\n".join("{}: {}".format(x, y) for x, y in m.items()))

    res = {}

    while m:
        kk = -1
        for k, vs in m.items():
            if len(vs) == 1:
                kk = k
                break
        if kk == -1:
            print("d'oh!")
            print("res:", res)
            print("remaining: ")
            print("\n".join("{}: {}".format(x, y) for x, y in m.items()))
            exit()
        v = m[kk][0]
        res[kk] = v
        print("{} must map to {}".format(kk, v))
        del m[kk]
        for k, l in m.items():
            if v in l:
                l.remove(v)

    return res












#
tinp = get_input("test.in")
# x, y, z = get_input("test.in")
# print(x)
# print(y)
# print(z)
# print(is_valid_assignment(x[1], z, 0))
# print(is_valid_assignment(x[0], z, 1))
# print(is_valid_assignment(x[2], z, 2))

inp = get_input("day16.in")

print("part1:", part1(inp))
print("part2:", part2(inp))
# p2 = part2(tinp)
# for i, x in enumerate(p2):
#     print("{}: {}".format(i, x))
