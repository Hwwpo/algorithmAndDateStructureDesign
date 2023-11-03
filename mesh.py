import time

import networkx as nx
from itertools import combinations

from matplotlib import pyplot as plt

from vertex import Vertex
from edge import Edge
from face import Face


class Mesh:
    def __init__(self):
        """
        self.vertices_count：该图形顶点数量\n
        self.faces_count：该图形面数量\n
        self.vertices: 返回一个数组，存储着每个点的坐标，e.g. self.vertices[0] = [0, 1, 1]\n
        self.faces: 返回一个数组，存储着每个面包含的点的坐标，e.g. self.faces[0] = [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]\n
        self.faces_index: 返回一个字典，存储着每个面包含的点的索引，e.g. self.faces_index[1] = [123, 234,345]\n
        self.vertices_index: 返回一个字典，存储着每个点被在哪些面之中，e.g. self.vertices_index[0] = [1324, 42345, 234523, 123]\n
        :param file_path: your off file path.
        """
        self.faces = []
        self.vertices = []
        self.vertices_count = 0
        self.faces_count = 0
        self.edges = []
        self.net = nx.Graph()

    def net_init(self):
        frame = [edge.nx_format for edge in self.edges]
        print(len(frame))
        self.net.add_weighted_edges_from(frame)
        # debugging
        minWPath = nx.dijkstra_path(self.net, source=0, target=10)
        lMinWPath = nx.dijkstra_path_length(self.net, source=0, target=10)
        print(minWPath)
        print(lMinWPath)
        pass

    def read_file(self, file_path):
        # 打开off文件
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # 计算顶点、边的数量
            vertices_count, faces_count, lines_count = map(int, lines[1].split())
            self.vertices_count = vertices_count
            self.faces_count = faces_count
            # 计算self.vertices
            vertex_id = 0
            for line in lines[2:2 + vertices_count]:
                new_vertex = Vertex(vertex_id)
                new_vertex.set_axis(list(map(float, line.split())))
                self.vertices.append(new_vertex)
                vertex_id += 1
            face_id = 0
            for line in lines[2 + vertices_count:]:
                index = list(map(int, line.split()))
                related_vertices = [self.vertices[i] for i in index[1:]]
                new_face = Face(index[0], face_id, related_vertices)
                self.faces.append(new_face)
                for vertex in self.faces[face_id].related_vertices:
                    self.vertices[vertex.vertex_id].related_faces.append(new_face)
                face_id += 1

    def find_first_neighbors(self, vertex_id):
        for face in self.vertices[vertex_id].related_faces:
            for i in range(face.n):
                curr_vertex = face.related_vertices[i]
                next_vertex = face.related_vertices[(i + 1) % face.n]
                last_vertex = face.related_vertices[(i + face.n - 1) % face.n]
                curr_vertex.add_first_neighbor(next_vertex)
                curr_vertex.add_first_neighbor(last_vertex)

    def find_all_first_neighbors(self):
        for face in self.faces:
            # print(face.vertices[0].x)
            for i in range(face.n):
                curr_vertex = face.related_vertices[i]
                next_vertex = face.related_vertices[(i + 1) % face.n]
                last_vertex = face.related_vertices[(i + face.n - 1) % face.n]
                curr_vertex.add_first_neighbor(next_vertex)
                curr_vertex.add_first_neighbor(last_vertex)

    # 感觉时间复杂度有点高
    def find_second_neighbors(self, vertex_id):
        if not self.vertices[vertex_id].get_first_neighbors():
            self.find_first_neighbors(vertex_id)
        first_neighbors = self.vertices[vertex_id].get_first_neighbors()
        neighbors = []
        for first_neighbor in first_neighbors:
            self.find_first_neighbors(first_neighbor.get_vertex_id())
            neighbors.extend(first_neighbor.get_first_neighbors())
        for neighbor in neighbors:
            if neighbor not in first_neighbors:
                self.vertices[vertex_id].add_second_neighbor(neighbor)

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]

    def edges_init(self):
        dictionary = {}
        for face in self.faces:
            vertex_ids = [vertex.vertex_id for vertex in face.related_vertices]
            combines = list(combinations(vertex_ids, 2))
            for combine in combines:
                vertex1 = self.get_vertex(combine[0])
                vertex2 = self.get_vertex(combine[1])
                new_edge = Edge((vertex1, vertex2))
                vertices = new_edge.vertices
                try:
                    a = dictionary[vertices]
                    continue
                except:
                    dictionary[vertices] = True
                    dictionary[vertices[::-1]] = True
                    self.edges.append(new_edge)
                # print(self.edges)
                # time.sleep(10)

