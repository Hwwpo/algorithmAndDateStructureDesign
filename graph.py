from mesh import Mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
FPS = 300


# hold_on之后不允许进行图像的修改，
def hold_on():
    plt.show()


class Graph(Mesh):
    def __init__(self):
        super().__init__('Bunny.off')
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

    def draw_by_step(self):
        faces_portion = []
        for index in range(len(self.faces)):
            faces_portion.append(self.faces[index].location)
            if index % FPS == 0:
                self.add_face(faces_portion, edge_color='g')
                faces_portion = []
                plt.pause(0.0001)

    def add_face(self, faces, edge_color, face_color='b', alpha=1):
        collection = Poly3DCollection(faces, linewidths=1)
        collection.set_edgecolor(edge_color)
        collection.set_facecolor(face_color)
        collection.set_alpha(alpha=alpha)
        self.ax.add_collection3d(collection)

    def draw_by_one_step(self):
        faces_location = [face.location for face in self.faces]
        self.add_face(faces_location, edge_color='g')

    def draw_edge(self, point):
        vertex = [i for i in self.vertices if i.id == point][0]
        print(vertex)
        faces = [face.location for face in vertex.related_face]
        print(faces)
        # face_index = self.vertices_index[point]
        # # debugging
        # print(face_index)
        # faces = [self.faces[index] for index in face_index]
        self.add_face(faces, edge_color='r', alpha=1)
        pass

    def get_adjacent_point(self, point):
        face_index = self.vertices_index[point]
        vertices = [self.faces_index[index] for index in face_index]
        vertices = list(map(lambda x: x.pop(x.index(point)), vertices))

        print(vertices)

    def add_comment(self, point, text='·', color='r'):
        assistant_points = [
            [x, y, z]
            for x in range(2)
            for y in range(2)
            for z in range(2)
        ]
        location = self.vertices[point]
        px, py, pz = location
        print(location)
        # self.ax.scatter(location[0], location[1], location[2])
        self.ax.text(px, py, pz, text, color=color)
        for assistant_point in assistant_points:
            xs, ys, zs = list(zip(assistant_point, location))
            print(xs)
            self.ax.plot(xs, ys, zs, color='r')
        # self.ax.text(location[0], location[1], location[2], text,color)
        # self.ax.plot([beg[0], end[0]], [beg[1], end[1]], [beg[2], end[2]], color='r', linewidth=10.0)

        # plt.show()
        # colors = ['w'] * len(faces)
        # collection.set_edgecolor(colors)
        # collection.set_facecolor('white')

        # def update(frame):
        #     colors[frame] = 'r'
        #     collection.set_edgecolor(colors)
        #     return collection,

        # anim = FuncAnimation(self.fig, update, frames=len(faces), blit=False, interval=100)
        # anim.save("a.gif")
    # 改变边的颜色并显示动画
    #     for i in range(len(faces)):  # 设置所有边为黑色
    #         colors[i] = 'r'  # 更改特定边的颜色为红色
    #         collection.set_edgecolor(colors)
    #         plt.pause(0.01)  # 显示0.5秒的间隔
