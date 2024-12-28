def parse_input(fname):
    make_key = lambda b: [6-row.index("#") for row in b]
    make_lock = lambda b: [row.index(".")-1 for row in b]
    with open(fname, 'r') as f:
        blocks = [x.split("\n") for x in f.read().split("\n\n")]
        blocks = [list(zip(*block)) for block in blocks]
        keys = [make_key(b) for b in blocks if b[0][0] == "."]
        locks = [make_lock(b) for b in blocks if b[0][0] == "#"]
        return keys, locks
    

def part1(keys, locks):
    fits = lambda k, l: all(x+y<6 for (x,y) in zip(k,l))
    return sum(1 for k in keys for l in locks if fits(k, l))


if __name__ == "__main__":
    keys, locks = parse_input("inp.txt")
    print("part 1:", part1(keys, locks))