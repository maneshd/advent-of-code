import re

def get_input(filename):
    with open(filename, 'r') as f:
        return f.read()


pattern1 = "mul\((\d\d?\d?),(\d\d?\d?)\)"
pattern2 = f"({pattern1}|do\(\)|don't\(\))"


def part1(inp):
    matches = re.findall(pattern1, inp)
    return sum(int(a)*int(b) for a, b in matches)


def part2(inp):
    res = 0
    on = True
    for command, a, b in re.findall(pattern2, inp):
        if command == "do()":
            on = True
        elif command == "don't()":
            on = False
        elif on:
            res += int(a)*int(b)
    return res


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))

