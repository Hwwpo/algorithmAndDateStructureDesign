import math


class Edge:
    def __init__(self, vertices: tuple):
        self.vertices = vertices
        # print(self.vertices)
        self.vertices_by_id = tuple([vertex.vertex_id for vertex in self.vertices])
        # print(self.vertices_by_id)
        self.weight = 0.
        self.calculate_weight()
        self.nx_format = (self.vertices_by_id[0], self.vertices_by_id[1], self.weight)
        # print(self.nx_format)

    def calculate_weight(self):
        self.weight = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(self.vertices[0].axis, self.vertices[1].axis)))

    def __str__(self):
        return (f"It's a Edge class:"
                f"self.vertices: {self.vertices}"
                f"self.nx_format: {self.nx_format}")