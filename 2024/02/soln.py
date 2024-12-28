
def get_input(filename):
    with open(filename, 'r') as f:
        parse_line = lambda line: [int(x) for x in line.split()]
        return list(map(parse_line, f.readlines()))

def get_diffs(L):
    return [x-y for x, y in zip(L, L[1:])]

def safe(diffs):
    return (all(x in (1, 2, 3) for x in diffs) or
            all(x in (-1, -2, -3) for x in diffs))

def all_possibilities(L):
    yield L
    for i in range(len(L)):
        yield L[:i] + L[i+1:]

def part1(inp):
    diffs = map(get_diffs, inp)
    safe_floors = filter(safe, diffs)
    return sum(1 for _ in safe_floors)
    

def part2(inp):
    def safe2(floor):
        return any(safe(get_diffs(p)) for p in all_possibilities(floor))
    safe_floors = filter(safe2, inp)
    return sum(1 for _ in safe_floors)


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))

