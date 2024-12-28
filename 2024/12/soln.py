def parse_input(file_name):
    with open(file_name, 'r') as f:
        return f.read().split("\n")


def in_bounds(M, i, j):
    return 0 <= i and 0 <= j and i < len(M) and j < len(M[0])


def get_region(M, i, j):
    ch = M[i][j]
    region = {(i, j)}

    to_process = [(i, j)]
    while to_process:
        i, j = to_process.pop()
        for i, j in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
            if not in_bounds(M, i, j):
                continue
            if M[i][j] != ch:
                continue
            if (i, j) in region:
                continue
            region.add((i, j))
            to_process.append((i, j))
    return region


def perimeter(region):
    r = 0
    for i, j in region:
        for (a, b) in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
            if (a, b) not in region:
                r += 1
    return r


def area(region):
    return len(region)


def num_sides(region):
    v, h = [], []  # Vertical/horizontal segments (top/left coords)
    for i, j in region:
        if (i-1, j) not in region:
            h.append((i, j))
        if (i+1, j) not in region:
            h.append((i+1, j))
        if (i, j-1) not in region:
            v.append((i, j))
        if (i, j+1) not in region:
            v.append((i, j+1))

    h.sort()
    v.sort(key=lambda k: (k[1], k[0]))
    sides = 0

    # Count horizontal sides
    prev = None
    for (a, b) in h:
        is_diag = lambda a, b: (a, b) in v or (a-1, b) in v
        if prev != (a, b-1) or is_diag(a, b):
            sides += 1
        prev = (a, b)

    # Count vertical sides
    prev = None
    for (a, b) in v:
        is_diag = lambda a, b: (a, b) in h or (a, b-1) in h
        if prev != (a-1, b) or is_diag(a, b):
            sides += 1
        prev = (a, b)
    return sides


def get_regions(M):
    regions = []
    known = set()
    for i in range(len(M)):
        for j in range(len(M[0])):
            if (i, j) in known:
                continue
            region = get_region(M, i, j)
            known = known.union(region)
            regions.append(region)
    return regions


def part1(M):
    return sum(perimeter(r)*area(r) for r in get_regions(M))


def part2(M):
    return sum(num_sides(r)*area(r) for r in get_regions(M))
    

if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))