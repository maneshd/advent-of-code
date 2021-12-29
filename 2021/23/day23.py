from collections import namedtuple


State = namedtuple('State', ['hall', 'rooms'])


ROOM_LOCS = {'A':2, 'B':4, 'C':6, 'D':8}
ROOM_IDXS = {'A':0, 'B':1, 'C':2, 'D':3}
IDX_TO_CH = 'ABCD'
ROOM_IDX_TO_HALL_IDX = (2, 4, 6, 8)
M = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


# Returns the lowest cost possible if the amphipods could pass right
# through each other in the hallways (but not the rooms).
def base_cost(s):
    res = 0
    for start_idx, room in enumerate(s.rooms):
        roomchar = IDX_TO_CH[start_idx]

        if all(x == roomchar for x in room):
            continue
        min_idx = 0
        while room[min_idx] == roomchar:
            min_idx += 1

        # This adds in the cost of moving other guys back into this room.
        for i in range(min_idx, len(room)):
            res += (len(room)-i)*M[roomchar]

        for inner_idx, ch in enumerate(room):
            if inner_idx < min_idx:
                continue
            i = ROOM_IDX_TO_HALL_IDX[start_idx]
            j = ROOM_LOCS[ch]

            # Add the cost of leaving the room plus moving horizontally
            # to the goal room.
            res += ((len(room)-inner_idx) + abs(j-i))*M[ch]

    return res


# Returns the number of extra steps to get from start_idx to goal_idx
# if we have to pass through target_idx on the way.
def extra_steps(start_idx, target_idx, goal_idx):
    # Simplify the logic by ensuring start_idx <= goal_idx
    if start_idx > goal_idx:
        start_idx, goal_idx, target_idx = -start_idx, -goal_idx, -target_idx

    if start_idx < target_idx < goal_idx:
        return 0
    if start_idx == goal_idx or target_idx < start_idx:
        return 2*abs(target_idx - start_idx)
    if goal_idx < target_idx:
        return 2*abs(target_idx - goal_idx)

    assert False


def add_to_room(room, ch):
    room = list(room)
    room[room.index('.')] = ch
    return ''.join(room)


# Gnaaaaaarly!
# Yields tuples of neighboring states plus thier adjusted cost,
# which is more or less the cost of superfluous movement.
def neighbors(s):
    # Try to move each amphipod in the hallway.
    for i, ch in enumerate(s.hall):
        if ch == '.':
            continue
        goal_room_idx = ROOM_IDXS[ch]
        goal_room_contents = s.rooms[goal_room_idx]
        # Is the room clear?
        if not all(x in ('.', ch) for x in goal_room_contents):
            continue
        # Is the path clear?
        j = ROOM_LOCS[ch]  # j = the hall idx of our goal room.
        if i < j and not s.hall[i+1:j+1] == '.'*(j-i):
            continue
        if j < i and not s.hall[j:i] == '.'*(i-j):
            continue

        # We're goooood.
        hall = list(s.hall)
        rooms = list(s.rooms)
        hall[i] = '.'
        rooms[goal_room_idx] = add_to_room(rooms[goal_room_idx], ch)
        s2 = State(''.join(hall), tuple(rooms))
        cost = 0
        yield (s2, cost)

    # Try to move amphipods out of each room.
    for start_room_idx, room in enumerate(s.rooms):
        # See if there's anyone that needs to be moved out of the room.
        roomchar = IDX_TO_CH[start_room_idx]  
        if all(x in ('.', roomchar) for x in room):
            continue

        # Determine the index of the amphipod who is not blocked in the room.
        inner_idx = len(room)-1
        while room[inner_idx] == '.':
            inner_idx -= 1
        ch = room[inner_idx]

        # start idx = i, target idx = j
        i = ROOM_IDX_TO_HALL_IDX[start_room_idx]
        for (j, hallchar) in enumerate(s.hall):
            # Check if j is in front of a room.
            if j in ROOM_LOCS.values():
                continue
            # Check if occupied.
            if hallchar != '.':
                continue
            # Check if path from i to j is clear.
            if i < j and not s.hall[i+1:j+1] == '.'*(j-i):
                continue
            if j < i and not s.hall[j:i] == '.'*(i-j):
                continue

            # The path is clear.
            hall = list(s.hall)
            rooms = list(s.rooms)
            hall[j] = ch

            room = list(rooms[start_room_idx])
            room[inner_idx] = '.'
            rooms[start_room_idx] = ''.join(room)

            s2 = State(''.join(hall), tuple(rooms))

            goal_idx = ROOM_LOCS[ch]
            cost = extra_steps(i, j, goal_idx) * M[ch]

            yield (s2, cost)


# debugging
def pstring(s):
    rooms = tuple(zip(*s.rooms))
    if len(rooms) == 4:
        return "\n".join([
            "#"*13,
            "#{}#".format(s.hall),
            "###{}###".format("#".join(rooms[3])),
            "  #{}#  ".format("#".join(rooms[2])),
            "  #{}#  ".format("#".join(rooms[1])),
            "  #{}#  ".format("#".join(rooms[0])),
            "  #########  "
        ])

    return "\n".join([
        "#"*13,
        "#{}#".format(s.hall),
        "###{}###".format("#".join(rooms[1])),
        "  #{}#  ".format("#".join(rooms[0])),
        "  #########  "
        ])


# O(n) - good enough :)
def extract_min(d):
    (v, k) = min((v, k) for (k, v) in d.items())
    del d[k]
    return k, v

# Dijkstra.
def solution(s0, goal):
    known = set([s0])
    to_process = {s0: 0}

    while to_process:
        s, cost = extract_min(to_process)
        known.add(s)

        if s == goal:
            return cost + base_cost(s0)

        for v, v_cost in neighbors(s):
            if v in known:
                continue
            to_process[v] = min(cost+v_cost, to_process.get(v, float('inf')))

    return None


INP1 = State('.'*11, ('DA', 'DC', 'BB', 'CA'))
TEST_INP1 = State('.'*11, ('AB', 'DC', 'CB', 'AD'))
GOAL1 = State('.'*11, ('AA', 'BB', 'CC', 'DD'))

INP2 = State('.'*11, ('DDDA', 'DBCC', 'BABB', 'CCAA'))
TEST_INP2 = State('.'*11, ('ADDB', 'DBCC', 'CABB', 'ACAD'))
GOAL2 = State('.'*11, ('AAAA', 'BBBB', 'CCCC', 'DDDD'))

print("Part1: ", solution(INP1, GOAL1))
print("Part2: ", solution(INP2, GOAL2))

