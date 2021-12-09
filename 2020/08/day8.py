
def parse_line(l):
    code, n = l.strip().split(' ')
    return code, int(n)

def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        return [parse_line(x) for x in f.readlines()]


def get_delta(r):
    code, n = r
    if code == 'nop':
        return 1, 0
    elif code == 'acc':
        return 1, n
    elif code == 'jmp':
        return n, 0
    else:
        print("unknown code:", code)
        exit()


def part1(inp):
    seen = set()

    ptr = 0
    acc = 0

    while ptr not in seen:
        seen.add(ptr)

        dptr, dacc = get_delta(inp[ptr])
        ptr += dptr
        acc += dacc

    return acc

def part2(inp, ptr=0, acc=0, changed=False):
    seen = set()
    ptr0 = ptr
    # print("attempting: ", ptr)


    while ptr not in seen:
        if ptr == len(inp):
            return True, acc

        seen.add(ptr)

        code, n = inp[ptr]
        if not changed and code != 'acc':
            newcode = "nop" if code == "jmp" else "jmp"
            new_inp = inp[:]
            new_inp[ptr] = (newcode, n)
            found, new_acc = part2(new_inp, ptr, acc, True)
            if found:
                return True, new_acc

        seen.add(ptr)
        dptr, dacc = get_delta(inp[ptr])
        ptr += dptr
        acc += dacc
        # print(ptr, acc)

    # print("no dice for: ", ptr0)
    return False, -1




inp = get_input("day8.in")
print("part1:", part1(inp))
print("part2:", part2(inp))
