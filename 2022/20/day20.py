def get_input(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.readlines()]


class Node:
    def __init__(self, value, prev=None):
        self.value = value
        self.prev = prev
        self.next = None


def make_list(inp):
    nodes = []

    for num in inp:
        node = Node(num)
        if len(nodes) > 0:
            nodes[-1].next = node
            node.prev = nodes[-1]
        nodes.append(node)

    # make it circular
    nodes[-1].next = nodes[0]
    nodes[0].prev = nodes [-1]

    return nodes


def move_n(n, node):
    for _ in range(n):
        A, C, B, D = node.prev, node, node.next, node.next.next
        A.next = B
        B.prev = A
        B.next = C
        C.prev = B
        C.next = D
        D.prev = C


def extract_res(node):
    while node.value != 0:
        node = node.next

    res = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.next
        res += node.value
    return res


def part1(inp):
    nodes = make_list(inp)
    N = len(nodes)

    for node in nodes:
        move_n(node.value % (N-1), node)

    return extract_res(nodes[0])


def part2(inp):
    inp = [x*811589153 for x in inp]
    nodes = make_list(inp)
    N = len(nodes)

    for i in range(10):
        print(f'iteration {i+1} of 10')
        for node in nodes:
            move_n(node.value % (N-1), node)

    return extract_res(nodes[0])


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))

