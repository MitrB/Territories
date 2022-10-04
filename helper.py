from random import randint
from GLOBVAR import * 

def generate_points():
    N = randint(8, 50)
    # N = 10
    points = [[randint(0, window_width - 10), randint(0, window_height - 10)]
              for i in range(N)]
    return points
