import rubik
from collections import deque


# only for testing
def index(dq, x):
    for i in range(len(dq)):
        if dq[i] == x:
            return i
    return -1


def print_output(path):
    for i in path:
        print(rubik.quarter_twists_names[i])


def neighbours(position):
    """
    given a position returns the list of the positions obtainable by one quarter twist
    """
    res = []
    for operation in rubik.quarter_twists:
        res.append((rubik.perm_apply(position, operation), operation))
    return res


def validity_check(key, predecessor):
    for i in range(1, 8):
        key = predecessor[key][0]
        if predecessor[key][0] == key:
            return True
    return False


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []
    # helper structures
    # stores elements that have already been popped from at least one queue
    popped = {}
    # dictionaries storing shortest length paths to positions in the cube in the forwards and backwards direction
    distance_f = {}
    distance_b = {}
    # storing the predecessor in the forwards and backwards direction
    predecessor_f = {}
    predecessor_b = {}
    # a fifo queue used by BFS
    queue_f = deque()
    queue_b = deque()

    queue_f.append(start)
    queue_b.append(end)
    distance_f[start] = 0
    distance_b[end] = 0
    predecessor_f[start] = (start, None)
    predecessor_b[end] = (end, None)

    terminate = False
    w = None
    counter = 1
    while not terminate:
        u = queue_f.popleft()
        if not validity_check(u, predecessor_f):
            return None
        if u not in popped:
            popped[u] = 1
        else:
            terminate = True
            w = u
        for v in neighbours(u):
            if v[0] not in predecessor_f:
                distance_f[v[0]] = distance_f[u] + 1
                predecessor_f[v[0]] = (u, v[1])
                queue_f.append(v[0])

        u = queue_b.popleft()
        if not validity_check(u, predecessor_b):
            return None
        if u not in popped:
            popped[u] = 1
        elif not terminate:
            terminate = True
            w = u
        for v in neighbours(u):
            if v[0] not in predecessor_b:
                distance_b[v[0]] = distance_b[u] + 1
                predecessor_b[v[0]] = (u, v[1])
                queue_b.append(v[0])

    path_f = []
    v = w
    while v != start:
        path_f.append(predecessor_f[v][1])
        v = predecessor_f[v][0]
    path_f.reverse()
    path_b = []
    while w != end:
        path_b.append(rubik.perm_inverse(predecessor_b[w][1]))
        w = predecessor_b[w][0]
    path_f.extend(path_b)
    path_f.reverse()
    return path_f
