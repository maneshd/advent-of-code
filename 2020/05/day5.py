
def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        return [x.strip() for x in f.readlines()]



def bin_search(L, high):
    # print("input: ", L)
    low = 1
    high += 1
    # print("low=", low, "high=", high)
    for x in L:
        if x == 1:
            low += (high - low + 1)//2
            # print("1: low=", low, "high=", high)
        else:
            high = (high + low-1) // 2
            # print("0: low=", low, "high=", high)
    return low-1



def get_rowcol(x):
    # lol, variables are backwards
    cc, rr = x[:7], x[7:]
    cc = [1 if a == 'B' else 0 for a in cc]
    rr = [1 if a == 'R' else 0 for a in rr]

    c = bin_search(cc, 127)
    r = bin_search(rr, 7)
    return c, r

def get_id(x):
    r, c = get_rowcol(x)
    return 8*r + c


inp = get_input("day5.in")
# print("inp[0] =", inp[0])
# r, c  = get_rowcol(inp[0])
# print("\n\n");
# get_rowcol(inp[1])
# print("col=", c, "row=", r)
# print("id=", get_id(inp[0]))

part1 = max(get_id(x) for x in inp)
print("part1: ", part1)

print("part2:")
ss = set(get_id(x) for x in inp)
for i in range(127*8):
    if i not in ss:
        print(i)
