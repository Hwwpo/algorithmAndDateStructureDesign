import numpy as np


class Vertex:
    def __init__(self, vertex_id, axis=None):
        self.vertex_id = vertex_id
        if axis is not None:
            self.axis = axis
        else:
            self.axis = [0., 0., 0.]
        self.first_neighbors = []
        self.second_neighbors = []
        self.related_faces = []

    def set_axis(self, x, y, z):
        self.axis = [x, y, z]

    def set_axis(self, axis):
        self.axis = axis

    def add_first_neighbor(self, another_vertex):
        if isinstance(another_vertex, Vertex):
            if another_vertex not in self.first_neighbors:
                self.first_neighbors.append(another_vertex)
        else:
            raise Exception("Input is not a valid Vertex object.")

    def add_second_neighbor(self, another_vertex):
        if isinstance(another_vertex, Vertex):
            if another_vertex not in self.second_neighbors and another_vertex is not self:
                self.second_neighbors.append(another_vertex)
        else:
            raise Exception("Input is not a valid Vertex object.")

    def get_first_neighbors(self):
        return self.first_neighbors

    def get_second_neighbors(self):
        return self.second_neighbors

    def get_vertex_id(self):
        return self.vertex_id

    def __str__(self):
        return f'id: {self.vertex_id}, axis: {self.axis}'

    def display(self):
        print(f"Vertex's id: {self.vertex_id}\n"
              f"Vertex's axis: {self.axis}\n"
              f"Vertex's related_face: {self.related_face}"
              )
