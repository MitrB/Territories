from dataclasses import dataclass
from random import choice


class Nation():
    """Agent"""

    def __init__(self, name, color, map, display):
        self.name = name
        self.color = color

        self.properties = NationProperties(1.)
        self.territory_owned = []
        self.map = map

        self.display = display

        # Extra feature
        # list of populations that are part of the Nation
        # self.populations = []

    def find_adjacent_territory(self):
        adjacent = []
        for t in self.territory_owned:
            for n in self.map.polygons[t]:
                if n not in self.territory_owned and n not in adjacent:
                    adjacent.append(n)

        return adjacent

    def add_territory_to_owned(self, territory):
        adj = self.find_adjacent_territory()
        if territory not in self.territory_owned and (territory in adj or adj == []) and not territory.owned:
            self.territory_owned.append(territory)
            territory.color = self.color
            territory.owned = True

    def add_random_territory(self):
        territory = choice(self.find_adjacent_territory())
        self.add_territory_to_owned(territory)
        self.display.drawTriangle(territory.shape, self.color)
        self.display.after(100, self.add_random_territory)


class Population():
    """A population is a group of people with similar properties"""

    def __init__(self, name):
        self.name = name


@dataclass()
class NationProperties():
    """Properties of nations"""
    property1: float
