from vertex import Vertex


class Face:
    def __init__(self, face_id, location, related_vertex):
        self.id = face_id
        self.location = location
        self.related_vertex = related_vertex

    def display(self):
        print(f"Face's id: {self.id}\n"
              f"Face's location: {self.location}\n"
              f"Face's related_vertex: {self.related_vertex}")
