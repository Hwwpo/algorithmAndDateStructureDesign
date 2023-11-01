class Vertex:
    def __init__(self, vertex_id, xyz):
        self.id = vertex_id
        self.xyz = xyz
        self.related_face = []

    def display(self):
        print(f"Vertex's id: {self.id}\n"
              f"Vertex's xyz: {self.xyz}\n"
              f"Vertex's related_face: {self.related_face}"
              )
