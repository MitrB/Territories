import math
from logging import debug, info

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
            if (get_cross_product(p1, p2, p3) < 0):
                triangles.append([p1, p2, p3])
        points_done.append(point)

    debug("POINTS DONE:")
    debug(points_done)

    return (triangles)


def calculate_delaunay(triangles):
    pairs = calculate_triangle_pairs(triangles)

    # mark all pairs as unchecked
    pairs = [[x, 0] for x in pairs]

    while not all_checked(pairs):
        print("Pairs:")
        print(pairs)
        # original triangles
        pair_full = pairs.pop(0)
        print("popped pair:")
        print(pair_full)
        pair = pair_full[0]
        check = pair_full[1]
        
        [edge, t1, t2] = pair

        # new triangles
        new_pair = make_locally_delaunay(pair)
        [new_edge, new_t1, new_t2] = new_pair

        # if new_pair != pair:
        #     for i in range(len(pairs)):
        #         if t1 == pairs[0][1]:
        #             if find_common_edge(t1, pair[0][2]) == new_pair[0]:
        #                 pairs[0][1] = new_pair[0]

        pairs.append([new_pair, 1])

    pairs = [x[0] for x in pairs]


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

    m1 = -1/slope1
    m2 = -1/slope2

    # y = mx + c
    c1 = middle1[1] - m1*middle1[0]
    c2 = middle2[1] - m2*middle2[0]
    pm_x = ((c2-c1)/(m1-m2))
    pm_y = m1*pm_x + c1
    pm = [pm_x, pm_y]

    r = math.dist(p1, pm)

    # print("slope1: " + str(slope1))
    # print("slope2: " + str(slope2))
    # print("c1: " + str(c1))
    # print("c2: " + str(c2))

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
        edge = [p_t1, p_t2]
        t1.remove(p_t2)
        t2.remove(p_t1)
        t1 = [p_t1, p_t2, t1[0]]
        t2.remove(t1[2])
        t2 = [p_t1, p_t2, t2[0]]

    return [edge, t1, t2]


if __name__ == '__main__':
    # circle = circle_from_triangle([[1, 2], [3, 4], [10, 1]])
    pair = [[[482, 538], [562, 922]], [[529, 414], [482, 538],
                                       [562, 922]], [[482, 538], [66, 268], [562, 922]]]
    pair = [[[251, 956], [503, 339]], [[408, 382], [251, 956],
                                       [503, 339]], [[503, 339], [251, 956], [706, 673]]]
    pair = make_locally_delaunay(pair)
    print(pair)
    # print(circle)
