class Mesh:
    def __init__(self, file_path):
        """
        self.vertices_count：该图形顶点数量\n
        self.faces_count：该图形面数量\n
        self.vertices: 返回一个数组，存储着每个点的坐标，e.g. self.vertices[0] = [0, 1, 1]\n
        self.faces: 返回一个数组，存储着每个面包含的点的坐标，e.g. self.faces[0] = [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]\n
        self.faces_index: 返回一个字典，存储着每个面包含的点的索引，e.g. self.faces_index[1] = [123, 234,345]\n
        self.vertices_index: 返回一个字典，存储着每个点被在哪些面之中，e.g. self.vertices_index[0] = [1324, 42345, 234523, 123]\n
        :param file_path: your off file path.
        """
        # 打开off文件
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # 计算顶点、边的数量
            vertices_count, faces_count, _ = map(int, lines[1].split())
            self.vertices_count = vertices_count
            self.faces_count = faces_count
            # 初始化数据
            self.vertices = []
            self.faces = []
            self.faces_index = {face: [] for face in range(faces_count)}
            self.vertices_index = {vertex: [] for vertex in range(vertices_count)}

            # 计算self.vertices
            for line in lines[2:2 + vertices_count]:
                vertex = list(map(float, line.split()))
                self.vertices.append(vertex)
            # 计算self.faces和self.faces_index
            faces = []
            for line in lines[2 + vertices_count:]:
                index = list(map(int, line.split()))[1:]
                faces.append(index)

            for index in faces:
                location = faces.index(index)
                face = []
                for i in index:
                    self.faces_index[location].append(i)
                    face.append(self.vertices[i])
                self.faces.append(face)
            # 计算self.vertices_index
            for i, face in enumerate(faces):
                for vertex in face:
                    self.vertices_index[vertex].append(i)
        # print(self.vertices_index)


