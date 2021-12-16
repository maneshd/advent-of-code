from functools import reduce
from collections import namedtuple

Packet = namedtuple('Packet', ['version', 'type', 'value', 'children'])


class BITSReader:
    def __init__(self, hex):
        bits = bin(int(hex, 16))[2:]
        pad = '0'*(len(hex)*4 - len(bits))
        self.bits = pad + bits
        self.idx = 0

    def read(self, n):
        self.idx += n
        return self.bits[self.idx-n:self.idx]


def parse_packet(reader):
    version, type_id = parse_header(reader)

    if type_id == 4:
        value = parse_literal(reader)
        children = []
        return Packet(version, type_id, value, children)

    # We have an operator!
    value = ''
    ltid = reader.read(1)

    if ltid == '1':
        num_subpackets = int(reader.read(11), 2)
        children = [parse_packet(reader) for x in range(num_subpackets)]
        return Packet(version, type_id, value, children)
    else:
        subpackets_length = int(reader.read(15), 2)
        children = []

        max_idx = reader.idx + subpackets_length
        while reader.idx < max_idx:
            children.append(parse_packet(reader))

        return Packet(version, type_id, value, children)

    print("Shouldn't get here!")
    exit()


def parse_header(reader):
    version, type_id = reader.read(3), reader.read(3)
    return int(version, 2), int(type_id, 2)


def parse_literal(reader):
    res = []
    while True:
        s, digits = reader.read(1), reader.read(4)
        res.append(digits)
        if s == '0':
            break
    return int(''.join(res), 2)


OPERATOR_FUNCS = {
  0: sum,
  1: lambda x: reduce(lambda a, b: a*b, x),
  2: min,
  3: max,
  5: lambda x: 1 if x[0] > x[1] else 0,
  6: lambda x: 1 if x[0] < x[1] else 0,
  7: lambda x: 1 if x[0] == x[1] else 0,
}

def evaluate_packet(p):
    if p.type == 4:
        return p.value

    f = OPERATOR_FUNCS[p.type]
    return f([evaluate_packet(x) for x in p.children])


def debugprint(packet, prefix=''):
    print('{}Packet(version={}, type={}, value={})'.format(prefix, packet.version, packet.type, packet.value))
    for x in packet.children:
        debugprint(x, prefix+' ')


def get_input(fname):
    with open(fname, 'r') as f:
        return f.read().strip()


def part1(inp):
    reader = BITSReader(inp)
    root = parse_packet(reader)

    def sum_versions(packet):
        return packet.version + sum(map(sum_versions, packet.children))

    return sum_versions(root)


def part2(inp):
    reader = BITSReader(inp)
    root = parse_packet(reader)
    return evaluate_packet(root)


inp = get_input("input.txt")
print("part 1:", part1(inp))
print("part 2:", part2(inp))
