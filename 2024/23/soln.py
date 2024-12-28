from collections import defaultdict
from itertools import combinations

def parse_input(fname):
    with open(fname, 'r') as f:
        return list(l.split("-") for l in f.read().splitlines())


def adjacency_list(L):
    E = defaultdict(lambda: [])
    for (u, v) in L:
        E[u].append(v)
        E[v].append(u)
    return E


def part1(L):
    E = adjacency_list(L)
    triangles = set()

    for u in E.keys():
        one_hop = set(E[u])
        for v in one_hop:
            for w in E[v]:
                if w in one_hop:
                    triangles.add(tuple(sorted((u,v,w))))

    return sum(1 for x in triangles if any(u[0]=='t' for u in x))


N = 13  # Each node has N neighbors


def check_clique(E, nodes):
    for u in nodes:
        for v in nodes:
            if u !=v and v not in E[u]:
                return False
    return True


def part2(L):
    E = adjacency_list(L)

    for k in range(N, 2, -1):
        for u in E.keys():
            candidates = E[u]+[u]
            for combo in combinations(candidates, k):
                if check_clique(E, combo):
                    return ','.join(sorted(combo))
    return None


if __name__ == "__main__":
    L = parse_input("inp.txt")
    print("part 1:", part1(L))
    print("part 2:", part2(L))