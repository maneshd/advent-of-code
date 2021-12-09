
def get_input(fname):
    with open(fname, 'r') as f:
        return [(x.strip()) for x in f.readlines()]

def majority_elem(r):
    return '1' if sum(1 for x in r if x == '1') >= len(r)/2 else '0'

# if __name__ == "__main__"
def part1(L):


    def flip(digit):
        return '1' if digit == '0' else '0'

    n1 = ''.join(majority_elem(x) for x in zip(*L))
    n2 = ''.join(flip(x) for x in n1)

    return int(n1, 2) * int(n2, 2)


def count_ones(x):
    return sum(1 for d in x if d == '1')

def count_zeros(x):
    return sum(1 for d in x if d == '0')


def part2(L):
    n1, n2 = -1, -1

    L1 = L[:]
    for i in range(len(L)):
        maj = '1' if count_ones(x[i] for x in L1) >= len(L1)/2 else '0'
        L1 = [x for x in L1 if x[i] == maj]
        if len(L1) == 1:
            n1 = L1[0]
            break

    L2 = L[:]
    for i in range(len(L)):
        mn = '0' if count_zeros(x[i] for x in L2) <= len(L2)/2 else '1'
        L2 = [x for x in L2 if x[i] == mn]
        if len(L2) == 1:
            n2 = L2[0]
            break
    print("res:")
    print(n1)
    print(n2)

    return int(n1, 2) * int(n2, 2)



in1 = get_input("day3.in")
# in1 = get_input("test.in")
print("part 1:", part1(in1))
print("part 2:", part2(in1))
