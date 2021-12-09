from collections import defaultdict

def get_input(fname):
    # return list() of tuples(set{ingredients}, set{allergens})
    res = []
    with open(fname, 'r') as f:
        for l in f.readlines():
            l = l.strip()
            greeds, allergens = l.split(' (contains ')
            greeds = set(greeds.split(' '))
            allergens = allergens[:-1]
            allergens = set(allergens.split(', '))
            res.append((greeds, allergens))
    return res

def identify_allergens(inp):
    # rebase to
    allergens = set()
    for _, a in inp:
        allergens |= a

    allergen_candidates = {}

    print("allergens: ", allergens)
    for allergen in allergens:
        candidates = None
        for greeds, agens in inp:
            if allergen not in agens:
                continue
            if candidates == None:
                candidates = set(greeds)
            else:
                candidates &= greeds
        allergen_candidates[allergen] = candidates

    res = {}
    while True:
        flag = False
        ing, alg = None, None
        for k, v in allergen_candidates.items():
            if len(v) == 1:
                res[k] = list(v)[0]
                ing = k
                alg = res[k]
                break
        if not ing:
            return res
        del allergen_candidates[ing]
        for _, v in allergen_candidates.items():
            if alg in v:
                v.remove(alg)



def part1(inp):
    # question: can we just determine what the allergens are straight up?
    allergens = identify_allergens(inp)
    print(allergens)
    print(len(allergens))

    bad_greeds = set(allergens.values())
    print(bad_greeds)

    return sum(len(k - bad_greeds) for k, _ in inp)

def part2(inp):
    m = identify_allergens(inp)
    return ','.join(m[allergen] for allergen in sorted(m.keys()))



inp = get_input("day21.in")

print("part1:", part1(inp))
print("part2:", part2(inp))
