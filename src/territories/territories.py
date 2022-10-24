from src.territories.territory.territory import *
from src.math_functions.precalc import *
from src.gui.gui import draw_territories
from src.math_functions.math_functions import *
import pickle
import sys

possible_args = ["-p","-s","-l"]


def main(args=sys.argv):
    N = 850
    save_points = False
    load_points = False

    for i in range(len(args)):
        if args[i] == "-p":
            N = int(args[i+1])
        elif args[i] == "-s":
            save_points = True
        elif args[i] == "-l":
            load_points = True

    if load_points:
        with open("points", "rb") as fp:
            points = pickle.load(fp)
    else:
        try:
            points = generate_points(N)
        except ():
            print("Points should be a number.")
            exit(1)

    if save_points:
        with open("points", "wb") as fp:
         pickle.dump(points, fp)


    # triangles = generate_generic_triangulisation(points.copy())
    triangles = generate_delauny_triangulisation(points)

    pairs = calculate_triangle_pairs(triangles)

    triangle_territories = []

    for t in triangles:
        t = Territory(t)
        triangle_territories.append(t)

    territories = Map(triangle_territories)

    for pair in pairs.values():
        territories.add_neighbour(pair[0], pair[1])
        territories.add_neighbour(pair[1], pair[0])

    # gui
    draw_territories(territories)
