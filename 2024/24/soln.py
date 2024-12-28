def parse_input(fname):
    def parse_initial(s):
        s, n = s.split(": ")
        return s, int(n)
    
    def parse_gates(line):
        l, r = line.split(" -> ")
        l1, l2, l3 = l.split(" ")
        return (l2, l1, l3, r)

    with open(fname, 'r') as f:
        L, R = f.read().split("\n\n")
        L = list(map(parse_initial, L.split("\n")))
        R = list(map(parse_gates, R.split("\n")))
        return L, R


OPS = {
    'XOR': (lambda x,y: x^y),
    'AND': (lambda x,y: x&y),
    'OR': (lambda x,y: x|y),
}

def part1(start_values, gates):
    R = {k:v for (k,v) in start_values}
    G = {l4: (l1, l2, l3) for (l1, l2, l3, l4) in gates}

    def out(gate):
        if gate in R:
            return R[gate]
        
        op, g1, g2 = G[gate]
        res = OPS[op](out(g1), out(g2))
        R[gate] = res
        return res

    zs = [(gate, out(gate)) for gate in G.keys() if gate[0] == 'z']
    zs.sort(reverse=True)
    return int(''.join(str(x[1]) for x in zs), 2)


# From inspection :)
SWAPS = [
    (("XOR", "x15", "y15", "rpb"), ("AND", "y15", "x15", "ctg")),
    (("AND", "x31", "y31", "z31"), ("XOR", "fgs", "ctw", "dmh")),
    (("OR", "bvk", "trm", "z38"), ("XOR", "hhv", "pqr", "dvq")),
    (("AND", "dvh", "hnn", "z11"), ("XOR", "hnn", "dvh", "rpv"))
]

def swap_wires(gates, gate1, gate2):
    res = []
    for gate in gates:
        if gate == gate1:
            res.append((gate[0], gate[1], gate[2], gate2[3]))
        elif gate == gate2:
            res.append((gate[0], gate[1], gate[2], gate1[3]))
        else:
            res.append(gate)
    return res


def swap_all_wires(gates):
    res = gates
    for a, b in SWAPS:
        res = swap_wires(res, a, b)
    return res


def check_for_weirdness(gates):
    gates = swap_all_wires(gates)
    G = {(in1, op, in2): out for (op, in1, in2, out) in gates}

    def check_digit(i):
        x = f"x0{i}" if i < 10 else f"x{i}"
        y = f"y0{i}" if i < 10 else f"y{i}"
        z = f"z0{i}" if i < 10 else f"z{i}"

        # Want: x XOR y 
        x_xor_y = G[(x, "XOR", y)] if (x, "XOR", y) in G else G[(y, "XOR", x)]
        x_and_y = G[(x, "AND", y)] if (x, "AND", y) in G else G[(y, "AND", x)]

        # zi gate should be (x ^ y) ^ c
        zi_gate = [gate for gate in gates if gate[3] == z]
        assert(len(zi_gate) == 1)
        # Should be x_xor_y XOR previous carry :)
        op, a, b, _ = zi_gate[0]
        if x_xor_y not in (a, b):
            print("bad gate:", zi_gate[0], "\nshould contain: ", x_xor_y)
            print("")
            return
        ci = a if b == x_xor_y else b

        mid_gate = [out for (op, a, b, out) in gates if op == "AND" and (x_xor_y, ci) in ((a,b), (b,a))]
        if len(mid_gate) != 1:
            print(mid_gate) # Problem!
        
        cj = [out for (op, a, b, out) in gates if (x_and_y, mid_gate[0]) in ((a,b), (b,a))]
        if len(cj) != 1:
            print("carry issue: ", cj, i)
            print("x_xor_y", x_xor_y)
            print("x_and_y", x_and_y)
            print("mid_gate:", mid_gate)

    for i in range(1, 44):
        check_digit(i)


def part2():
    res = []
    for a, b in SWAPS:
        res.append(a[-1])
        res.append(b[-1])
    return ",".join(sorted(res))

if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(*inp))
    print("part 2:", part2())

    
