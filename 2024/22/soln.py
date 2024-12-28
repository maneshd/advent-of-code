from functools import reduce


def parse_input(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.read().splitlines()]


N = 16777216
def f(n):
    n = ((n*64) ^ n) % N
    n = ((n//32) ^ n) % N
    n = ((n*2048) ^ n) % N
    return n


def part1(L):
    nth_secret = lambda n, t: reduce(lambda n, _: f(n), range(t), n)
    return sum(map(lambda n: nth_secret(n, 2000), L))


M = 2000
def part2(L):
    def seq_to_price(n):
        prices = [n%10]
        for _ in range(M):
            n = f(n)
            prices.append(n%10)
        diffs = [x-y for (x,y) in zip(prices[1:], prices)]

        res = {}  # maps: sequence to price
        for i, seq in enumerate(zip(diffs, diffs[1:], diffs[2:], diffs[3:])):
            if seq not in res:
                res[seq] = prices[i+4]  # TODO: check
        return res 

    D = list(map(seq_to_price, L))
    scores = {}

    # Try every present sequence
    for d in D:
        for seq in d.keys():
            if seq in scores:
                continue
            scores[seq] = sum(map(lambda d: d.get(seq, 0), D))
    return max(scores.values())


if __name__ == "__main__":
    L = parse_input("inp.txt")
    print("part 1:", part1(L))
    print("part 2:", part2(L))