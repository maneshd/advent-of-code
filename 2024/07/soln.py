
def get_input(file_name):
    with open(file_name, "r") as f:
        def parse_line(line):
            target, rest = line.split(": ")
            target = int(target)
            nums = tuple(int(x) for x in rest.split(" "))
            return target, nums
        return [parse_line(l) for l in f.read().split("\n")]


def concat(a, b):
    return int(str(a)+str(b))


def count_ways(target, nums):
    if len(nums) == 2:
        a, b = nums
        return (1 if a+b == target else 0) + (1 if a*b == target else 0)

    res = 0
    res += count_ways(target - nums[-1], nums[:-1])
    if target % nums[-1] == 0:
        res += count_ways(target // nums[-1], nums[:-1])

    return res

def count_ways2(target, nums):
    if target < 0:
        return 0
    res = 0
    if len(nums) == 2:
        a, b = nums
        res += (1 if a+b == target else 0)
        res += (1 if a*b == target else 0)
        res += (1 if concat(a, b) == target else 0)
        return res

    res = 0
    rest, last = nums[:-1], nums[-1]

    res += count_ways2(target - last, rest)
    if target % last == 0:
        res += count_ways2(target // last, rest)
    if str(target).endswith(str(last)):
        if len(str(target)) == len(str(last)):
            res += count_ways2(0, rest)
        else:
            new_target = str(target)[:-len(str(last))]
            res += count_ways2(int(new_target), rest)

    return res


def part1(inp):
    return sum(target for (target, nums) in inp if count_ways(target, nums) > 0)


def part2(inp):
    return sum(target for (target, nums) in inp if count_ways2(target, nums) > 0)


if __name__ == "__main__":
    inp = get_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))
