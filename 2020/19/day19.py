from collections import defaultdict

MAX_LEN = 96

'''
possibilities:
 - bidirectional search
 - use a heuristic (e.g. distance from (0,) to something containing the thing)

'''

def get_input(fname):
    rules = {}
    strings = []
    state = "rules"
    with open(fname, 'r') as f:
        for x in f.readlines():
            x = x.strip()
            if x == '':
                state = "strings"
                continue

            if state == "strings":
                strings.append(x)
                continue

            idx, rule = x.split(':')
            r = None
            if '"' in rule:
                r = rule.replace('"', '').strip()
            else:
                r = [tuple(int(a) for a in b.split()) for b in rule.split('|')]
            rules[int(idx)] = r

    return rules, strings


def invert_rules(rules):
    res = defaultdict(lambda: [])
    for k, vs in rules.items():
        for v in vs:
            res[v].append(k)
    return res


# def get_applicable_indices
def get_matching_idxs(u, m):
    # print("get_matching_idxs({}, {})".format(u, m))
    res = []
    for i, j in zip(range(len(u)), range(len(m), len(u)+1)):
        # gs = "did not match"
        if u[i:j] == m:
            res.append((i, j))
            # gs = "matched"
        # print("m[{}:{}] {}".format(i, j, gs))

    # print("get_matching_idxs({}, {}) = {}".format(u, m, res))
    # print()
    return res

def get_neighbors(u, inv_rules):
    res = []

    for k, vs in inv_rules.items():
        for i, j in get_matching_idxs(u, k):
            for v in vs:
                res.append(u[0:i] + (v,) + u[j:])
    return res

# u = (1, 2, 3)
# inv_rules = {
#   (1, 2): [5, 6],
#   (2, 3): [7],
#   (1, 2, 3): [8],
#   (3, 4): [9],
# }
# print("get_neighbors_test:", get_neighbors(u, inv_rules))


''' TODO: graph search'''
def matches_rule(inv_rules, string, target=0):
    s = tuple(inv_rules[x][0] for x in string)
    target = (target,)

    seen = set(s)
    to_process = [s]

    while to_process:
        u = to_process.pop()

        for v in get_neighbors(u, inv_rules):
            if v in seen:
                continue
            if v == target:
                return True
            seen.add(v)
            to_process.append(v)
    return False


'''
TODO: is there something greedy we can do in the search? Like, if we know the
first character has to be 'a', can we do something nice?
'''


'''
BEGIN! THE GOOD STUFF
'''

def forward_neighbors(rules, u):

    res = []
    for i in range(len(u)):
        if type(u[i]) == str:
            continue
        for v in rules[u[i]]:
            res.append(u[:i] + v + u[i+1:])

    return res


def is_plausible(u, target):
    if len(u) > len(target):
        return False

    if all(type(x)==str for x in u) and u != target:
        return False

    if not is_subseq(target, u):
        return False

    for i in range(len(u)):
        if type(u[i]) != str:
            break
        if u[i] != target[i]:
            return False

    for i in range(1, len(u)+1):
        if type(u[-i]) != str:
            break
        if u[-i] != target[-i]:
            return False

    return True

# u = ['a', 'b', 1, 4, 'b', 'a']
#
# ts = [
# 'ababababba',
# 'ababba',
# 'ababab',
# 'ababbb',
# 'abba',
# 'baaaaaba',
# ]
# for t in ts:
#     tt = tuple(x for x in t)
#     print("string {} : {}".format(t, is_plausible(u, tt)))


def is_subseq(t, u):
    # is u a subsequence of t
    j = 0
    for i in range(len(u)):
        if type(u[i]) == str:
            while j < len(t) and t[j] != u[i]:
                j += 1
        if j >= len(t):
            return False
        j += 1
    return True

t = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
us = [
  (3, 'a', 3),
  (3, 'b', 3),
  (3, 'd', 3),
  ('a', 3, 'b', 'g'),
  (3, 'c', 'f', 3),
]


def is_valid(rules, target):
    target = tuple(x for x in target)

    start = (0,)
    to_process = [start]
    seen = set([start])

    print("Looking for target of length={}: '{}'".format(len(target), target))

    while to_process:
        u = to_process.pop()

        for v in forward_neighbors(rules, u):
            if v == target:
                return True
            if v in seen or not is_plausible(v, target):
                continue
            seen.add(v)
            to_process.append(v)
            if len(seen) % 10000 == 0:
                # pass
                print("Round: {}".format(len(seen)))
                print("sample: ", v)


    return False

def part1(inp):
    rules, strings = inp
    rules = simplify_rules(rules)
    super_simplify(rules)
    # print("simplified rules")
    res = 0


    for i, string in enumerate(strings):
        i = 135 + i
        if is_valid(rules, string):
            print("{}: match".format(i))
            res += 1
        else:
            print("{}: no match".format(i))

    return res

def super_simplify(rules):
    s = {}
    for k in rules.keys():
        all_strings = get_all_strings(rules, (k,))
        if all_strings:
            s[k] = all_strings
        else:
            print("not replacing rule {}".format(k))

    for k, v in s.items():
        rules[k] = v
        # print("replacing rule {} w/ {} possibilities".format(k, len(v)))



