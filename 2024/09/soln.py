from collections import defaultdict

def parse_input(file_name):
    with open(file_name, 'r') as f:
        return list(map(int, f.read().strip()))



def part1(inp):
    L = []
    for i, n in enumerate(inp):
        id = i//2 if i%2 == 0 else -1
        L.extend([id]*n)
    
    i, j = 0, len(L)-1
    while L[i] != -1:
        i += 1
    while L[j] == -1:
        j -= 1
    
    while i < j:
        L[i], L[j] = L[j], L[i]
        i += 1
        while i < len(L) and L[i] != -1:
            i += 1
        j -= 1
        while j >= 0 and L[j] == -1:
            j -= 1
    
    L = [x for x in L if x != -1]
    return sum(idx*n for (idx, n) in enumerate(L))


# A linkedlist is probably overkill, but whatever :)
class Entry:
    def __init__(self, id, length, prev, next):
        self.id = id
        self.length = length
        self.prev = prev
        self.next = next
    

empty = lambda entry: entry.id == -1


def part2(inp):
    head = None
    tail = None
    
    for i, n in enumerate(inp):
        if n == 0:
            continue
        id = i//2 if i%2 == 0 else -1
        if head == None:
            head = tail = Entry(id, n, None, None)
        else:
            tail.next = Entry(id, n, tail, None)
            tail = tail.next

    b = tail
    i = 0
    
    while b:
        if empty(b):
            b = b.prev
            continue

        # Find a hole for b :)
        a = head
        while a != b:
            if empty(a) and a.length >= b.length:
                break
            a = a.next
        
        # No hole for b
        if a == b:
            b = b.prev
            continue

        # b fits into a :)
        orig_b = b
        b = Entry(b.id, b.length, None, None)

        a.prev.next, b.prev = b, a.prev  # a.prev <-> b
        if a.length == b.length:
            b.next, a.next.prev = a.next, b # b <-> a.next
        else:
            # b <-> a' <-> a.next
            a = Entry(-1, a.length - b.length, b, a.next) # b <- a' -> a.next
            b.next, a.next.prev = a, a  # b -> a' <- a.next

        orig_b.id = -1
        b = orig_b.prev

    L = []
    a = head
    while a:
        L.extend([a.id]*a.length)
        a = a.next
    
    return sum(idx*n for (idx, n) in enumerate(L) if n != -1)
    

if __name__ == "__main__":
    inp = parse_input("inp.txt")
    print("part 1:", part1(inp))
    print("part 2:", part2(inp))
