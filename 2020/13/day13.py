from collections import defaultdict

def get_input(fname):
    with open(fname, 'r') as f:
        ls = f.readlines()
        t = int(ls[0])
        bt = [(int(x) if x != 'x' else -1) for x in ls[1].strip().split(',')]
        return t, bt

inp = get_input("day13.in")

def part1(t, ts):
    t0 = t
    bus_times = [x for x in ts if x != -1]
    while True:
        for tt in bus_times:
            if t % tt == 0:
                return (t-t0) * tt
        t += 1
        if t >= t0*t0:
            print("too much!")


primes = set([2, 3, 5])
for i in range(6, 1000):
    if all(i % p != 0 for p in primes):
        primes.add(i)

def decomp(x):
    res = {}
    for p in primes:
        while x > 1 and x % p == 0:
            x //= p
            if p not in res:
                res[p] = 0
            res[p] += 1
    return res


class StepCalculator:
    def __init__(self):
        self.c = {}

    def add(self, x):
        d = decomp(x)
        for k, v in d.items():
            if k not in self.c:
                self.c[k] = 0
            self.c[k] = max(self.c[k], v)

    def get_step(self):
        res = 1
        for k, v in self.c.items():
            res *= k*v
        return res



def part2(_, ts):
    targets = []
    for (i, t) in enumerate(ts):
        if t != -1:
            targets.append((i, t))

    start = 100000000000000
    # t = start + (start % targets[0][1])
    stepper = StepCalculator()

    for i, target in targets:
        # we know for all targets in good, t is a good time.
        # want to find the next good time.
        # Advancing by step should also produce a good time.
        while (t + i) % target != 0:
            t += stepper.get_step()

        stepper.add(target)

    return t




print("part1:", part1(*inp))
print("part2:", part2(*inp))
