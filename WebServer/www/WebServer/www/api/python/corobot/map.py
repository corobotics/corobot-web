"""This module represents the map for use in navigation.

Authors: Z. Butler, M. Bogue

"""
from collections import namedtuple

class Map():

    Node = namedtuple("Node", "name, x, y, neighbors")

    def __init__(self, mapFile):
        self.nodes = {}
        with open(mapFile) as f:
            f.next() # skip the first line
            for line in f:
                parts = line.split(",")
                name = parts[0]
                x, y = float(parts[3]), float(parts[4])
                neighbors = parts[6:]
                self.nodes[name] = Node(name, x, y, neighbors)

    def get_closest_node(self, pos):
        """Return the name of the closest node to the given position."""
        min_dist = float('+infinity')
        closest = None
        for name, x, y, _ in self.nodes.values():
            dx = pos.x - x
            dy = pos.y - y
            # Just use square distance since we're only comparing them.
            dist = dx * dx + dy * dy
            if dist < min_dist:
                min_dist = dist
                closest = name
        return closest

    def get_node_names(self):
        """Returns names of all nodes in the map."""
        return self.nodes.keys()

    def get_node(self, name):
        """Returns a Map.Node object for the given name."""
        return self.nodes[name.upper()]

    def is_node(name):
        """Returns whether the given name represents a node in the map."""
        return name.upper() in self.nodes
