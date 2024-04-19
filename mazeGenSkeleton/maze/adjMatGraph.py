# ------------------------------------------------------------------------
# Please COMPLETE the IMPLEMENTATION of this class.
# Adjacent matrix implementation.
#
# __author__ = 'Jeffrey Chan', 'Mashuk Arefin Pranjol'
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List

from maze.util import Coordinates
from maze.graph import Graph

# Define the AdjMatGraph class that inherits from the Graph class
class AdjMatGraph(Graph):
    # Constructor to initialize graph with number of rows and columns
    def __init__(self, rowNum, colNum):
        # Store the number of rows in the graph
        self.rowNum = rowNum
        # Store the number of columns in the graph
        self.colNum = colNum
        # Initialize an empty matrix using dictionary of dictionaries for representing the adjacency matrix
        self.matrix = {
            (r, c): {} for r in range(-1, rowNum + 1) for c in range(-1, colNum + 1)
        }

    # Method to add a single vertex to the adjacency matrix
    def addVertex(self, label: Coordinates):
        # Initialize the vertex with an empty dictionary if it's not already present
        if label not in self.matrix:
            self.matrix[label] = {}

    # Method to add multiple vertices to the adjacency matrix
    def addVertices(self, vertLabels: List[Coordinates]):
        # Iterate through each label in the list and add it using addVertex method
        for label in vertLabels:
            self.addVertex(label)

    # Method to add an edge between two vertices
    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False):
        # Check if both vertices exist in the matrix
        if vert1 in self.matrix and vert2 in self.matrix:
            # Set the wall status for both directions
            self.matrix[vert1][vert2] = addWall
            self.matrix[vert2][vert1] = addWall
            return True
        return False

    # Method to update the wall status between two vertices
    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool):
        # Check if both vertices exist in the matrix
        if vert1 in self.matrix and vert2 in self.matrix:
            # Updates the wall status for both directions
            self.matrix[vert1][vert2] = wallStatus
            self.matrix[vert2][vert1] = wallStatus
            return True
        return False

    # Method to remove an edge between two vertices 
    def removeEdge(self, vert1: Coordinates, vert2: Coordinates):
        # Check if both vertices exist and there is an edge to remove
        if vert1 in self.matrix and vert2 in self.matrix and vert2 in self.matrix[vert1]:
            # Remove the edge from both vertices
            del self.matrix[vert1][vert2]
            del self.matrix[vert2][vert1]
            return True
        return False

    # Method to check if a vertex exists in the graph
    def hasVertex(self, label: Coordinates):
        return label in self.matrix

    # Method to check if an edge exists between two vertices
    def hasEdge(self, vert1: Coordinates, vert2: Coordinates):
        return vert2 in self.matrix.get(vert1, {})

    # Method to retrieve the wall status between two vertices
    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates):
        return self.matrix.get(vert1, {}).get(vert2, False)

    # Method to list all neighbors for a given vertex
    def neighbours(self, label: Coordinates):
        return list(self.matrix.get(label, {}).keys())
