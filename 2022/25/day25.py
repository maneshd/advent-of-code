def get_input(fname):
    with open(fname, 'r') as f:
        return [line.strip() for line in f.readlines()]

VALUE = { "1": 1, "2": 2, "0": 0, "-": -1, "=": -2, }

DIGIT_TO_SNAFU = { v: k for (k, v) in VALUE.items() }

def to_decimal(numstr):
    return sum(
            VALUE[digit] * 5**i
            for (i, digit) in enumerate(reversed(numstr))
            )

# Max snafu number w/ specified # of digits, in decimal :)
def mx_snafu(digits):
    return sum(map(lambda i: 2*5**i, range(digits)))

def mn_snafu(digits):
    return sum(map(lambda i: -2*5**i, range(digits)))


def to_snafu(n):
    if n in DIGIT_TO_SNAFU:
        return DIGIT_TO_SNAFU[n]

    first_digit = None
    num_digits = 0

    if n > 0:
        while mx_snafu(num_digits) < n:
            num_digits += 1
        i = num_digits - 1
        # get the first digit! It's either 1 or 2.
        # It's 2 if n > 12222...
        first_digit = ('2' if 5**i + mx_snafu(i) < n else '1')
    else:
        # n < 0
        while mn_snafu(num_digits) > n:
            # we need more digits
            num_digits += 1
        i = num_digits - 1
        # It's = if -=======.... is not small enough.
        first_digit = ('=' if -1 * 5**i + mn_snafu(i) > n else '-')

    n_remaining = n - VALUE[first_digit]*5**(num_digits-1)
    remaining_digits = to_snafu(n_remaining)
    return first_digit + "0"*(num_digits - 1 - len(remaining_digits)) + remaining_digits


def part1(inp):
    res = sum(map(to_decimal, inp))
    return to_snafu(res)

inp = get_input("input.txt")
print("part 1:", part1(inp))

