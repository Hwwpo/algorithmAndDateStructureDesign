from collections import deque
from edge import Edge
from face import Face
from mesh import Mesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from vertex import Vertex
import matplotlib.pyplot as plt
import time
# 逐步画图帧数
FPS = 300
# 坐标轴展示设置
AXIS_SHOW = 'off'
FIRST_NEIGHBOR_COLOR = 'r'
SECOND_NEIGHBOR_COLOR = 'y'


def hold_on():
    """
    图像展示，hold_on之后不允许进行图像的修改
    :return: None
    """
    plt.show()


class Graph(Mesh):
    def __init__(self):
        """
        self.ax: 存储绘图内容
        """
        super().__init__()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        plt.axis(AXIS_SHOW)
        self.ax.view_init(elev=-87, azim=-95)

    def read_file(self, file_path: str) -> None:
        """
        读文件，根据文件内容初始化属性
        :param file_path: 文件路径
        :return: None
        """
        super(Graph, self).read_file(file_path)
        self.__edges_init__()
        self.__net_init__()
        self.find_all_first_neighbors()

    def get_faces_seq(self, vertices: list) -> list:
        """
        根据所给的点的顺序得到面的顺序
        :param vertices: 顶点数组
        :return: 返回绘制的面的顺序
        """
        # 使用字典判断重复边
        appended = [False] * self.faces_count
        # 存储生成的面的集合
        faces = []
        for vertex in vertices:
            related_face = vertex.related_faces
            for face in related_face:
                if not appended[face.face_id]:
                    faces.append(face)
                    appended[face.face_id] = True
        return faces

    def add_face(self, faces: list, edge_color: str, face_color='b', alpha=1, line_width=0.5, z_order=1) -> None:
        """
        将面的绘制到窗口中
        :param faces: 面的集合，一个面为：[[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]
        :param edge_color: 面的边颜色
        :param face_color: 面的颜色
        :param alpha: 面不透明度
        :param line_width: 线宽
        :param z_order: 图层优先级
        :return: None
        """
        collection = Poly3DCollection(faces, linewidths=1)
        collection.set_edgecolor(edge_color)
        collection.set_facecolor(face_color)
        collection.set_linewidth(line_width)
        collection.set_alpha(alpha=alpha)
        collection.set_zorder(z_order)
        self.ax.add_collection3d(collection)

    def draw_by_one_step(self) -> None:
        """
        直接画出图，无动态过程
        :return: None
        """
        faces_location = [face.location for face in self.faces]
        self.add_face(faces_location, edge_color='g')

    # 已使用直接画边的方式画邻接点
    # def draw_adjacent_face(self, point, color='r', z_order=1):
    #     vertex = self.get_vertex(vertex_id=point)
    #     print(vertex)
    #     faces = [face.location for face in vertex.related_faces]
    #     print(faces)
    #     # face_index = self.vertices_index[point]
    #     # # debugging
    #     # print(face_index)
    #     # faces = [self.faces[index] for index in face_index]
    #     self.add_face(faces, edge_color=color, alpha=1, face_color='g', z_order=z_order)
    #     pass

    def draw_neighbors(self, vertex_id: int) -> None:
        """
        绘制出指定点的第一邻接点和第二邻接点，使用不同颜色标注
        :param vertex_id: 顶点的id
        :return: None
        """
        vertex = self.vertices[vertex_id]
        # self.highlight_point(vertex_id, color='w')
        self.find_second_neighbors(vertex_id)
        for first_neighbor in vertex.get_first_neighbors():
            self.draw_edge(beg=vertex, end=first_neighbor, color=FIRST_NEIGHBOR_COLOR)
            for second_neighbor in first_neighbor.get_first_neighbors():
                if second_neighbor in vertex.get_second_neighbors():
                    self.draw_edge(beg=first_neighbor, end=second_neighbor, color=SECOND_NEIGHBOR_COLOR)
        self.draw_by_one_step()
        # print(vertex)
        # for neighbor in first_neighbors:
        #     self.draw_adjacent_face(neighbor.get_vertex_id(), z_order=10)

    # 高亮一个点，有bug，待修复
    # def highlight_point(self, vertex_id: int, color: str):
    #     vertex = self.vertices[vertex_id]
    #     xs, ys, zs = vertex.axis
    #     print(xs, ys, zs)
    #     self.ax.scatter(xs, ys, zs, color=color, zorder=11)

    def mark_point(self, vertex_id: int, text=None, color='y') -> None:
        """
        在点的附近添加注释
        :param vertex_id: 点的id
        :param text: 标注的内容，默认为点的id
        :param color: 标注的颜色
        :return: None
        """
        if not text:
            text = str(vertex_id)
        location = self.get_vertex(vertex_id).axis
        px, py, pz = location
        # print(location)
        # self.ax.scatter(location[0], location[1], location[2])
        self.ax.text(px, py, pz, text, color=color, zorder=10)

    def draw_edge(self, edge: Edge, color='r', z_order=10) -> None:
        """
        在窗口上绘制一条边
        :param edge: 需要画的边
        :param color: 线的颜色
        :param z_order: 图层优先级，建议保持默认
        :return: None
        """
        beg, end = edge.vertices
        xs, ys, zs = list(zip(beg.axis, end.axis))
        self.ax.plot(xs, ys, zs, color=color, zorder=z_order)

    def draw_edge(self, beg: Vertex, end: Vertex, color='r', z_order=10) -> None:
        """
        从起点到终点画一条边
        :param beg: 边的起点
        :param end: 边的终点
        :param color: 边的颜色
        :param z_order: 图层优先级，建议保持默认
        :return: None
        """
        xs, ys, zs = list(zip(beg.axis, end.axis))
        self.ax.plot(xs, ys, zs, color=color, zorder=z_order)

    def iterative_dfs(self, start_id):
        # self.find_all_first_neighbors()
        visited = [False] * self.vertices_count
        stack = []
        dfs_sequence = []

        stack.append(self.get_vertex(start_id))

        while stack:
            node = stack.pop()
            node_id = node.get_vertex_id()

            if not node.get_first_neighbors():
                self.find_first_neighbors(node_id)
            if not visited[node_id]:
                visited[node_id] = True
                dfs_sequence.append(node)

            for neighbor in node.get_first_neighbors():
                if not visited[neighbor.get_vertex_id()]:
                    stack.append(neighbor)

        return dfs_sequence

    def bfs(self, start_id):
        visited = [False] * self.vertices_count
        queue = deque()
        bfs_sequence = []

        queue.append(self.get_vertex(start_id))
        visited[start_id] = True

        while queue:
            node = queue.popleft()
            bfs_sequence.append(node)

            if not node.get_first_neighbors():
                self.find_first_neighbors(node.get_vertex_id())

            for neighbor in node.get_first_neighbors():
                neighbor_id = neighbor.get_vertex_id()
                if not visited[neighbor_id]:
                    queue.append(neighbor)
                    visited[neighbor_id] = True

        return bfs_sequence

    def dijkstra_draw(self, path: list) -> None:
        """
        绘制Dijkstra算法生成的路径，并标注起点、终点
        :param path: 路径
        :return: None
        """
        self.draw_by_one_step()
        for index in range(len(path) - 1):
            print(f"beg:{path[index]}, end:{path[index + 1]}")
            self.draw_edge(beg=self.get_vertex(path[index]), end=self.get_vertex(path[index + 1]))
        self.mark_point(path[0], 'beg')
        self.mark_point(path[-1], 'end')
