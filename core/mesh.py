from typing import Tuple, Any

import networkx as nx
from itertools import combinations
from core.vertex import Vertex
from core.edge import Edge
from core.face import Face


class Mesh:
    def __init__(self):
        """
        self.vertices_count：该图形顶点数量\n
        self.faces_count：该图形面数量\n
        self.vertices: 返回vertex数组，为顶点集合\n
        self.faces: 返回face数组，为面集合\n
        self.edges: 返回edge数组，为边集合\n
        self.max_lim: 坐标的最大值
        self.min_lim: 坐标的最小值
        self.net: 存储图结构
        """
        self.vertices_count = 0
        self.faces_count = 0
        self.faces = []
        self.vertices = []
        self.edges = []
        self.max_lim = -1e6
        self.min_lim = 1e6
        self.net = nx.Graph()

    def __edges_init__(self):
        """
        边初始化函数
        :return: None
        """
        # 使用字典判重
        dictionary = {}

        # 遍历每一个面
        for face in self.faces:
            vertex_ids = [vertex.vertex_id for vertex in face.related_vertices]

            # 将每个面的点两两排列组合
            combines = list(combinations(vertex_ids, 2))

            # 遍历组合
            for combine in combines:
                vertex1 = self.get_vertex(combine[0])
                vertex2 = self.get_vertex(combine[1])
                vertices = (vertex1, vertex2)

                # 判重，(1, 2)和(2, 1)属于同一条边，并且多个面可能共用一条边
                try:
                    a = dictionary[vertices]
                    continue
                except:
                    dictionary[vertices] = True
                    dictionary[vertices[::-1]] = True
                    # 无重复则添加新边
                    new_edge = Edge((vertex1, vertex2))
                    self.edges.append(new_edge)

    def __net_init__(self):
        """
        图网络的初始化函数
        :return: None
        """
        frame = [edge.nx_format for edge in self.edges]
        self.net.add_weighted_edges_from(frame)

    def dijkstra(self, start: int, end: int) -> tuple[Any, Any]:
        """
        Dijkstra求最短路
        :param start: 开始节点的vertex_id
        :param end: 结束节点的vertex_id
        :return: 返回最短距离和最短路径
        """
        # 创建一个字典来保存每个节点的最短距离
        shortest_distances = {node: float('infinity') for node in self.net.nodes}
        shortest_distances[start] = 0

        # 创建一个字典来保存最短路径
        shortest_paths = {node: [] for node in self.net.nodes}
        shortest_paths[start] = [start]

        # 创建一个集合来保存已经访问过的节点
        visited_nodes = set()

        while True:
            # 从未访问过的节点中找到距离最短的节点
            min_distance_node = None
            for node in self.net.nodes:
                if node not in visited_nodes:
                    if min_distance_node is None:
                        min_distance_node = node
                    elif shortest_distances[node] < shortest_distances[min_distance_node]:
                        min_distance_node = node

            # 如果我们没有找到一个新的节点，那么我们已经完成了所有的访问
            if min_distance_node is None:
                break

            # 否则，我们将这个节点添加到已访问过的节点的集合中
            visited_nodes.add(min_distance_node)

            # 然后，我们更新所有相邻节点的最短距离
            for neighbour, properties in self.net[min_distance_node].items():
                distance = properties['weight']
                new_distance = shortest_distances[min_distance_node] + distance
                if new_distance < shortest_distances[neighbour]:
                    shortest_distances[neighbour] = new_distance
                    shortest_paths[neighbour] = shortest_paths[min_distance_node] + [neighbour]

        # 最后，我们返回到目标节点的最短距离和最短路径
        return shortest_distances[end], shortest_paths[end]

    def read_file(self, file_path: str):
        """
        读文件，初始化属性
        :param file_path: 文件路径
        :return: None
        """
        # 打开off文件

        with open(file_path, 'r') as file:
            lines = file.readlines()

            # 从0开始分配ID
            vertex_id = 0
            face_id = 0
            vertices_count = 0
            faces_count = 0
            is_vertex_section = False
            for line in lines:

                # 如果是以 "#" 开头的行，则跳过，将其视为注释
                if line.startswith('#'):
                    continue

                if line.startswith('OFF'):
                    continue

                # 空行跳过
                if len(line) == 0:
                    continue

                if not is_vertex_section:

                    # 获得顶点、边的数量
                    vertices_count, faces_count, _ = map(int, line.split())
                    self.vertices_count = vertices_count
                    self.faces_count = faces_count
                    is_vertex_section = True
                else:
                    # 还在添加顶点
                    if vertices_count > 0:

                        # 新建顶点
                        new_vertex = Vertex(vertex_id)

                        # 计算坐标
                        new_vertex.set_axis(list(map(float, line.split())))

                        # 计算3D图的坐标范围，切换全局视角时需要使用
                        max_lim = max(new_vertex.axis)
                        min_lim = min(new_vertex.axis)
                        if self.max_lim < max_lim:
                            self.max_lim = max_lim
                        if self.min_lim > min_lim:
                            self.min_lim = min_lim

                        # 添加新顶点
                        self.vertices.append(new_vertex)
                        vertex_id += 1
                        vertices_count -= 1

                    # 顶点添加结束，添加面
                    elif faces_count > 0:

                        # 计算相关参数
                        index = list(map(int, line.split()))
                        related_vertices = [self.vertices[i] for i in index[1:]]

                        # 添加新面
                        new_face = Face(index[0], face_id, related_vertices)
                        self.faces.append(new_face)

                        # 将面的属性也添加到其关联的点中
                        for vertex in self.faces[face_id].related_vertices:
                            self.vertices[vertex.vertex_id].related_faces.append(new_face)

                        # 下一个面
                        face_id += 1
                        faces_count -= 1

    def find_first_neighbors(self, vertex_id):
        for face in self.vertices[vertex_id].related_faces:
            for i in range(face.n):
                curr_vertex = face.related_vertices[i]
                if curr_vertex.get_vertex_id() == vertex_id:
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
        """
        通过id获得对应的vertex类
        :param vertex_id:
        :return:
        """
        return self.vertices[vertex_id]

