from collections import Counter
from functools import reduce
from PIL import Image


W, H = 101, 103

def parse_input(file_name):
    def parse_coord(s):
        return tuple(map(int, s[2:].split(',')))
    def parse_line(l):
        return tuple(map(parse_coord, l.split(" ")))

    with open(file_name, 'r') as f:
        return list(map(parse_line, f.read().split("\n")))


def advance(bot):
    (x, y), (dx, dy) = bot
    return ((x+dx)%W, (y+dy)%H), (dx, dy)
    

def part1(bots):
    for _ in range(100):
        bots = map(advance, bots)

    # unique tuple per quadrant, or None
    def get_quadrant(bot):
        (x, y), _ = bot
        midX, midY = (W-1)/2, (H-1)/2
        if midX == x or midY == y:
            return None
        return (x < midX, y < midY)
    
    quadrants = map(get_quadrant, bots)
    quadrants = filter(lambda x: x is not None, quadrants)
    quadrant_counts = Counter(quadrants)
    mul = lambda x, y: x*y
    return reduce(mul, quadrant_counts.values(), 1)


def get_image(bots):
    img = [[' ']*W for _ in range(H)]
    for ((x, y), _) in bots:
        img[y][x] = "#"
    return '\n'.join(''.join(row) for row in img)

def part2(bots):
    # with open("xmas.txt", "w") as f:
    img = Image.new('RGB', (W*100, H*100), "white")
    P = img.load()
    for i in range(10000):
        bots = list(map(advance, bots))
        # Option 1) binary search until you find the answer :)
        lo, hi = 0, 10000
        if i < lo or i > hi:
            continue

        xOffset = (i // 100)*W
        yOffset = (i % 100)*H
        for ((x, y), _) in bots:
            P[x+xOffset,y+yOffset] = (0, 0, 0)
    
    # Option 2) Count tick marks :)
    for i in range(100):
        xOffset = i*W
        h = 80 if (i % 10) == 0 else 20
        for x in range(20):
            for y in range(h):
                P[x+xOffset, y] = (100, 0, 0)
    for i in range(100):
        yOffset = i*H
        w = 80 if (i % 10) == 0 else 20
        for y in range(20):
            for x in range(w):
                P[x, y+yOffset] = (100, 0, 0)

    img.save("xmas.png")


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))