def get_all_strings(rules, start):
    rules = simplify_rules(rules)
    limit = 1000000
    res = []
    seen = set([start])

    to_process = [start]
    while to_process:
        u = to_process.pop()

        for v in forward_neighbors(rules, u):
            if 8 in v or 11 in v:
                return None
            if v in seen:
                continue
            if all(type(x)==str for x in v):
                seen.add(v)
                res.append(v)
                continue
            seen.add(v)
            to_process.append(v)

            if len(seen) > limit:
                return None

    # print("found all strings! seen things: ", len(seen))
    return res


def simplify_rules(rules):
    res = {k:v for k, v in rules.items()}
    res[26] = [("a",)]
    res[16] = [("b",)]

    while True:
    # for i in range(5):
        a, b = None, None
        for k, vs in res.items():
            if k == 0:
                continue
            if type(vs) == str:
                a, b = k, (vs,)
                break
            elif len(vs) == 1:
                a, b = k, vs[0]
                break
        if not b:
            return res

        # print("replacing {} with {}".format(a, b))

        del(res[a])
        for k, vs in res.items():
            for i in range(len(vs)):
                vl = vs[i]
                if a not in vl:
                    continue
                while a in vl:
                    j = vl.index(a)
                    vl = vl[:j] + b + vl[j+1:]
                # print("rules[{}]: {} -> {}".format(k, vs[i], vl))
                vs[i] = vl
    return res





'''
0 -> 8 11

8 -> {42}+
11 -> {42}^k{31}^k

SO:
better part 2:

keep matching (from left) {42} until you can't. then match {31} until you can't.
If the {42} matches count is > the other, then you win!
'''


inp = get_input("day19.in")
rules = inp[0]
rules[8] = [(42,), (42, 8)]
rules[11] = [(42, 31), (42, 11, 31)]
# print("part2:", part1(inp))
# bbbbbbaa
# 12345678

things42 = get_all_strings(rules, (42,))
things31 = get_all_strings(rules, (31,))
if things42:
    print("things42")
    print(len(things42))
    for x in things42:
        if len(x) != 8:
            print("ACK!")
        # print(''.join(x))
if things31:
    print("things31")
    # print(things31)
    print(len(things31))
    for x in things31:
        if len(x) != 8:
            print("ACK!")
        # print(''.join(x))

strings = inp[1]

A = set(''.join(x) for x in things42)
B = set(''.join(x) for x in things31)

# def is_string_good(A, B, s):
#     if len(s) % 8 != 0 or len(s) < 24:
#         print("1111")
#         return False
#     if s[-8:] not in B:
#         # print("3333")
#         return False
#     s = s[:-8]
#
#     state = "A"
#     matchA, matchB = 0, 1
#     for i in range(0, len(s), 8):
#         sub = s[i:i+8]
#         if state == "A":
#             if sub in A:
#                 matchA += 1
#                 continue
#             elif sub in B:
#                 matchB += 1
#                 state == "B"
#                 continue
#             else:
#                 return False
#         elif state == "B":
#             if sub in B:
#                 matchB += 1
#                 continue
#             else:
#                 return False
#     return matchA > 2 and matchA >= matchB + 1
#
#
#
#
#
#
#
#     if s[:8] not in A or s[8:16] not in A:
#         s1, s2 = s[:8], s[8:16]
#         # print("A is: {}".format(A))
#         # print("string is: '{}'".format(s))
#         # print("s1={}, in A == {}".format(s1, s1 in A))
#         # print("s2={}, in A == {}".format(s2, s2 in A))
#         return False
#     s = s[16:-8]
#     amatch, bmatch = 0, 0
#     state = "A"
#     while s:
#         sub, s = s[:8], s[8:]
#         if state == "A":
#             if sub in A:
#                 amatch += 1
#             elif sub in B:
#                 state = "B"
#                 bmatch += 1
#             else:
#                 return False
#
#         if state == "B":
#             if sub not in B:
#                 return False
#             else:
#                 bmatch += 1
#
#     return amatch >= bmatch

def is_string_good(A, B, s):
    ss = split_string(s)

    if ss[-1] not in B:
        return False

    if ss[0] not in A or ss[1] not in A:
        return False

    ss = ss[2: -1]

    if not ss:
        return True


    inA = [x in A for x in ss]
    inB = [x in B for x in ss]

    if False not in inA:
        return True

    aCount = inA.index(False)
    if not all(inB[aCount:]):
        return False

    bCount = len(inA) - aCount
    return aCount >= bCount








def split_string(s):
    result = []
    for i in range(0, len(s), 8):
        result.append(s[i:i+8])
    return result


res = 0
c = 0
for s in strings:
    # print("STRING:", s)
    # ssplit = split_string(s)
    # for x in ssplit:
        # print("'{}': in A == {}; in B == {}".format(x, x in A, x in B))
    good = is_string_good(A, B, s)
    # print("verdict: {}".format(good))
    if is_string_good(A, B, s):
        res += 1
    # c+= 1
    # if c > 3:
        # exit()
print("part2: ", res)
