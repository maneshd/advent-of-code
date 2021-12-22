def part1(inp):

    def deterministic_die():
        while True:
            for i in range(1, 101):
                yield i

    def turns():
        die = deterministic_die()
        while True:
            yield next(die)+next(die)+next(die)

    scores = [0, 0]
    positions = inp

    for (turn, roll) in enumerate(turns()):
        idx = turn % 2

        positions[idx] = ((positions[idx]-1)+roll)%10 + 1
        scores[idx] += positions[idx]

        if scores[idx] >= 1000:
            return scores[(idx+1)%2] * (turn+1)*3


def part2(inp):
    roll_freqs = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

    def advance(state, roll):
        pos1, pos2, score1, score2, turn = state
        pos = [pos1, pos2]
        scores = [score1, score2]

        pos[turn] = ((pos[turn]-1)+roll)%10 + 1
        scores[turn] += pos[turn]

        return (pos[0], pos[1], scores[0], scores[1], (turn+1)%2)

    def count_possibilities(s, memo={}):
        if s in memo:
            return memo[s]
        pos1, pos2, score1, score2, turn = s

        if score1 >= 21:
            return (1, 0)
        elif score2 >= 21:
            return (0, 1)

        res = [0, 0]
        for roll, freq in roll_freqs.items():
            s_next = advance(s, roll)
            a, b = count_possibilities(s_next)
            res[0] += freq*a
            res[1] += freq*b

        memo[s] = res
        return res

    return max(count_possibilities((inp[0], inp[1], 0, 0, 0)))

inp = [3, 10]
#  inp = [4,8]  # test data

print("part1: ", part1(inp))
print("part2: ", part2(inp))

