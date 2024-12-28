from collections import defaultdict
from collections import Counter


def parse_input(fname):
    with open(fname, 'r') as f:
        return f.read().splitlines()


U, D, L, R = (-1, 0), (1, 0), (0, -1), (0, 1)
A = 'A'
pad1 = {
    7:(0,0), 8:(0,1), 9:(0,2),
    4:(1,0), 5:(1,1), 6:(1,2),
    1:(2,0), 2:(2,1), 3:(2,2),
             0:(3,1), A:(3,2),
}
PAD1 = {str(k):v for (k,v) in pad1.items()}
S1 = (3,2)

PAD2 = {
             U:(0,1), A:(0,2),
    L:(1,0), D:(1,1), R:(1,2)
}
S2 = (0,2)


def shortest_path(target, pad, s):
    i1,j1 = s
    res = []
    for v in target:
        i2, j2 = pad[v]
        di, dj = (i2-i1), (j2-j1)
        dis = [(di//abs(di), 0)]*abs(di) if di != 0 else []
        djs = [(0, dj//abs(dj))]*abs(dj) if dj != 0 else []
        if (i1, j1+dj) not in pad.values():
            deltas = dis+djs
        elif (i1+di, j1) not in pad.values():
            deltas = djs+dis
        elif dj < 0:  # (A) If we need to go left, prefer doing it first.
            deltas = djs+dis
        else:  # (B) Otherwise, prefer traveling UP/DOWN first.
            deltas = dis+djs
        res.extend(deltas)
        res.append(A)
        i1,j1 = i2,j2
    return res


bigram_mapping = {}
for ch1 in [U,D,L,R,A]:
    for ch2 in [U,D,L,R,A]:
        bigram = (ch1, ch2)
        sp = shortest_path(bigram, PAD2, PAD2[ch1])
        bigram_mapping[bigram] = [x for x in zip(sp, sp[1:])]


# Of course we can use the part2 approach, too.
def part1(L):
    def score(s):
        sp = shortest_path(s, PAD1, S1)
        sp = shortest_path(sp, PAD2, S2)
        sp = shortest_path(sp, PAD2, S2)
        return len(sp) * int(s[:-1])
    return sum(map(score, L))


def part2(L):
    def score(s):
        sp = shortest_path(s, PAD1, S1)
        sp = [A] + sp
        bigrams = Counter(zip(sp, sp[1:]))
        for _ in range(25):
            new_bigrams = defaultdict(lambda: 0)
            for bigram, count in bigrams.items():
                for t in bigram_mapping[bigram]:
                    new_bigrams[t] += count
            bigrams = new_bigrams
        return sum(bigrams.values()) * int(s[:-1])
    return sum(map(score, L))


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))