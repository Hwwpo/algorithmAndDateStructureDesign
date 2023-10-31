from mesh import Mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


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
    # 顶点数据
        # vertices = np.array(self.vertices)

    # 面的顶点数据
        # self.draw_by_step()

        # plt.show()

    def draw_by_step(self):
        faces_portion = []
        for index in range(len(self.faces)):
            faces_portion.append(self.faces[index])
            if index % 300 == 0:
                self.add_face(faces_portion, edge_color='g')
                faces_portion = []
                plt.pause(0.0001)

    def add_face(self, faces,edge_color, face_color='b'):
        collection = Poly3DCollection(faces, linewidths=1)
        collection.set_edgecolor(edge_color)
        collection.set_facecolor(face_color)
        self.ax.add_collection3d(collection)

    def draw(self):
        self.add_face(self.faces, edge_color='g')

    def draw_edge(self, point):
        face_index = self.vertices_index[point]
        faces = []
        for index in face_index:
            faces.append(self.faces[index])
        self.add_face(faces, edge_color='b', face_color='r')
        pass
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

