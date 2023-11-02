import numpy as np


class Face:
    def __init__(self, n, face_id, related_vertices):
        self.n = n
        self.face_id = face_id
        self.related_vertices = related_vertices
        self.location = []
        for i in range(self.n):
            self.location.append(self.related_vertices[i].axis)

    # 可以删了（？
    def set_vertices(self, related_vertices):
        self.related_vertices = related_vertices

    def get_vertices_ids(self):
        return [vertex.vertex_id for vertex in self.related_vertices]

    def display(self):
        print(f"Face's id: {self.face_id}\n"
              f"Face's location: {self.location}\n"
              f"Face's related_vertices: {self.related_vertices}")
