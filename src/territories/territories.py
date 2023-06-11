from src.territories.territory.territory import *
from src.territories.nation.nation import *
from src.math_functions.precalc import *
from src.gui.gui import draw_territories, setup_tk, start_tk_loop
from src.math_functions.math_functions import *
from src.vars.logging_settings import config_logging
import pickle
import random
import sys

possible_args = ["-p", "-s", "-l", "-d"]


def main(args=sys.argv):
    N = 500
    save_points = False
    load_points = False

    for i, a in enumerate(args):
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

    full_map = Map(triangle_territories)

    for pair in pairs.values():
        for t in triangle_territories:
            if t.shape == pair[0]:
                for t2 in triangle_territories:
                    if t2.shape == pair[1]:
                        full_map.add_neighbour(t, t2)
                        full_map.add_neighbour(t2, t)

    # gui
    (root, display) = setup_tk()

    file_name = 'nation_names.txt'
    with open(f'./Data/{file_name}') as names_file:
        lines = names_file.readlines()
        name = random.choice(lines)
        nation = Nation(name, "#FF0000", full_map, display)
        add_random_territory_to_nation(full_map, nation, root)
        nation.add_random_territory()

        nation2 = Nation(name, "#00FF00", full_map, display)
        add_random_territory_to_nation(full_map, nation2, root)
        nation2.add_random_territory()

    draw_territories(display, full_map)
    # display.add_label(points)
    start_tk_loop(root)


def add_random_territory_to_nation(full_map, nation, root):
    random_territory = random.choice(list(full_map.polygons.keys()))
    nation.add_territory_to_owned(random_territory)


if __name__ == "__main__":
    config_logging()
    main([])
