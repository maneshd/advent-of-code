from collections import deque

def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


def _get_input(f):
    return f.read().strip()

ROCKS = [
    ((2, 3), (3, 3), (4, 3), (5, 3)),
    ((3, 3), (3, 4), (3, 5), (2, 4), (4, 4)),
    ((2, 3), (3, 3), (4, 3), (4, 4), (4, 5)),
    ((2, 3), (2, 4), (2, 5), (2, 6)),
    ((2, 3), (2, 4), (3, 3), (3, 4)),
]

def inf_rocks():
    while True:
        for rock_num, rock in enumerate(ROCKS):
            yield (rock, rock_num)

def directions(dirs):
    while True:
        for dr_num, dr in enumerate(dirs):
            res = 1 if dr == ">" else -1
            yield res, dr_num


def print_tower(filled):
    maxy = max( y for x, y in filled)
    for y in range(maxy, -1, -1):
        print("".join('#' if (x, y) in filled else '.' for x in range(7)))

def part1(inp):
    filled = set()
    max_y = -1

    seen = {}

    wind = directions(inp)

    for ((rock, rock_num), i) in zip(inf_rocks(), range(1090)):
    #  for ((rock, rock_num), i) in zip(inf_rocks(), range(2022)):
        rock = tuple((x, y+max_y+1) for x, y in rock)

        while True:
            #  print("rock is: ", list(rock))
            dx, wind_num = next(wind)
            r2 = tuple((x+dx, y) for (x, y) in rock)
            xs = (x for x, y in r2)
            if all(x >= 0 and x < 7 and (x, y) not in filled for (x, y) in r2):
                rock = r2

            dy = -1
            r2 = tuple((x, y+dy) for x, y in rock)
            if any((x, y) in filled or y < 0 for (x, y) in r2):
                for r in rock:
                    filled.add(r)
                    max_y = max(max_y, r[1])
                filled, canonical, did_prune = maybe_prune(filled, rock)
                if did_prune:
                    key = (rock_num, wind_num, canonical)
                    if key in seen:
                        print("!!!")
                        print("Iteration matches: ", seen[key], i+1)
                        #  return
                    else:
                        seen[key] = i+1
                break
            else:
                rock = r2

    return max_y + 1

def find_height(inp, iters):
    filled = set()
    max_y = -1

    wind = directions(inp)

    for ((rock, rock_num), i) in zip(inf_rocks(), range(iters)):
        rock = tuple((x, y+max_y+1) for x, y in rock)

        while True:
            #  print("rock is: ", list(rock))
            dx, wind_num = next(wind)
            r2 = tuple((x+dx, y) for (x, y) in rock)
            xs = (x for x, y in r2)
            if all(x >= 0 and x < 7 and (x, y) not in filled for (x, y) in r2):
                rock = r2

            dy = -1
            r2 = tuple((x, y+dy) for x, y in rock)
            if any((x, y) in filled or y < 0 for (x, y) in r2):
                for r in rock:
                    filled.add(r)
                    max_y = max(max_y, r[1])
                break
            else:
                rock = r2

    return max_y + 1


def maybe_prune(filled, new_rock):
    ys = list(set(p[1] for p in new_rock))
    ys.sort()
    ys.reverse()

    for y in ys:
        if all((x, y) in filled for x in range(7)):
            pruned = set((xx, yy) for (xx, yy) in filled if yy >= y)
            canonical = tuple(sorted((xx, yy-y) for (xx, yy) in pruned))
            return pruned, canonical, True
    return filled, None, False

def part2(inp):
    target = 1000000000000
    adjusted = target - 247
    mod = adjusted % 1710
    div = adjusted // 1710

    A = 247 + mod
    B = 247 + mod + 1710
    dh = find_height(inp, B) - find_height(inp, A)

    # dh = height / 1710   and div = how much to go / 1710 = # of 1710s 
    
    return find_height(inp, A) + dh * div


inp = get_input("input.txt")
#  inp = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
print("part 1:", part1(inp))
print("part 2:", part2(inp))

