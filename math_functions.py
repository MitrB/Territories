import math
from logging import debug, info
import numpy as np

# https://lvngd.com/blog/convex-hull-graham-scan-algorithm-python/


def convex(points):
    points = points.copy()
    points.sort(key=lambda x: [x[0], x[1]])
    hull = []
    start = points.pop(0)
    hull.append(start)
    points.sort(key=lambda p: (get_slope(p, start), -p[1], p[0]))
    while points != []:
        hull.append(points.pop(0))
        while len(hull) > 2 and get_cross_product(hull[-3], hull[-2], hull[-1]) < 0:
            hull.pop(-2)
    return hull


def get_slope(p1, p2):
    if p1[0] == p2[0]:
        return float('inf')
    else:
        return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])


def get_cross_product(p1, p2, p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))


def calculate_pbp_triangulation(points):
    points.sort(key=lambda x: [x[0], x[1]])
    debug("POINTS:")
    debug(points)

    triangles = []
    triangles.append(points[:3])
    points_done = points[:3]
    points = points[3:]
    while points != []:  # :
        point = points.pop(0)
        debug("DONE:")
        debug(points_done)
        convex_shape = convex(points_done)
        convex_shape.append(convex_shape[0])
        debug("CONVEX:")
        debug(convex_shape)
        for i in range(0, len(convex_shape)-1):
            p1, p2, p3 = convex_shape[i], convex_shape[i+1], point
            if (get_cross_product(p1, p2, p3) < 0) and not collinear(p1, p2, p3):
                triangles.append([p1, p2, p3])
        points_done.append(point)

    debug("POINTS DONE:")
    debug(points_done)

    return (triangles)


def calculate_delaunay(triangles):
    if len(triangles) == 1:
        return triangles
    pairs = calculate_triangle_pairs(triangles)

    edge_stack = [key for key in pairs]
    edge_mark = {edge: True for edge in pairs}

    while edge_stack != []:
        # pop edge and unmark
        edge = edge_stack.pop()
        edge_mark[edge] = False
        pair = pairs[edge]
        # check = pair_full[1]
        [t1, t2] = pair

        # new triangles
        new_pair = make_locally_delaunay([edge, t1, t2])
        [new_edge, new_t1, new_t2] = new_pair

        # If we had to flip the edge, there are 4 possible triangles that have a new pair
        if new_edge != edge:
            # delete old edge, add new edge
            pairs.pop(edge)
            pairs[new_edge] = [new_t1, new_t2]
            # unmark new edge
            edge_mark[new_edge] = False
            # get edges from new pairs
            pair_edges_to_change = list(
                edges_from_triangle(t1) + edges_from_triangle(t2))
            print(edge)
            print(pair_edges_to_change)
            pair_edges_to_change.remove(edge)
            pair_edges_to_change.remove(edge)

            # Update triangles
            for pe in pair_edges_to_change:
                if pe in pairs:
                    [tpe1, tpe2] = pairs[pe]
                    if find_common_edge(tpe1, new_t1) == pe and not (tpe1 == t1 or tpe1 == t2):
                        pairs[pe] = [tpe1, new_t1]
                    elif find_common_edge(tpe2, new_t2) == pe and not (tpe2 == t1 or tpe2 == t2):
                        pairs[pe] = [new_t2, tpe2]
                    elif find_common_edge(tpe2, new_t1) == pe and not (tpe2 == t1 or tpe2 == t2):
                        pairs[pe] = [tpe2, new_t1]
                    elif find_common_edge(tpe1, new_t2) == pe and not (tpe1 == t1 or tpe1 == t2):
                        pairs[pe] = [new_t2, tpe1]

                    # if not marked add to the stack for re-evaluation
                    if not edge_mark[pe]:
                        edge_stack.append(pe)
                        edge_mark[pe] = True

    # TODO: optimise
    triangles_to_return = []
    for key, value in pairs.items():
        for t in value:
            if t not in triangles_to_return:
                triangles_to_return.append(t)   

    return triangles_to_return

def circle_from_triangle(t):
    [p1, p2, p3] = t
    circle = define_circle(p1, p2, p3)
    [pm, r] = circle

    return [pm, r]

# https://stackoverflow.com/questions/28910718/give-3-points-and-a-plot-circle
def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return (None, np.inf)

    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return ((cx, cy), radius)


def calculate_triangle_pairs(triangles):
    pairs = {}
    for i in range(len(triangles)):
        for j in range(i + 1, len(triangles)):
            t1 = triangles[i]
            t2 = triangles[j]
            edge = find_common_edge(t1, t2)
            if edge != None:
                pairs[edge] = [t1, t2]

    return pairs


def find_common_edge(t1, t2):
    """returns 1 common edge of 2 given triangles"""
    # edges1 = edges_from_triangle(t1)
    # edges2 = edges_from_triangle(t2)
    # for e1 in edges1:
    #     for e2 in edges2:
    #         if e1[0] in e2 and e1[1] in e2:
    #             return tuple(sorted(e1))
    edges = zip(t1,t2)

    for edge in edges:
        [p1, p2] = edge
        if ((p1 in t2 and p2 in t1) or (p1 in t1 and p2 in t2)) and p1 != p2:
            return tuple(sorted(edge))
    
    return None


def edges_from_triangle(t):
    return (tuple(sorted((t[0], t[1]))), tuple(sorted((t[1], t[2]))), tuple(sorted((t[2], t[0]))))


def make_locally_delaunay(pair):
    edge, t1, t2 = pair

    c = circle_from_triangle(t1)

    # point that is not in t2
    p_t2 = []
    for p in t1:
        if p not in t2:
            p_t2 = p

    # point that is not in t1
    p_t1 = []
    for p in t2:
        if p not in t1:
            p_t1 = p

    if math.dist(p_t1, c[0]) < c[1]:
        t1 = (p_t1, p_t2, edge[0])
        t2 = (p_t1, p_t2, edge[1])

        # first is faster but might be wrong, but shouldn't be 
        # edge = tuple(sorted((p_t1, p_t2)))
        edge = find_common_edge(t1, t2)

    if len(t1) != 3 or len(t2) != 3 or len(edge) != 2:
        print("ERROR: something went wrong making local delaunay: ")
        print(edge)
        print(t1)
        print(t2)
        exit(1)

    return [edge, t1, t2]


def collinear(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    """ Calculation the area of 
        triangle. We have skipped
        multiplication with 0.5 to
        avoid floating point computations """
    a = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)

    if (a == 0):
        return True
    else:
        return False


if __name__ == '__main__':
    pass
