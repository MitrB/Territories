from src.territories.territory.territory import *
from src.math_functions.precalc import *
from src.gui.gui import draw_territories, setup_tk, start_tk_loop
from src.math_functions.math_functions import *
from src.vars.logging_settings import config_logging
import pickle
import sys

possible_args = ["-p", "-s", "-l", "-d"]


def main(args=sys.argv):
    N = 200
    save_points = False
    load_points = False

    for i,a in enumerate(args):
        if a == "-p":
            N = int(args[i+1])
        elif a == "-s":
            save_points = True
        elif a == "-l":
            load_points = True
        elif a == "-d":
            config_logging()

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
    (root, display) = setup_tk()
    draw_territories(display, territories)
    # display.add_label(points)
    start_tk_loop(root)


if __name__ == "__main__":
    config_logging()
    main([])
