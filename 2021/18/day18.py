from itertools import combinations
from functools import reduce

# Node either represents a "snailfish number" or a single normal number.
class Node:
    def __init__(self, left=None, right=None, value=None, parent=None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = parent

        if left is not None:
            left.parent = self

        if right is not None:
            right.parent = self

    def __str__(self):
        if self.value is not None:
            return str(self.value)

        return "[{},{}]".format(str(self.left), str(self.right))

    def __add__(self, other):
        res = Node(left=self, right=other)
        res.reduce()
        return res

    # iterate through the leaf nodes
    def leaf_nodes(self):
        n = self
        while n.left is not None:
            n = n.left

        while n:
            yield n
            n = n.next()

    def _reduce(self):
        for n in self.leaf_nodes():
            if (n.parent.left.value is not None and
                    n.parent.right.value is not None and
                    n.parent.num_parents() >= 4):
                n.parent.explode()
                return True

        for n in self.leaf_nodes():
            if n.value >= 10:
                n.split()
                return True

        return False

    def reduce(self):
        while self._reduce():
            pass

    def explode(self):
        assert self.left.value is not None
        assert self.right.value is not None

        l, r = self.prev(), self.next()
        if l:
            l.value += self.left.value
        if r:
            r.value += self.right.value

        self.left, self.right = None, None
        self.value = 0

    def split(self):
        self.left = Node(value=self.value//2, parent=self)
        self.right = Node(value=self.value//2 + self.value%2, parent=self)
        self.value = None

    def num_parents(self):
        return 0 if self.parent is None else 1 + self.parent.num_parents()

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def next(self):
        prev, p = self, self.parent

        while p and p.right == prev:
            prev, p = p, p.parent

        if p is None:
            return None

        res = p.right
        while res.left is not None:
            res = res.left

        return res

    def prev(self):
        prev, p = self, self.parent
        while p and p.left == prev:
            prev, p = p, p.parent

        if p is None:
            return None

        res = p.left
        while res.right is not None:
            res = res.right

        return res


def parse_tree(it):
    # Convenience so we can call parse_tree on a string instead of an iterator.
    if isinstance(it, str):
        return parse_tree(iter(it))

    lch = next(it)

    if lch != "[":
        return Node(value=int(lch))

    left = parse_tree(it)
    assert next(it) == ","
    right = parse_tree(it)
    assert next(it) == "]"

    return Node(left=left, right=right)


def get_input(fname):
    with open(fname, 'r') as f:
        return [l.strip() for l in f]


def part1(inp):
    return reduce(lambda a, b: a+b, map(parse_tree, inp)).magnitude()


def part2(inp):
    mag_sum = lambda x: (parse_tree(x[0]) + parse_tree(x[1])).magnitude()
    return max(map(mag_sum, combinations(inp, 2)))


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("partr2:", part2(inp))

