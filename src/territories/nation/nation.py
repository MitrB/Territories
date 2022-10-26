class Nation():
    """Agent"""

    def __init__(self, name, color):
        self.name = name
        self.color = color
        # list of populations that are part of the Nation
        self.populations = []


class Population():
    """A population is a group of people with similar properties"""

    def __init__(self, name):
        self.name = name

class NationProperties():
    """Properties of nations"""
    pass
