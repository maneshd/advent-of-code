
def get_input(fname):
    with open(fname, 'r') as f:
        res = []
        for s in f.readlines():
            L, R = s.strip().split(" | ")
            # L = L.split(" ")
            # L = [''.join(sorted(x)) for x in L]

            L = [''.join(sorted(x)) for x in L.split(" ")]
            R = [''.join(sorted(x)) for x in R.split(" ")]
            res.append((L, R))
        return res

def part1(inp):
    res = 0
    for (_, R) in inp:
        res += sum(1 for x in R if len(x) in (2, 3, 4, 7))
    return res

NUMS = {
  'cf': 1,     # length
  'acf': 7,    # length
  'bcdf': 4,   # length
  'acdeg': 2,
  'acdfg': 3,  # length==5 and shares digits w/ one
  'abdfg': 5,
  'abdefg': 6,  # missing 'c'
  'abcdfg': 9,  # missing 'e'
  'abcefg': 0,  # missing 'd'
  'abcdefg': 8
}

REV_NUMS = {y:x for (x, y) in NUMS.items()}

LENGTH_TO_NUM = {2:1, 3:7, 4: 4, 7:8}

# WARNING:
def get_mapping(nums):
    # print("running get_mapping on: ", nums)
    M = {x:'abcdefg' for x in 'abcdefg'}

    nums_by_length = {x:[] for x in set(len(n) for n in NUMS.keys())}
    for n in nums:
        nums_by_length[len(n)].append(n)

    # print("intermediate: ", nums_by_length)

    for n in nums:
        if len(n) not in (2, 3, 4, 7):
            continue
        num_found = LENGTH_TO_NUM[len(n)]
        s = REV_NUMS[num_found]
        # print("So", n, "must be in", s)
        for digit in n:
            orig = M[digit]
            M[digit] = [x for x in M[digit] if x in s]

    def digit_must_be(ldigs, rdigs):
        for dig in ldigs:
            M[dig] = [d for d in M[dig] if d in rdigs]

        if len(ldigs) != len(rdigs):
            return

        for l, r in M.items():
            if l in ldigs:
                continue
            for dig in rdigs:
                if dig in r:
                    r.remove(dig)

    #
    #
    # def remove_from_others(letter):
    #     for _, b in M.items():
    #         if letter in b and len(b) > 1:
    #             b.remove(letter)


    # let's just apply some rules lol.
    # we can get 'a' by comparing the 1 and 7
    seven = nums_by_length[3][0]
    one = nums_by_length[2][0]
    one_digit = [dig for dig in seven if dig not in one][0]
    digit_must_be(one_digit, 'a')
    # M[one_digit] = 'a'
    # remove_from_others('a')

    # look at what 1 and 4 have in common
    four = nums_by_length[4][0]
    bd = [dig for dig in four if dig not in one]
    digit_must_be(bd, 'bd')


    # let's find the three lol
    three = [x for x in nums_by_length[5] if all(y in x for y in one)][0]
    digit_must_be(three, 'acdfg')
    b = [x for x in four if x not in three][0]
    digit_must_be(b, 'b')


    s1, s2, s3 = (set(x) for x in nums_by_length[6])
    fgab = s1 & s2 & s3
    digit_must_be(fgab, 'fgab')

    # lol, one more pass...
    itms = M.items()
    for digit, possibilities in itms:
        if len(possibilities) == 1:
            digit_must_be(digit, possibilities[0])

    return {k:v[0] for k, v in M.items()}


def decode(code, M):
    decoded = ''.join(M[dig] for dig in code)
    decoded = ''.join(sorted(decoded))
    return str(NUMS[decoded])


def part2(inp):
    res = 0

    for L, R in inp:
        m = get_mapping(L)
        res += int(''.join(decode(x, m) for x in R))

    return res


# inp = get_input("test.txt")
inp = get_input("input.txt")
# inp = [16,1,2,0,4,2,7,1,2,14]
print("part 1:", part1(inp))
print("part 2:", part2(inp))
