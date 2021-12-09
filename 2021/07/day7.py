
def get_input(fname):
    with open(fname, 'r') as f:
        l1 = f.readlines()
        return [int(x) for x in l1[0].split(',')]

def part1(inp):

    cdict = {}
    for x in inp:
        cdict[x] = cdict.get(x, 0) + 1
    crabs = list(sorted(cdict.items()))

    L = {} # L[x] cost of getting all crabs to pos >= x
    R = {}

    pos, count = crabs[0]
    fuel = 0
    L[pos] = fuel

    for (next_pos, next_count) in crabs[1:]:
        fuel += (next_pos-pos) * count
        count += next_count
        pos = next_pos
        L[pos] = fuel

    # now go from the right

    pos, count = crabs[-1]
    fuel = 0
    R[pos] = fuel
    for (next_pos, next_count) in reversed(crabs[:-1]):
        fuel += (pos - next_pos) * count
        count += next_count
        pos = next_pos
        R[pos] = fuel


    # print(crabs)
    # print(list(sorted(L.items())))
    # print(list(sorted(R.items())))

    fuel, pos = min((L[k]+R[k], k) for k in L.keys())

    return fuel

    # Greedy approach - does not work!
    #
    #
    #
    #
    #
    # ccrabs = 0
    # prev_pos = 0
    #
    # for (pos, count) in crabs:
    #     if len(L) == 0:
    #         L[pos] =
    #     L[pos] =
    #
    #
    # res = 0
    #
    #
    #
    # def get_cost(c1, c2, isRight=False):
    #     pos1, count1 = c1
    #     pos2, count2 = c2
    #     return (pos2-pos1) * (count2 if isRight else count1)
    #
    # while len(crabs) > 1:
    #     left_cost = get_cost(crabs[0], crabs[1])
    #     right_cost = get_cost(crabs[-2], crabs[-1], True)
    #     print("left cost of {} and {} -> {}".format(crabs[0], crabs[1], left_cost))
    #     print("right cost of {} and {} -> {}".format(crabs[-2], crabs[-1], right_cost))
    #
    #
    #     if left_cost < right_cost:
    #         res += left_cost
    #         n = crabs[0][1]
    #         crabs = crabs[1:]
    #         c0 = crabs[0]
    #         crabs[0] = (c0[0], c0[1]+n)
    #     else:
    #         res += right_cost
    #         n = crabs[-1][1]
    #         crabs = crabs[:-1]
    #         clast = crabs[-1]
    #         crabs[-1] = (clast[0], clast[1]+n)
    #
    #     print("crabs: ", crabs)
    #     print("fuel used: ", res)
    #     print()
    #
    # return res

def part2(inp):
    lo, hi = min(inp), max(inp)

    crabs = {}
    for x in inp:
        crabs[x] = crabs.get(x, 0) + 1

    L = {}
    R = {}

    snowball = [(crabs[lo], 1)]  # list of (count, next_step_fuel)
    fuel = 0
    L[lo] = fuel

    for i in range(lo+1, hi+1):
        # how much fuel to move snowball from i-1 to i?
        for count, f in snowball:
            fuel += count*f

        snowball = [(count, f+1) for (count, f) in snowball]

        if i in crabs:
            snowball.append((crabs[i], 1))

        L[i] = fuel


    snowball = [(crabs[hi], 1)]
    fuel = 0
    R[hi] = fuel

    for i in range(hi-1, lo-1, -1):
        for count, f in snowball:
            fuel += count*f

        snowball = [(count, f+1) for (count, f) in snowball]

        if i in crabs:
            snowball.append((crabs[i], 1))

        R[i] = fuel


    fuel, pos = min((L[k]+R[k], k) for k in L.keys())

    return fuel











# inp = get_input("test.txt")
inp = get_input("input.txt")
# inp = [16,1,2,0,4,2,7,1,2,14]
print("part 1:", part1(inp))
print("part 2:", part2(inp))
