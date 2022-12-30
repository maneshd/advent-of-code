''' Warning: Part 2 takes ~5 minutes to run :) '''
from collections import deque

def get_input(fname):
    with open(fname, 'r') as f:
        return _get_input(f)


def _get_input(f):
    flows = {}
    G = {}

    for line in f.readlines():
        line = line.strip().replace("valve ", "valves ")  # lol, I refuse to use regex
        u = line[6:8]
        flows[u] = int(line[line.index("=")+1 : line.index(";")])
        G[u] = line.split(" valves ")[1].split(", ")

    return G, flows

def BFS(G, s):
    dist = {s:0}
    to_process = deque([s])

    while to_process:
        u = to_process.popleft()
        for v in G[u]:
            if v in dist:
                continue
            dist[v] = dist[u] + 1
            to_process.append(v)

    return dist

# Transform the graph to only have the nodes with >0 flow-rate
# Return new graph GG which has an adjacency map mapping a node to its neighbors 
# and their edge weights (where weight is # of hops)
def transformed_graph(G, flows):
    nodes = ["AA"] + [node for (node, flow) in flows.items() if flow > 0]
    GG = {node: [] for node in nodes}

    for s in nodes:
        d = BFS(G, s)
        for t in nodes:
            if t in (s, 'AA'):  # no self-edges; don't go back to AA
                continue
            GG[s].append((t, d[t]+1))  # add 1 for time to open valve

    return GG


def neighbors_p1(G, flows, cur_state):
    max_time = 30
    u, openValves, t, score = cur_state
    
    for (v, dt) in G[u]:
        if v in openValves:
            continue
        if t+dt > max_time:
            continue

        dscore = (max_time - (t+dt)) * flows[v]
        newValves = tuple(sorted(openValves + (v,)))

        yield (v, newValves, t+dt, score+dscore)


def part1(inp):
    G, flows = inp
    G = transformed_graph(*inp)

    s = ('AA', tuple(), 0, 0)  # position, open-valves, time, score
    to_process = deque([s])
    seen = set([s])

    while to_process:
        u = to_process.popleft()
        for v in neighbors_p1(G, flows, u):
            if v in seen:
                # probably won't happen much?
                continue
            to_process.append(v)
            seen.add(v)

    print(len(seen))

    return max(x[3] for x in seen)


def make_canonical(u):
    u1, u2, valves, t1, t2, score = u
    if (u1 > u2):
        return u2, u1, valves, t2, t1, score
    else:
        return u

def neighbors_p2(G, flows, cur_state):
    max_time = 26
    u1, u2, openValves, t1, t2, score = cur_state

    for (v1, dt1) in G[u1]:

        # See if u1=>v1 is viable
        if v1 in openValves:
            continue
        if t1+dt1 > max_time:
            continue

        # Move for u1=>v1 without moving u2
        dscore = (max_time - (t1+dt1))*flows[v1]
        newValves = tuple(sorted(openValves + (v1,)))
        yield (v1, u2, newValves, t1+dt1, t2, score+dscore)

        for (v2, dt2) in G[u2]:
            # is u2 => v2 viable (along with u1=>v1)?
            if v2 in openValves or v1 == v2:
                continue
            if t2+dt2 > max_time:
                continue

            dscore = (max_time - (t1+dt1))*flows[v1] + (max_time - (t2+dt2))*flows[v2] 
            newValves = tuple(sorted(openValves + (v1, v2)))
            yield (v1, v2, newValves, t1+dt1, t2+dt2, score+dscore)

    # and now also move just u2 :)
    for (v2, dt2) in G[u2]:
        if v2 in openValves or t2+dt2 > max_time:
            continue

        dscore = (max_time - (t2+dt2))*flows[v2]
        newValves = tuple(sorted(openValves + (v2,)))
        yield (u1, v2, newValves, t1, t2+dt2, score+dscore)


def part2(inp):
    G, flows = inp
    G = transformed_graph(*inp)

    s = ('AA', 'AA', tuple(), 0, 0, 0)  # p1, p2, open-valves, t1, t2, score
    to_process = deque([s])
    seen = set([s])
    # Seen 2 keeps track of the times/scores for locations+open-valves we've seen
    seen2 = {('AA', 'AA', tuple()): [(0, 0, 0)]}  # map from p1, p2,

    c = 0

    while to_process:
        u = to_process.popleft()
        c += 1
        if c % 10000 == 0:
            print(f'processed: {c}. to_process currently has {len(to_process)} left')

        for v in neighbors_p2(G, flows, u):
            # We don't care which agent is which, so put them in a canonical ordering
            v = make_canonical(v)

            if v in seen:
                continue

            # Ignore it if we've seen something better before.
            u1, u2, valves, t1, t2, score = v
            if not (u1, u2, valves) in seen2:
                seen2[(u1, u2, valves)] = [(t1, t2, score)]
            else:
                seen_better = False
                for (tt1, tt2, s) in seen2[(u1, u2, valves)]:
                    if score <= s and t1 >= tt1 and t2 >= tt2:
                        seen_better = True
                        break
                if seen_better:
                    continue
                seen2[(u1, u2, valves)].append((t1, t2, score))

            to_process.append(v)
            seen.add(v)

    print(len(seen))

    return max(x[-1] for x in seen)


inp = get_input("input.txt")
#  inp = get_input("test.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))

