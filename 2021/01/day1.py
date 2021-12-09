
def get_input(fname):
    with open(fname, 'r') as f:
        return [int(x.strip()) for x in f.readlines()]

# if __name__ == "__main__"
def part1(L):
    return sum(1 for (x, y) in zip(L, L[1:]) if x < y)

def part2(L):
    return part1(list(x+y+z for (x, y, z) in zip(L, L[1:], L[2:])))


in1 = get_input("day1.in")
print("part 1:", part1(in1))
print("part 2:", part2(in1))
