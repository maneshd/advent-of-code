'''
Wooof.

This one is pretty slow. It's a guided search w/ some adequate pruning heuristics.
'''
from collections import deque


RESOURCES = ('ore', 'clay', 'obsidian', 'geode')
TIME = 24


def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


def _get_input(f):
    def get_rule(sentence):
        res = [0, 0, 0, 0]
        _, r = sentence.split("costs ")

        costs = []
        for cost_part in r.split(" and "):
            cost_part = cost_part.strip()
            cost, cost_type = cost_part.split(" ")
            #  print(f'cost type: "{cost_type}"')
            res[RESOURCES.index(cost_type)] = int(cost)
        return tuple(res)

    def map_line(line):
        l, r = line.split(": ")
        idx = int(l[10:])

        r = r.strip()[:-1]  # chop off the last period lol
        return (idx, tuple(map(get_rule, r.split(". "))))

    return list(map(map_line, f.readlines()))

'''
Some heuristics for getting neighbor states.
'''
# Returns True if you have the resources to just buy geode robots till the end.
def must_create_geode(state, blueprint):
    (t, resources, _) = state
    cost = blueprint[3]

    time_left = TIME - t - 1
    if time_left < 1:
        return False

    cost = tuple(x*time_left for x in cost)
    if all(x < y for (x, y) in zip(cost, resources)):
        return True


# If we can't even use more of a resource, don't bother building the robot.
def should_create_robot(idx, state, blueprint):
    if idx == 3:
        return True

    (t, resources, _) = state
    time_left = TIME - t - 1

    max_cost = max(cost[idx] for cost in blueprint)
    return resources[idx] < max_cost * time_left


def add(t1, t2):
    return tuple(x+y for (x, y) in zip(t1, t2))

def sub(t1, t2):
    return tuple(x-y for (x, y) in zip(t1, t2))


def neighbors(state, blueprint):
    (t, resources, robots) = state
    if t >= TIME:
        return
    if t == TIME - 1:
        # not worth building a robot
        yield (t+1, tuple(x+y for (x, y) in zip(resources, robots)), robots)
        return

    if must_create_geode(state, blueprint):
        # We gotta buy geodes till the end.
        cost = blueprint[3]
        time_left = TIME - t - 1

        # We only really care about the geodes at this point, so let's not update
        # the other resources lol. YOLO.
        yield (TIME, add(resources, (0, 0, 0, sum(range(time_left+1)))), robots)
        return

    # Try making each thang
    for (idx, cost) in enumerate(blueprint):
        if not should_create_robot(idx, state, blueprint):
            continue
        r = tuple(resources)

        for tt in range(t, TIME-1):
            # can we build at time tt?
            if all(x >= 0 for x in sub(r, cost)):
                if idx != 3:
                    # Build AND collect resources in time tt
                    new_robots = list(robots)
                    new_robots[idx] += 1
                    yield (tt+1, sub(add(r, robots), cost), tuple(new_robots))
                else:
                    # Let's be nasty! Add the full value of getting the geode robot, but don't update the robot count.
                    rr = add(r, robots)
                    rr = sub(rr, cost)
                    rr = add(rr, (0, 0, 0, TIME - tt - 1))
                    yield (tt+1, rr, robots)
                break

            # Collect resources from time tt and move on until we can build our robot
            r = add(r, robots)

    # Now, consider not buying anything ever :)
    # Not technically necessary if we don't count the geode bots, but w/e
    r = tuple(resources)
    for tt in range(t, TIME):
        r = add(r, robots)
    yield (TIME, r, robots)


# For part 1 :)
def run_search(blueprint):
    s = (0, (0, 0, 0, 0), (1, 0, 0, 0))
    seen = set([s])
    to_process = deque([s])

    best = 0

    while to_process:
        u = to_process.popleft()

        for v in neighbors(u, blueprint):
            #  print("neighbor: ", v)
            if v in seen:
                continue
            best = max(best, v[1][3])
            to_process.append(v)
            seen.add(v)

    return best


# A bunch for part 2!

# Keep a specialized dictionary 'seen' of seen elements.
# TL;DR: adds it to the set and returns False if it's strictly inferior.
# Not perfect,  but not false negatives.
# seen: (robots) => time => resources
def update_seen(seen, state):
    t1, r1, b1 = state
    if b1 not in seen:
        seen[b1] = {t1: [r1]}
        return True

    # need to iter more
    for t in range(0, t1+1):
        if t not in seen[b1]:
            continue

        for r2 in seen[b1][t]:
            if all(x <= y for (x, y) in zip(r1, r2)):
                return False

    if t1 not in seen[b1]:
        seen[b1][t1] = [r1]
    else:
        seen[b1][t1].append(r1)

    return True


# Discard if we definitely cannot make up the deficit of geodes
def is_def_inferior(best, state):
    t, resources, robots = state

    geodes = resources[3]
    bots = robots[3]

    for _ in range(t, TIME):
        geodes += bots
        bots += 1

    return geodes <= best

# Why not roll our own specialized priority queue
# Prioritize based on higher geodes, then lower times.
class PQ:
    def __init__(self, size):
        # We have 'size' buckets for possible values # of geodes.
        # For each bucket, we have an array of size TIME+1 for each possible time.
        # Then, finally, we have an array of the items.
        # So: items[geodes][time] = [item1, item2, ...]
        self.items = [
                [[] for y in range(TIME+1)]
                for x in range(size+1)]

    def put(self, state):
        t, resources, _ = state
        geodes = min(resources[3], len(self.items)-1)
        self.items[geodes][t].append(state)

    def get(self):
        for L1 in self.items:
            for L2 in L1:
                if len(L2) == 0:
                    continue
                return L2.pop()

    def size(self):
        return sum(sum(len(x) for x in bucket) for bucket in self.items)

    def empty(self):
        return self.size() == 0

    def print(self):
        print("PQ Contents: ")
        print(" ".join(str(sum(len(x) for x in bucket)) for bucket in self.items))


def run_search2(blueprint):
    s = (0, (0, 0, 0, 0), (1, 0, 0, 0))
    to_process = PQ(30)
    to_process.put(s)

    seen = {}
    update_seen(seen, s)

    best = 0

    # Progress counters :)
    count = 0
    thrown = 0
    thrown2 = 0
    thrown3 = 0

    while not to_process.empty():
        u = to_process.get()
        count += 1
        if count % 20000 == 0:
            print(f'iter {count}:')
            print(f'  remaning: {to_process.size()}')
            print(f'  discarded: {thrown}+{thrown2}+{thrown3}={thrown+thrown2+thrown3}')
            print(f'  best: {best}')
            to_process.print()
            print("processing: ", u)
            print()

        if is_def_inferior(best, u):
            thrown3 += 1
            continue

        for v in neighbors(u, blueprint):
            if is_def_inferior(best, v):
                thrown2 += 1
                continue
            if not update_seen(seen, v):
                thrown += 1
                continue
            to_process.put(v)
            best = max(best, v[1][3])

    return best


def part1(inp):
    global TIME
    TIME = 24
    res = 0
    for (idx, blueprint) in inp:
        geodes = run_search(blueprint)
        print(f'blueprint {idx} can get {geodes}')
        res += idx * geodes

    return res


def part2(inp):
    global TIME  # womp womp
    TIME = 32

    res = 1
    for (idx, blueprint) in inp[:3]:
        geodes = run_search2(blueprint)
        print("geodes: ", geodes)
        res *= geodes

    return res


inp = get_input("input.txt")

print("part 1:", part1(inp))
print("part 2:", part2(inp))

