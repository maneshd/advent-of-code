REQ = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
OPT = ['cid']

def get_input(fname):
    res = []
    with open(fname, 'r') as f:
        current = []
        for l in f.readlines():
            l = l.strip()
            if l == '' and current:
                res.append(current)
                current = []
                continue
            for kv in l.split(' '):
                k, v = kv.split(':')
                current.append((k,v))

        if current:
            res.append(current)
        return res


def validate(p):
    keys = [x[0] for x in p]
    for x in REQ:
        if x not in keys:
            return False
    for k in keys:
        if k not in REQ and k not in OPT:
            return False
    return True


pps = get_input('day4.in')
part1 = sum(1 for x in pps if validate(x))
print("part1: ", part1)


def is_num(x, mn, mx):
    try:
        a = int(x)
        return mn <= a and a <= mx
    except:
        return False

def byr(x):
    return is_num(x, 1920, 2002)

def iyr(x):
    return is_num(x, 2010, 2020)

def eyr(x):
    return is_num(x, 2020, 2030)

def hgt(x):
    if len(x) <= 2:
        return False
    p, s = x[:-2], x[-2:]
    if s == 'cm':
        return is_num(p, 150, 193)
    if s == 'in':
        return is_num(p, 59, 76)
    return False

def hcl(x):
    if len(x) != 7:
        return False
    if x[0] != '#':
        return False
    for c in x[1:]:
        if c not in '1234567890abcdef':
            return False
    return True

def ecl(x):
    return x in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

def pid(x):
    return len(x) == 9 and all(a in '1234567890' for a in x)

def cid(x):
    return True

validators = {
  'byr': byr,
  'iyr': iyr,
  'eyr': eyr,
  'hgt': hgt,
  'hcl': hcl,
  'ecl': ecl,
  'pid': pid,
  'cid': cid,
}

def vvalidate(p):
    return all(validators[k](v) for k, v in p)

part2 = sum(1 for x in pps if validate(x) and vvalidate(x))
print("part2: ", part2)
