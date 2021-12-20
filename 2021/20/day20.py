from collections import defaultdict


def get_input(fname):
    with open(fname, 'r') as f:
        left, right = f.read().strip().split("\n\n")

        mapping = ['1' if x == '#' else '0' for x in left.strip()]

        pixels = defaultdict(lambda: '0')
        for i, row in enumerate(right.split("\n")):
            for j, ch in enumerate(row):
                if ch == "#":
                    pixels[(i, j)] = '1'

        return mapping, pixels


def neighborhood(i, j):
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            yield (i+di, j+dj)


def pixel_to_num(pixels, i, j):
    return int(
            ''.join(map(lambda x: pixels[x], neighborhood(i, j))),
            2)


# The trick here is that the resulting dictionary of pixel values
# only contains the pixels that don't match the 'majority' pixel (i.e.
# the pixels beyond the borders).
def step(pixels, mapping):
    res_default = mapping[int(pixels.default_factory()*9, 2)]
    res = defaultdict(lambda: res_default)

    to_consider = set()
    for i, j in pixels.keys():
        for ij in neighborhood(i, j):
            to_consider.add(ij)

    for (i,j) in to_consider:
        res_pixel = mapping[pixel_to_num(pixels, i, j)]
        if res_pixel != res_default:
            res[(i, j)] = res_pixel

    return res


def solution(inp, steps):
    mapping, pixels = inp

    for i in range(steps):
        pixels = step(pixels, mapping)

    return sum(map(int, pixels.values()))


inp = get_input("input.txt")
#  inp = get_input("test.txt")

print("part1: ", solution(inp, 2))
print("part2: ", solution(inp, 50))

