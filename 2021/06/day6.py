
def get_input(fname):
    with open(fname, 'r') as f:
        l1 = f.readlines()
        return [int(x) for x in l1[0].split(',')]

def fishcount(inp, days):
    state = [0]*9
    for x in inp:
        state[x] += 1

    def advance(s):
        res = s[1:] + [s[0]]
        res[6] += s[0]
        return res

    # print("initial state: ", state)
    # print(len(state))

    for i in range(days):
        state = advance(state)
        # print(i, ":", state)
    return sum(state)

    # [ 32, 54, 765, 31]









# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", fishcount(inp, 80))
print("part 2:", fishcount(inp, 256))
