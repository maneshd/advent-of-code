


def get_input(fname):
    with open(fname, 'r') as f:
        return [int(x.strip()) for x in f.readlines()]

# if __name__ == "__main__"
def solve2(L):
    d = set()
    for x in L:
        if (2020 - x) in d:
            print(x, 2020-x, x*(2020-x))
        d.add(x)

def solve3(L):
    s1 = set(L)
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            x, y = L[i], L[j]
            z = 2020 - x - y
            if z in s1:
                print(x, y, z, x*y*z)
                return

in1 = get_input("day1.in")
solve2(in1)
solve3(in1)
