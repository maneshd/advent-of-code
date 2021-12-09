

inp = (int(x) for x in '716892543')

class Node:

    def __init__(self,val):
        self.val = val
        self.prev = None
        self.next = None

def link(n1, n2):
    # n1.next = n2
    # n2.prev = n1
    n1.next, n2.prev = n2, n1

def print_list(s):
    res = []
    while s.val not in res:
        res.append(s.val)
        s = s.next
    print(tuple(res))
    print(''.join(str(i) for i in res))

def make_move(cup):
    # cup is the current cup.
    # returns the next cup.
    c1 = cup.next
    c2 = c1.next
    c3 = c2.next
    target_val = cup.val - 1 if cup.val != 1 else 9
    while target_val in (c1.val, c2.val, c3.val):
        target_val = target_val - 1 if target_val > 1 else 9

    target = c3.next
    while target.val != target_val:
        target = target.next

    # rewire!
    link(cup, c3.next)
    link(c3, target.next)
    link(target, c1)
    return cup.next



def part1():

    L = [Node(x) for x in inp]

    n = len(L)
    for i in range(len(L)):
        L[i].prev = L[(i-1)%n]
        L[i].next = L[(i+1)%n]

    cup = L[0]
    for i in range(100):
        cup = make_move(cup)
    print_list(cup)


def smart_move(cup, H):
    c1 = cup.next
    c2 = c1.next
    c3 = c2.next
    target_val = cup.val
    while target_val in (cup.val, c1.val, c2.val, c3.val):
        target_val = target_val -1 if target_val > 1 else 1000000
    target = H[target_val]

    # rewire!
    link(cup, c3.next)
    link(c3, target.next)
    link(target, c1)
    return cup.next

def part2():

    L = [Node(x) for x in inp]
    H = [None] * 1000001

    for i in range(len(L)-1):
        link(L[i], L[i+1])

    for n in L:
        H[n.val] = n

    current = L[-1]
    for i in range(10, 1000001):
        H[i] = Node(i)
        link(current, H[i])
        current = H[i]
    link(H[1000000], L[0])

    cup = L[0]

    for i in range(10000000):
        if i % 1000000 == 0:
            print(i/10000000)
        cup = smart_move(cup, H)

    return H[1].next.val * H[1].next.next.val



# print("part1:", part1())
print("part2:", part2())
