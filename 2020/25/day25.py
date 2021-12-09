from collections import defaultdict

def get_input():
    return (9033205, 9281649)


def transform(subject_number, loop_size):
    v = 1
    for i in range(loop_size):
        v *= subject_number
        v = v % 20201227
    return v


def find_loop_size(subject, target):
    v = 1
    for i in range(20201227):
        v *= subject
        v = v % 20201227
        if v == target:
            return i+1
    print("find_loop_size failed")
    exit()


'''
CARD_PUBLIC = transform(7, CARD_LOOP)
DOOR_PUBLIC = transform(7, DOOR_LOOP)
'''

card_public = 9033205
door_public = 9281649



# print("TEST:", find_loop_size(7, 5764801))
# print("should be: 8")



card_loop = find_loop_size(7, card_public)
door_loop = find_loop_size(7, door_public)

print(card_loop, door_loop)

print(transform(card_public, door_loop))
print(transform(door_public, card_loop))
