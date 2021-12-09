from collections import defaultdict


class Tile:

    def __init__(self, idn, contents):
        self.id = idn
        self.contents = contents
        self.N = len(contents)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def get_data(self):
        return [x[1:-1] for x in self.contents[1:-1]]

    def rotate(self):
        # rotate 90 degrees clockwise
        contents = []
        for i in range(len(self.contents)):
            contents.append(''.join(L[i] for L in self.contents[::-1]))
        self.contents = contents

    def flip(self):
        self.contents = [x[::-1] for x in self.contents]

    def top(self):
        return self.contents[0]

    def right(self):
        return ''.join(x[-1] for x in self.contents)

    def bottom(self):
        return self.contents[-1][::-1]

    def left(self):
        return ''.join(x[0] for x in self.contents)[::-1]

    def sides(self):
        return (self.top(), self.right(), self.bottom(), self.left())

    def __repr__(self):
        return "Tile: {}\n".format(self.id) + '\n'.join(self.contents)

# a = Tile(123, ['##.', '#..', '...'])
a = Tile(123, ['1234', '5678', '1357', '2468'])
print(a.get_data())
# print(a)
# a.flip()
# print(a)
# a.rotate()
# print(a)
# a.rotate()
# print(a)
# a = Tile(123, ['1234', '5678', '1357', '2468'])
# print("Test tile:")
# print(a)
# print("Top:", a.top())
# print("right:", a.right())
# print("bottom:", a.bottom())
# print("left:", a.left())


def get_input(fname):
    tiles = []

    idn = None
    t = []

    with open(fname, 'r') as f:
        for x in f.readlines():
            x = x.strip()
            if x == '':
                tiles.append(Tile(idn, t))
                idn = None
                t = []
            elif "Tile" in x:
                idn = int(x[5:-1])
            else:
                t.append(x)
    if idn:
        tiles.append(Tile(idn, t))

    return tiles


def find_upper_left_corner(tiles):
    for tile in tiles:
        ns = get_possible_neighbors(tile, tiles)
        nc = [len(x) for x in ns]

        zeros = []
        for i in range(4):
            if nc[i] == 0:
                zeros.append(i)
        zeros = tuple(zeros)

        if len(zeros) < 2:
            continue

        if zeros == (0, 1):
            tile.rotate()
            tile.rotate()
            tile.rotate()
        elif zeros == (1, 2):
            tile.rotate()
            tile.rotate()
        elif zeros == (2, 3):
            tile.rotate()
        return tile

    print("FAIL!")
    exit()


def find_tile(seen, tiles, left, top):
    # find a tile matching the left and top patterns!
    # can't be one we've already found!
    for tile in tiles:
        if tile.id in seen:
            continue

        if not (left in tile.sides() or top in tile.sides()):
            tile.flip()

        if not (left in tile.sides() or top in tile.sides()):
            continue

        # left OR top matches!
        if left:
            if left == left[::-1]:
                print("BAD SITUATION!")
                exit()
            while tile.left() != left:
                tile.rotate()
        if top:
            if top == top[::-1]:
                print("BAD SITUATION!")
                exit()
            while tile.top() != top:
                tile.rotate()

        return tile

def get_board(tiles):
    board = []
    for row in tiles:
        blocks = [tile.get_data() for tile in row]
        for i in range(len(blocks[0])):
            board.append(''.join(b[i] for b in blocks))

    return board

# tiles = [[None]*3 for x in range(3)]
#
# for i in range(3):
#     for j in range(3):
#         tiles[i][j] = Tile(1, ['...', '.{}.'.format(3*i+j), '...'])
#
# print("tiles: ", tiles)
# board = get_board(tiles)
#
# bigtile = Tile(123123, board)
# print(bigtile)

mh = 3
mw = 20

moffsets = [
(0, 18), (1, 0), (1, 5), (1, 6), (1, 11), (1, 12), (1, 17), (1, 18), (1, 19),
(2, 1), (2, 4), (2, 7), (2, 10), (2, 13), (2, 16)
]

