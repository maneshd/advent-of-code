def parse_input(file_name):
    with open(file_name, 'r') as f:
        L, R = f.read().split("\n\n")
        regs = [int(s.split(" ")[2]) for s in L.split("\n")]
        program = [int(x) for x in R.split(" ")[1].split(",")]
        return regs, program


def run_program(regs, program):
    pc, out = 0, []
    combo = lambda x: x if x <= 3 else regs[x-4]

    while pc < len(program):
        op, x = program[pc:pc+2]
        A, B, C = regs
        if op == 0:
            A = A // 2**combo(x)
        elif op == 1:
            B = B ^ x
        elif op == 2:
            B = combo(x) % 8
        elif op == 3 and A != 0:
            pc = x
            continue
        elif op == 4:
            B = B ^ C
        elif op == 5:
            out.append(combo(x)%8)
        elif op == 6:
            B = A // 2**combo(x)
        elif op == 7:
            C = A // 2**combo(x)
        pc += 2
        regs = A, B, C

    return regs, out


def part1(regs, program):
    _, out = run_program(regs, program)
    return ','.join(map(str, out))


def part2(regs, program):
    '''
    1) 2,4   B = A % 8
    2) 1,1   B = B ^ 1
    3) 7,5   C = A // 2**B
    4) 4,7   B = B ^ C
    5) 1,4   B = B ^ 4
    6) 0,3   A = A // 2**3
    7) 5,5   out -> B % 8
    8) 3,0   repeat

    You can map out on paper what happens for each trio of digits (A%8).
    '''

    want_out = tuple(reversed(program))
    prefix = (0, 0, 0, 0, 0, 0, 0)

    def f(prefix, outputs):
        # Returns the minimum valued A register to get the outputs given the prefix.
        # A = < prefix=x10..x4> x3 x2 x1 <f(next)>
        x10, x9, x8, x7, x6, x5, x4 = prefix
        n10, n9, n8, n7, n6, n5, n4 = tuple((x+1) % 2 for x in prefix)

        if len(outputs) == 0:
            return tuple()
        target = outputs[0]

        binify = lambda x, y, z: z+2*y+4*x

        output_and_prefix = [
            (binify(n4, 0, 1), (0, 0, 0)),
            (binify(1, 0, 1), (0, 0, 1)),
            (binify(n6, n5, n4), (0, 1, 0)),
            (binify(n5, n4, 0), (0, 1, 1)),
            (binify(x8, x7, n6), (1, 0, 0)),
            (binify(x7, x6, x5), (1, 0, 1)),
            (binify(x10, n9, n8), (1, 1, 0)),
            (binify(x9, n8, x7), (1, 1, 1)),
        ]

        for output, p in output_and_prefix:
            if output == target:
                r = f(prefix[3:]+p, outputs[1:])
                if r is not None:
                    return p+r
        
        return None

    res = f(prefix, want_out)
    return int(''.join(str(x) for x in res), 2)


if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(*inp))
    print("part 2:", part2(*inp))