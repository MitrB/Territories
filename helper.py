from random import randint
from GLOBVAR import *
from enum import *
import math


class PointDistribution(Enum):
    RANDOM = 0
    GRID = 1
    SPIRAL = 2


def generate_points(N=10, point_distribution=PointDistribution.GRID):
    match point_distribution:
        case PointDistribution.RANDOM:
            points = [__generate_random_point(
                window_width, window_height) for i in range(N)]
        case PointDistribution.GRID:
            points = [(math.floor(window_width/(2*N) + i*window_width/N), math.floor(window_height/(2*N) + j*window_height/N))
                      for i in range(N) for j in range(N)]  # NxN grid TODO: might want to make N total points

    # points = __remove_duplicate_points(points)
    # points = __add_points_until_full(points, N)
    return points


def __remove_duplicate_points(points):
    unique_points = []
    for point in points:
        if point not in points:
            unique_points.append(point)

    return unique_points


def __add_points_until_full(points, N):
    while not len(points) >= N:
        random_point = __generate_random_point(window_width, window_height)
        if random_point not in points:
            points.append(random_point)
    return points


def __generate_random_point(width, height):
    return (randint(10, width - 10), randint(10, height - 10))
