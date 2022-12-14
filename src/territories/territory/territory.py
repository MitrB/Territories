from src.vars.GLOBVAR import *
import random


class Map():
    """Collection of Polygons"""
    # pairs are polygons that share an edge: {edge: p1, p2}

    def __init__(self, polygons):
        # all polygons that exist
        # id: Polygon class
        self.polygons = {}

        for p in polygons:
            self.polygons[p] = []

    # Todo: call Polygon function probably
    def add_neighbour(self, polygon, polygon_ne):
        neighbour_list = self.polygons[polygon]
        self.polygons[polygon] = neighbour_list + [polygon_ne]


class Polygon():
    """Mathematical presentation of a region"""

    def __init__(self, shape):
        self.neighbours = []
        self.shape = shape

    # Todo: check
    def add_neighbour(self, polygon):
        self.neighbours += [polygon]

    def __hash__(self):
        return hash(self.shape)

    def __eq__(self, other):
        return self.shape == other

    def __str__(self):
        return str(self.shape)




class Territory(Polygon):
    """A Territory is a Polygon with properties of the land it represents"""

    def __init__(self, shape):
        super().__init__(shape)

        self.type = "zone"
        # self.color = random.choice(biomes_list)
        self.color = grey

        self.food_meat = random.uniform(0, 1)
        self.food_green = random.uniform(0, 1)
        self.food_drink = random.uniform(0, 1)
        self.resource_wood = random.uniform(0, 1)
        self.resource_stone = random.uniform(0, 1)
        self.resource_minerals = random.uniform(0, 1)
        self.natural_defence = random.uniform(0, 1)
        self.natural_danger = random.uniform(0, 1)

        self.owned = False
