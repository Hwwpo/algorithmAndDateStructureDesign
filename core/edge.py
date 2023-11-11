import math


class Edge:
    def __init__(self, vertices: tuple):
        """
        边类\n
        self.vertices: 边的节点
        self.vertices_by_id: 节点的坐标
        self.weight: 边权
        self.nx_format: 存入nx的Graph中使用的结构
        :param vertices: 两个节点组成的tuple
        """
        self.vertices = vertices
        self.vertices_by_id = tuple([vertex.vertex_id for vertex in self.vertices])
        self.weight = 0.
        self.calculate_weight()
        self.nx_format = (self.vertices_by_id[0], self.vertices_by_id[1], self.weight)

    def calculate_weight(self):
        """
        计算边权
        :return:
        """
        self.weight = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(self.vertices[0].axis, self.vertices[1].axis)))

    def __str__(self):
        return (f"It's a Edge class:"
                f"self.vertices: {self.vertices}"
                f"self.nx_format: {self.nx_format}")