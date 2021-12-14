from collections import defaultdict

def get_input(fname):
    with open(fname, 'r') as f:
        start = f.readline().strip()
        f.readline()

        rules = [tuple(x.strip().split(" -> ")) for x in f]
        rules = {a:b for (a, b) in rules}
        return start, rules

# Slower version, for part 1
def step(s, rules):
    res = [a + rules.get(a+b, '') for (a, b) in zip(s, s[1:])]
    res.append(s[-1])
    return ''.join(res)


def part1(inp):
    s, rules = inp
    for i in range(10):
        s = step(s, rules)

    counts = defaultdict(lambda: 0)
    for ch in s:
        counts[ch] += 1

    return max(counts.values()) - min(counts.values())

# Fast version. S is a dict mapping letter pairs to their frequencies.
def step2(S, rules):
    res = defaultdict(lambda: 0)
    for (pair, n) in S.items():
        if pair not in rules:
            res[pair] = n
            continue
        a, c = pair
        b = rules[pair]
        res[a+b] += n
        res[b+c] += n
    return res

def part2(G):
    s, rules = inp

    # Get the frequency of each pair
    S = defaultdict(lambda: 0)
    for (a, b) in zip(s, s[1:]):
        S[a+b] += 1

    for i in range(40):
        S = step2(S, rules)

    # 'counts' will double-count everything except for the first and last
    # characters of `s`, so we manually double-count them :)
    counts = defaultdict(lambda: 0)
    counts[s[0]] = 1
    counts[s[-1]] = 1
    for ((x, y), n) in S.items():
        counts[x] += n
        counts[y] += n

    return max(counts.values())//2 - min(counts.values())//2

# inp = get_input("test.txt")
inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
