def parse_input(fname):
    with open(fname, 'r') as f:
        L, R = f.read().split("\n\n")
        return L.split(", "), R.split("\n")


def count_ways(palette, target, memo):
    if target == '':
        return 1
    elif target in memo:
        return memo[target]
    
    res = sum(count_ways(palette, target[len(s):], memo)
              for s in palette if target.startswith(s))
    memo[target] = res
    return res


def part1(palette, targets):
    return sum(min(1, count_ways(palette, t, {})) for t in targets)


def part2(palette, targets):
    return sum(count_ways(palette, t, {}) for t in targets)


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print(f"part 1: {part1(*inp)}")
    print(f"part 2: {part2(*inp)}")