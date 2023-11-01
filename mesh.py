from vertex import Vertex
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

    def read_file(self, file_path):
        # 打开off文件
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # 计算顶点、边的数量
            vertices_count, faces_count, lines_count = map(int, lines[1].split())
            self.vertices_count = vertices_count
            self.faces_count = faces_count
            # self.faces_index = {face: [] for face in range(faces_count)}
            # self.vertices_index = {vertex: [] for vertex in range(vertices_count)}

            # 计算self.vertices
            vertex_id = 0
            for line in lines[2:2 + vertices_count]:
                new_vertex = Vertex(vertex_id)
                new_vertex.set_axis(list(map(float, line.split())))
                self.vertices.append(new_vertex)
                # print(f'[{self.vertices[vertex_id].x}, {self.vertices[vertex_id].y}, {self.vertices[vertex_id].z}]')
                vertex_id += 1
            # 计算self.faces和self.faces_index
            # faces = []
            face_id = 0
            for line in lines[2 + vertices_count:]:
                index = list(map(int, line.split()))
                # faces.append(index)

                # for index in faces:
                # location = faces.index(index)
                related_vertices = [self.vertices[i] for i in index[1:]]
                print(index[0], face_id, related_vertices)
                #print(type(related_vertices))
                new_face = Face(index[0], face_id, related_vertices)
                self.faces.append(new_face)
                # face = []
                # for i in index:
                #     # self.faces_index[location].append(i)
                #     face.append(self.vertices[i])
                for vertex in self.faces[face_id].related_vertices:
                    self.vertices[vertex.vertex_id].related_faces.append(new_face)
                face_id += 1
            # 计算self.vertices_index
            # for i, face in enumerate(faces):
            #     for vertex in face:
            #         self.vertices_index[vertex].append(i)
        # print(self.vertices_index)

    def find_first_neighbors(self, vertex_id):
        for face in self.faces:
            if vertex_id in face.get_vertices_ids():
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
                print(neighbors)
                self.vertices[vertex_id].add_second_neighbor(neighbor)
        print(self.vertices[vertex_id].get_second_neighbors())
