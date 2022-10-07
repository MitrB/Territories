from random import randint
from GLOBVAR import * 

def generate_points(N=10):
    generated_points = [(randint(0, window_width - 10), randint(0, window_height - 10))
              for i in range(N)]


    # No duplicates
    points = []
    for point in generated_points:
        if point not in points:
            points.append(point)

    return points
