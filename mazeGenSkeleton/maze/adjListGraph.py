# ------------------------------------------------------------------------
# Please COMPLETE the IMPLEMENTATION of this class.
# Adjacent list implementation.
#
# __author__ = 'Jeffrey Chan', 'Mashuk Arefin Pranjol'
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List

from maze.util import Coordinates
from maze.graph import Graph

# Define the AdjListGraph class that inherits from the Graph class
class AdjListGraph(Graph):
    # Constructor to initialize the graph with the number of rows and columns
    def __init__(self, rowNum, colNum):
        # Store the number of rows
        self.rowNum = rowNum
        # Store the number of columns
        self.colNum = colNum
        # Initialize the adjacency list that will hold vertices and their neighbors
        self.adjList = {
            (r, c): set() for r in range(-1, rowNum + 1) for c in range(-1, colNum + 1)
        }

    # Method to add a single vertex to the adjacency list
    def addVertex(self, label: Coordinates):
        # Add the vertex if it's not already in the adjacency list
        if label not in self.adjList:
            self.adjList[label] = set()

    # Method to add multiple vertices to the adjacency list
    def addVertices(self, vertLabels: List[Coordinates]):
        # Loop through the list of vertex labels and add each one
        for label in vertLabels:
            self.addVertex(label)

    # Method to add an edge between two vertices
    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False):
        # Check if both vertices are in the graph
        if vert1 in self.adjList and vert2 in self.adjList:
            # Add the edge in both directions
            self.adjList[vert1].add((vert2, addWall))
            self.adjList[vert2].add((vert1, addWall))
            return True
        return False

    # Method to update the status of a wall between two vertices
    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool):
        # Check if both vertices exist in the adjacency list
        if vert1 in self.adjList and vert2 in self.adjList:
            # Find and remove the existing wall status
            pairs1 = {(v, w) for v, w in self.adjList[vert1] if v == vert2}
            pairs2 = {(v, w) for v, w in self.adjList[vert2] if v == vert1}
            self.adjList[vert1] -= pairs1
            self.adjList[vert2] -= pairs2
            # Add the updated wall status
            self.adjList[vert1].add((vert2, wallStatus))
            self.adjList[vert2].add((vert1, wallStatus))
            return True
        return False

    # Method to remove an edge between two vertices
    def removeEdge(self, vert1: Coordinates, vert2: Coordinates):
        success = False
        # Check if both vertices are in the adjacency list
        if vert1 in self.adjList and vert2 in self.adjList:
            success |= {(vert2, w) for w in [True, False]} <= self.adjList[vert1]
            success |= {(vert1, w) for w in [True, False]} <= self.adjList[vert2]
            # Remove the edge from both directions
            self.adjList[vert1] = {(v, w) for v, w in self.adjList[vert1] if v != vert2}
            self.adjList[vert2] = {(v, w) for v, w in self.adjList[vert2] if v != vert1}
        return success

    # Method to check if a vertex exists in the graph
    def hasVertex(self, label: Coordinates):
        return label in self.adjList

    # Method to check if an edge exists between two vertices
    def hasEdge(self, vert1: Coordinates, vert2: Coordinates):
        return any(v == vert2 for v, _ in self.adjList.get(vert1, set()))

    # Method to check the status of a wall between two vertices
    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates):
        return any(v == vert2 and w for v, w in self.adjList.get(vert1, set()))

    # Method to get the neighbors of a vertex
    def neighbours(self, label: Coordinates):
        return [v for v, _ in self.adjList.get(label, set())]
