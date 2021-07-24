import rubik


def neighbours(position):
    """
    given a position returns the list of the positions obtainable by one quarter twist
    """
    res = []
    for operation in rubik.quarter_twists:
        res.append((position.perm_apply(operation), operation))
    return res


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
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
    queue_f = []
    queue_b = []

    queue_f.append(start)
    queue_b.append(end)
    distance_f[start] = 0
    distance_b[end] = 0

    terminate = False
    w = None
    while not terminate:
        u = queue_f.pop()
        if u not in popped:
            popped[u] = 1
        else:
            terminate = True
            w = u
        for v in neighbours(u):
            if v[0] not in predecessor_f:
                distance_f[v[0]] = distance_f[u] + 1
                predecessor_f[v[0]] = (u, v[1])
                print v[0]
                queue_f.append(v[0])

        u = queue_b.pop()
        if u not in popped:
            popped[u] = 1
        else:
            terminate = True
            w = u
        for v in neighbours(u):
            if v[0] not in predecessor_b:
                distance_b[v[0]] = distance_b[u] + 1
                predecessor_b[v[0]] = (u, v[1])
                queue_b.append(v[0])

    path_f = []
    path_f.append(w)
    v = w
    while predecessor_f[v] is not None:
        path_f.append(predecessor_f[v][1])
        v = predecessor_f[v][0]
    path_f.append(v)
    path_f.reverse()
    path_b = []
    while predecessor_b[w] is not None:
        path_b.append(predecessor_b[w][1])
        w = predecessor_b[w][0]
    path_f.append(w)
    path_f.extend(path_b)
    return path_f


