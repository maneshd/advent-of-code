from collections import Counter

def get_input(fname):
    with open(fname, 'r') as f:
        res = set()
        for r, line in enumerate(f.readlines()):
            for c, ch in enumerate(line.strip()):
                if ch == "#":
                    res.add((r, c))
        return res


# direction should be a unit-step in NSWE
def spots_to_check(pos, direction):
    r, c = pos
    dr, dc = direction
    if dr == 0:
        return ((r, c+dc), (r-1, c+dc), (r+1, c+dc))
    elif dc == 0:
        return ((r+dr, c), (r+dr, c-1), (r+dr, c+1))

    print("Shouldn't get here!")
    exit()


def surrounding_spots(pos):
    x, y = pos
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx, dy) != (0, 0):
                yield (x+dx, y+dy)


def run_round(elves, dirs):
    elves_w_proposals = []

    for elf in elves:
        if not any(pos in elves for pos in surrounding_spots(elf)):
            # No one is around
            elves_w_proposals.append((elf, elf))
            continue

        proposal = elf

        for direction in dirs:

            if any(spot in elves for spot in spots_to_check(elf, direction)):
                continue
            # okay, we found a good direction
            proposal = (elf[0]+direction[0], elf[1]+direction[1])
            break

        elves_w_proposals.append((elf, proposal))

    res = set()
    proposals = Counter(map(lambda x: x[1], elves_w_proposals))
    for elf, proposal in elves_w_proposals:
        if proposals[proposal] > 1:
            res.add(elf)
        else:
            res.add(proposal)

    return res

def get_bounding_box(positions):
    xs, ys = zip(*positions)
    return (min(xs), min(ys)), (max(xs), max(ys))


def part1(inp):
    positions = inp
    # NSWE
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    for _ in range(10):
        positions = run_round(positions, directions)
        directions = directions[1:] + directions[:1]

    (x1, y1), (x2, y2) = get_bounding_box(positions)
    return (x2-x1+1)*(y2-y1+1) - len(positions)


def part2(inp):
    positions = inp
    # NSWE
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    for i in range(1, 100000):
        new_positions = run_round(positions, directions)
        if positions == new_positions:
            return i

        directions = directions[1:] + directions[:1]
        positions = new_positions

    print("too much...")

inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))

