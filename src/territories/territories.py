from .territory.territory import *
from src.gui.helper import *
from src.gui.gui import draw_territories
from src.math_functions.math_functions import *


# create teritorries

def main():
    # get triangles
    N = 250
    points = generate_points(N)
    triangles = calculate_pbp_triangulation(points.copy())
    triangles = calculate_delaunay(triangles)

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
