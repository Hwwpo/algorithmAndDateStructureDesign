import numpy as np


class Face:
    def __init__(self, n: int, face_id: int, related_vertices: list):
        """
        面类\n
        self.location: 面的坐标
        :param n: 面的顶点数
        :param face_id: 面分配的id
        :param related_vertices: 面的顶点
        """
        self.n = n
        self.face_id = face_id
        self.related_vertices = related_vertices
        self.location = []
        for i in range(self.n):
            self.location.append(self.related_vertices[i].axis)

    def __str__(self):
        return f"Face's id: {self.face_id}\n" \
              f"Face's location: {self.location}\n" \
              f"Face's related_vertices: {self.related_vertices}"
