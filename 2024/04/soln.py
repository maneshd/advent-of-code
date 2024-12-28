def get_input(filename):
    with open(filename, 'r') as f:
        return f.read().split("\n")


def get_letter(M, x, y):
    if (x < 0 or y < 0 or x >= len(M) or y >= len(M[0])):
        return "."
    return M[x][y]


def word_coords1(x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (dx, dy) == (0, 0):
                continue
            yield ((x+dx*i, y+dy*i) for i in range(4))

def word_coords2(x, y):
    yield ((x, y), (x+1, y+1), (x+2, y+2))
    yield ((x+2, y), (x+1, y+1), (x, y+2))


def word_from_coords(M, coords):
    return ''.join(get_letter(M, x, y) for x, y in coords)


def words_at_pos(M, x, y, get_word_coords_fn):
    return [word_from_coords(M, p) for p in get_word_coords_fn(x, y)]
        

def part1(M):
    positions = [(i, j) for i in range(len(M)) for j in range(len(M[0]))]
    words_per_pos = (words_at_pos(M,i,j,word_coords1) for (i, j) in positions)
    count_xmas = lambda words: sum(1 for w in words if w == "XMAS")
    return sum(map(count_xmas, words_per_pos))


def part2(M):
    positions = [(i, j) for i in range(len(M)) for j in range(len(M[0]))]
    words_per_pos = (words_at_pos(M,i,j,word_coords2) for (i,j) in positions)
    mas_crossing = lambda words: all(w in ("MAS", "SAM") for w in words)
    return sum(1 for words in words_per_pos if mas_crossing(words))


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))

