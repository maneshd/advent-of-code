from collections import defaultdict

def get_input(fname):
    with open(fname, 'r') as f:
        return [[y for y in x.strip()] for x in f.readlines()]

inp = get_input("day11.in")

ndiffs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def part1(G):
    l1, l2 = len(G), len(G[0])

    changed = True

    while changed:
        changed = False
        GG = [[y for y in x] for x in G]

        for i in range(l1):
            for j in range(l2):
                if G[i][j] == '.':
                    continue

                occupied = 0

                for di, dj in ndiffs:
                    ii, jj = i+di, j+dj
                    if ii < 0 or ii >= l1 or jj < 0 or jj >= l2:
                        continue
                    if G[ii][jj] == '#':
                        occupied += 1

                if G[i][j] == 'L' and occupied == 0:
                    GG[i][j] = '#'
                    changed = True
                elif G[i][j] == '#' and occupied >= 4:
                    GG[i][j] = 'L'
                    changed = True

        G = GG

    return sum(len([x for x in row if x == '#']) for row in G)

def get_occupied(G, x, y):
    res = []

    lx, ly = len(G), len(G[0])

    for dx, dy in ndiffs:
        xx, yy = x, y
        while True:
            xx += dx
            yy += dy
            if xx < 0 or yy < 0 or xx >= lx or yy >= ly:
                break
            try:
                if G[xx][yy] == '#':
                    res.append((xx, yy))
                    # res += 1
                    break
                elif G[xx][yy] == 'L':
                    break
            except:
                break
    return res


def prettyprint(G):
    print('\n'.join(''.join(x) for x in G))
    print()

debug = False

def part2(G):
    l1, l2 = len(G), len(G[0])

    changed = True

    if debug:
        print("(1)")
        prettyprint(G)

    cnt = 1

    while changed:
        changed = False
        GG = [[y for y in x] for x in G]

        for i in range(l1):
            for j in range(l2):
                if G[i][j] == '.':
                    continue

                occupied_sqs = get_occupied(G, i, j)
                occupied = len(occupied_sqs)
                if debug and i == 0 and j == 2:
                    print("(0, 2) counts {} occupied".format(occupied))
                    print(occupied_sqs)

                if G[i][j] == 'L' and occupied == 0:
                    GG[i][j] = '#'
                    changed = True
                elif G[i][j] == '#' and occupied >= 5:
                    GG[i][j] = 'L'
                    changed = True

        G = GG
        if debug:
            cnt += 1
            print("({})".format(cnt))
            prettyprint(G)

    return sum(len([x for x in row if x == '#']) for row in G)




# print("part1:", part1(inp))
print("part2:", part2(inp))

# tinp = get_input("test.in")
# print(tinp)
# print("test2:", part2(tinp))