def is_monster_present(data):
    for i in range(len(data)-mh+1):
        for j in range(len(data[i]) - mw + 1):
            if all(data[i+di][j+dj] == '#' for di, dj in moffsets):
                return True

def non_monster_hashes(data):
    if not is_monster_present(data):
        return 0

    monster = set()

    for i in range(len(data)-mh+1):
        for j in range(len(data[i]) - mw + 1):
            if not all(data[i+di][j+dj] == '#' for di, dj in moffsets):
                continue
            monster |= set([(i+di, j+dj) for di, dj in moffsets])

    res = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '#' and (i, j) not in monster:
                res += 1

    return res



# testinp = [
# '#.###...#.##...#.######.',
# '.###.###.#######..#####.',
# '..##.#..#..#.#######.#',
# ]
#
# print("is present?", is_monster_present(testinp))
                  #
#    ##    ##    ###
 #  #  #  #  #  #


'''
01234567890123456789
....................
                  #
#    ##    ##    ###
 #  #  #  #  #  #

'''


def part2(tiles):
    res = [[None]*12 for i in range(12)]

    res[0][0] = find_upper_left_corner(tiles)

    seen = {res[0][0].id}

    for i in range(12):
        for j in range(12):
            if i == 0 and j == 0:
                continue

            top = None
            left = None
            if i > 0:
                top = res[i-1][j].bottom()[::-1]
            if j > 0:
                left = res[i][j-1].right()[::-1]

            res[i][j] = find_tile(seen, tiles, left, top)
            seen.add(res[i][j].id)


    pic = get_board(res)
    pictile = Tile(123123123, pic)
    # print(pictile)

    for i in range(4):
        for j in range(2):
            r = non_monster_hashes(pictile.contents)
            if r > 0:
                return r
            pictile.flip()

        pictile.rotate()

    print("BOOO")
    exit()






def get_possible_neighbors(tile, tiles):
    res = []
    for a in tile.sides():
        neighbors = []
        for other in tiles:
            if tile == other:
                continue
            for b in other.sides():
                if a == b[::-1] or a == b:
                    neighbors.append(other)
                    break
        res.append(neighbors)
    return res

def print_stats(tiles):

    must_be_corners = []
    must_be_edges = []

    h = defaultdict(lambda: 0)

    for tile in tiles:
        ns = get_possible_neighbors(tile, tiles)
        nc = [len(x) for x in ns]
        for c in nc:
            h[c] += 1
        nc.sort()
        if nc[0] == 0:
            if nc[1] == 0:
                must_be_corners.append(tile)
            else:
                must_be_edges.append(tile)

    print("Corners: ", len(must_be_corners))
    print("Edges: ", len(must_be_edges))
    print("Histogram:")
    ks = [k for k in h.keys()]
    ks.sort()
    for k in ks:
        print("  {}: {}".format(k, h[k]))


    r = 1
    for t in must_be_corners:
        r *= t.id
    print("PART1:", r)


tiles = get_input("day20.in")
# tiles = get_input("test.in")
# n = len(tiles)
# nr = int(n**0.5)

print("part1: ")
# print_stats(tiles)
print("part2:", part2(tiles))

# print("STATISTICS:")
# print("Total tiles: {}".format(n))
# print("Board: {}x{}".format(nr, nr))


# td = {tile.id: tile for tile in tiles}
# t = td[1427]
# print("Considering tile: \n")
# print(t)
# print("neighbors:")
# for direction, ns in zip(("Top", "Right", "Bottom", "Left"), get_possible_neighbors(t, tiles)):
#     print("{} Neighbors:".format(direction))
#     for n in ns:
#         print(n)
#     print()


# for row in tiles[0].contents:
#     print(' '.join(x for x in row))


'''

two pieces fit IF they match backwards lol.

...###
...###
...###

'''
