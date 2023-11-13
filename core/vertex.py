import numpy as np


class Vertex:
    def __init__(self, vertex_id, axis=None):
        """
        Vertex类的构造函数
        :param vertex_id: 顶点的id
        :param axis: 顶点的坐标，默认为[0., 0., 0.]
        """
        self.vertex_id = vertex_id
        if axis is not None:
            self.axis = axis
        else:
            self.axis = [0., 0., 0.]

        # 第一、第二邻接点
        self.first_neighbors = []
        self.second_neighbors = []

        # 顶点所在的面
        self.related_faces = []

    def set_axis(self, x, y, z):
        """
        设置顶点的坐标

        :param x: x坐标
        :param y: y坐标
        :param z: z坐标
        :return:
        """
        self.axis = [x, y, z]

    def set_axis(self, axis: list):
        """
        使用列表设置顶点坐标
        :param axis: 顶点坐标
        :return:
        """
        self.axis = axis

    def add_first_neighbor(self, another_vertex):
        """
        将一阶相邻顶点添加到列表中
        :param another_vertex:
        :return:要添加为一阶相邻顶点的另一个Vertex对象。
        """
        if isinstance(another_vertex, Vertex):
            if another_vertex not in self.first_neighbors:
                self.first_neighbors.append(another_vertex)
        else:
            raise Exception("Input is not a valid Vertex object.")

    def add_second_neighbor(self, another_vertex):
        """
        将二阶邻接点添加到列表中
        :param another_vertex:要添加为二阶相邻顶点的另一个Vertex对象。
        :return:
        """
        if isinstance(another_vertex, Vertex):
            if another_vertex not in self.second_neighbors and another_vertex is not self:
                self.second_neighbors.append(another_vertex)
        else:
            raise Exception("Input is not a valid Vertex object.")

    def get_first_neighbors(self):
        """
        获取一阶相邻顶点的列表。
        :return: 一阶相邻顶点的列表。
        """
        return self.first_neighbors

    def get_second_neighbors(self):
        """
        获取二阶相邻顶点的列表。
        :return:二阶相邻顶点的列表。
        """
        return self.second_neighbors

    def get_vertex_id(self):
        """
        获取顶点ID。
        :return:顶点ID。
        """
        return self.vertex_id

    def __str__(self):
        return f'id: {self.vertex_id}, axis: {self.axis}'
