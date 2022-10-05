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
    while points != []:
        point = points.pop(0)
        debug("DONE:")
        debug(points_done)
        convex_shape = convex(points_done)
        convex_shape.append(convex_shape[0])
        debug("CONVEX:")
        debug(convex_shape)
        for i in range(0, len(convex_shape)-1):
            p1, p2, p3 = convex_shape[i], convex_shape[i+1], point
            if (get_cross_product(p1, p2, p3) < 0) and p1[0] != p2[0] != p3[0] and p1[1] != p2[1] != p3[1]:
                triangles.append([p1, p2, p3])
        points_done.append(point)

    debug("POINTS DONE:")
    debug(points_done)

    return (triangles)


def calculate_delaunay(triangles):
    if len(triangles) == 1:
        return triangles
    pairs = calculate_triangle_pairs(triangles)


    # mark all pairs as unchecked
    pairs = [[x, 0] for x in pairs]

    while not all_checked(pairs):
        # original triangles
        pair_full = pairs.pop(0)
        pair = pair_full[0]
        check = pair_full[1]
        [edge, t1, t2] = pair

        # new triangles
        new_pair = make_locally_delaunay(pair)
        [new_edge, new_t1, new_t2] = new_pair

        check = 1

        if new_pair != pair:
            check = 0
            for p in pairs:
                p = p[0]
                if t1 == p[1] or t2 == p[1]:
                    if find_common_edge(new_t1, p[2]) != None:
                        p[1] = new_t1
                    elif find_common_edge(new_t2, p[2]) != None:
                        p[1] = new_t2
                if t1 == p[2] or t2 == p[2]:
                    if find_common_edge(new_t1, p[1]) != None:
                        p[2] = new_t1
                    elif find_common_edge(new_t2, p[1]) != None:
                        p[2] = new_t2

        pairs.append([new_pair, check])

    pairs = [x[0] for x in pairs]

    # TODO: optimise
    triangles_to_return = []
    for p in pairs:
        for t in p[1:]:
            if t not in triangles_to_return:
                triangles_to_return.append(t)

    return triangles_to_return


def all_checked(pairs):
    for pair in pairs:
        if pair[1] == 0:
            return False
    return True


def circle_from_triangle(t):
    [p1, p2, p3] = t
    middle1 = ((p1[0] + p2[0])/2, (p1[1]+p2[1])/2)
    middle2 = ((p2[0] + p3[0])/2, (p2[1]+p3[1])/2)
    slope1 = get_slope(p1, p2)
    slope2 = get_slope(p2, p3)

    # General equation of circle:
    # x^2 + y^2 + Ax + By + C = 0

    a = np.array([[p1[0], p1[1], 1], [p2[0], p2[1], 1], [p3[0], p3[1], 1]])
    b = np.array([-(p1[0]**2 + p1[1]**2), -(p2[0]**2 + p2[1]**2), -(p3[0]**2 + p3[1]**2)])
    A,B,C = np.linalg.solve(a, b)
    A,B,C = A.item(),B.item(),C.item()

    pm = [-1*A/2, -1*B/2] 
    r = math.sqrt((A/2)**2 + (B/2)**2 - C)

    return [pm, r]


def calculate_triangle_pairs(triangles):
    pairs = []
    for i in range(len(triangles)):
        for j in range(i + 1, len(triangles)):
            t1 = triangles[i]
            t2 = triangles[j]
            edge = find_common_edge(t1, t2)
            if edge != None:
                pairs.append([edge, t1, t2])

    return pairs


def find_common_edge(t1, t2):
    edges1 = edges_from_triangle(t1)
    edges2 = edges_from_triangle(t2)
    for e1 in edges1:
        for e2 in edges2:
            if e1[0] in e2 and e1[1] in e2:
                return e1
    return None


def edges_from_triangle(t):
    return [[t[0], t[1]], [t[1], t[2]], [t[2], t[0]]]


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
        t1 = [p_t1, p_t2, edge.pop(0)]
        t2 = [p_t1, p_t2, edge.pop(0)]
        edge = [p_t1, p_t2]

    if len(t1) != 3 or len(t2) != 3 or len(edge) != 2:
        print("ERROR: something went wrong making local delaunay: ")
        print(edge)
        print(t1)
        print(t2)
        exit(1)

    return [edge, t1, t2]


if __name__ == '__main__':
    pass