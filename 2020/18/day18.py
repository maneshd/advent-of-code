from collections import defaultdict

def get_input(fname):
    with open(fname, 'r') as f:
        return [x.strip() for x in f.readlines()]

def line_to_symbols(l):
    res = []
    for c in l:
        if c == ' ':
            continue
        if c in '()+*':
            res.append(c)
        else:
            res.append(int(c))
    return res

def find_closing_paren_index(l, i):
    if l[i] != '(':
        print("baaaaad")
        exit()
    j = i
    pcount = 0
    while j < len(l):
        if l[j] == '(':
            pcount += 1
        elif l[j] == ')':
            pcount -= 1
            if pcount == 0:
                return j
        j += 1
    print("boooo")
    exit()


def symbols_to_nested(l):
    res = []
    i = 0
    while i < len(l):
        c = l[i]
        if c == '(':
            j = find_closing_paren_index(l, i)
            res.append(symbols_to_nested(l[i+1:j]))
            i = j + 1
        elif c == ')':
            print("panic!")
            exit()
        else:
            res.append(c)
            i += 1
    return res

def evaluate_nested(l):
    if type(l) == int:
        return l
    if type(l) == str:
        print("nope!")
        exit()

    res = evaluate_nested(l[0])

    for i in range(1, len(l), 2):
        sign = l[i]
        right = l[i+1]

        rval = evaluate_nested(right)
        if sign == '+':
            res += rval
        elif sign == '*':
            res *= rval
        else:
            print("unexpected sign:", sign)

    return res

def eval2(l):
    if type(l) == int:
        return l
    if type(l) == str:
        return l

    l = [eval2(x) for x in l]

    # 2 * 3 * 4 * 5 + 5 * 4 + 7
    # now l has no parens/no lists!
    # 1 + 2 * 3 + 4 * 5 * 6 + 7
    s = [l[0]]
    for i in range(1, len(l), 2):
        sign, right = l[i], l[i+1]
        if sign == '*':
            s.append(right)
        else:
            left = s.pop()
            s.append(left+right)

    res = 1
    for x in s:
        res *= x
    return res

def part1(input):
    res = 0
    for line in input:
        symbols = line_to_symbols(line)
        nested = symbols_to_nested(symbols)
        value = evaluate_nested(nested)
        res += value
    return res

def part2(input):
    res = 0
    for line in input:
        symbols = line_to_symbols(line)
        nested = symbols_to_nested(symbols)
        value = eval2(nested)
        res += value
    return res

inp = get_input("day18.in")
# print("part1:", part1(inp))
print("part2:", part2(inp))
