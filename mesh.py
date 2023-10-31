class Mesh:
    def __init__(self, file_path):
        self.vertices = []
        self.faces = []

        with open(file_path, 'r') as file:
            lines = file.readlines()
            # print(lines[1])
            vertices_count, faces_count, _ = map(int, lines[1].split())
            # print(vertices_count)
            # print(faces_count)
            self.faces_index = {face: [] for face in range(faces_count)}
            self.vertices_index = {vertex: [] for vertex in range(vertices_count)}
            for line in lines[2:2 + vertices_count]:
                vertex = list(map(float, line.split()))
                self.vertices.append(vertex)

            count = 0
            faces = []
            for line in lines[2 + vertices_count:]:
                index = list(map(int, line.split()))[1:]
                faces.append(index)
                face = []
                for i in index:
                    self.faces_index[count].append(i)
                    face.append(self.vertices[i])
                count += 1
                self.faces.append(face)

            for i, face in enumerate(faces):
                for vertex in face:
                    self.vertices_index[vertex].append(i)
        # print(self.vertices_index)


