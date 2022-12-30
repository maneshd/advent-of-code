
def get_input(fname):
    with open(fname, "r") as f:

        def map_segment(seg):
            return list(map(int, seg.split("-")))

        def map_line(line):
            return list(map(map_segment, line.split(",")))

        return list(map(map_line, f.read().strip().split("\n")))

def contains(A, B):
    a1, a2 = A
    b1, b2 = B
    return a1 <= b1 and b2 <= a2

def overlap(a, b):
    a1, a2 = a
    b1, b2 = b
    return (a1 <= b1 <= a2) or (b1 <= a1 <= b2)

def part1(data):
    return sum(1 for (a, b) in data if (contains(a, b) or contains(b, a)))

def part2(data):
    return sum(1 for (a, b) in data if overlap(a, b))

d = get_input("input.txt")
print("part1: ", part1(d))
print("part2: ", part2(d))

