from random import randint
from GLOBVAR import *


def generate_points(N=10):
    points = [ __generate_random_point(window_width, window_height) for i in range(N)]
    points = __remove_duplicate_points(points)
    points = __add_points_until_full(points, N)
    return points


def __remove_duplicate_points(points):
    unique_points = []
    for point in points:
        if point not in points:
            unique_points.append(point)

    return unique_points


def __add_points_until_full(points, N):
    while len(points) != N:
        random_point = __generate_random_point(window_width, window_height)
        if random_point not in points:
            points.append(random_point)
    return points

def __generate_random_point(width, height):
    return (randint(10, width - 10), (10, height - 10))
