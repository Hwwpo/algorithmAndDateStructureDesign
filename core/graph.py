from collections import deque

import networkx as nx

from core.edge import Edge
from core.mesh import Mesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from core.vertex import Vertex
import matplotlib.pyplot as plt

# 坐标轴展示设置
AXIS_SHOW = 'off'

# 邻接点显示颜色设置
FIRST_NEIGHBOR_COLOR = 'r'
SECOND_NEIGHBOR_COLOR = 'y'


class Graph(Mesh):
    def __init__(self):
        """
        self.ax: 存储绘图内容
        """
        super().__init__()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect([1, 1, 1])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        plt.axis(AXIS_SHOW)
        self.ax.view_init(elev=-87, azim=-95)

    def clear_data(self):
        """
        清空图的内容
        :return:
        """
        self.vertices_count = 0
        self.faces_count = 0
        self.faces = []
        self.vertices = []
        self.edges = []
        self.max_lim = -1e6
        self.min_lim = 1e6
        self.net = nx.Graph()

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

        # 判断重复边
        appended = [False] * self.faces_count

        # 存储生成的面的集合
        faces = []

        # 遍历顶点
        for vertex in vertices:
            related_face = vertex.related_faces
            for face in related_face:
                # 如果没有添加过
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

    def draw_neighbors(self, vertex_id: int) -> None:
        """
        绘制出指定点的第一邻接点和第二邻接点，使用不同颜色标注
        :param vertex_id: 要绘制邻接点的顶点ID。
        :return: None
        """
        # 标记指定点
        self.mark_point(vertex_id=vertex_id, text='point')

        # 获得指定点对象
        vertex = self.vertices[vertex_id]

        # 查找并记录第二邻接点
        self.find_second_neighbors(vertex_id)

        # 遍历第一邻接点并绘制
        for first_neighbor in vertex.get_first_neighbors():
            self.draw_edge(beg=vertex, end=first_neighbor, color=FIRST_NEIGHBOR_COLOR)

            # 遍历第二邻接点并绘制
            for second_neighbor in first_neighbor.get_first_neighbors():
                if second_neighbor in vertex.get_second_neighbors():
                    self.draw_edge(beg=first_neighbor, end=second_neighbor, color=SECOND_NEIGHBOR_COLOR)

        # 绘制完点之后再绘制整个图形
        self.draw_by_one_step()

    def mark_point(self, vertex_id: int, text=None, color='y') -> None:
        """
        为点添加注释
        :param vertex_id: 需要注释的点的id
        :param text: 标注的内容，默认为点的id
        :param color: 标注的颜色
        :return: None
        """
        # 如果没有文本内容，则默认为顶点的id
        if not text:
            text = str(vertex_id)

        # 得到点的坐标
        location = self.get_vertex(vertex_id).axis
        px, py, pz = location

        # 添加注释
        self.ax.text(px, py, pz, text, color=color, zorder=10)

    def draw_edge(self, edge: Edge, color='r', z_order=10) -> None:
        """
        在窗口上绘制一条边
        :param edge: 画的对象
        :param color: 线的颜色
        :param z_order: 图层优先级，建议保持默认
        :return: None
        """
        # 得到边的起点终点坐标
        beg, end = edge.vertices
        xs, ys, zs = list(zip(beg.axis, end.axis))

        # 绘制边
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
        # 得到边的起点终点坐标
        xs, ys, zs = list(zip(beg.axis, end.axis))
        self.ax.plot(xs, ys, zs, color=color, zorder=z_order)

    def iterative_dfs(self, start_id):
        """
        使用迭代深度优先搜索（DFS）算法遍历图的顶点，并返回遍历的顺序。

        :param start_id: 深度优先搜索的起始顶点ID。
        :return: DFS遍历的顶点序列。
        """
        # 初始化
        visited = [False] * self.vertices_count  # 记录顶点是否被访问
        stack = []  # 模拟栈来存储待访问的顶点
        dfs_sequence = []  # 存储序列

        # 起点入栈
        stack.append(self.get_vertex(start_id))

        # 迭代DFS算法
        while stack:
            node = stack.pop()  # 弹出栈顶顶点
            node_id = node.get_vertex_id()

            # 如果没有找第一邻接点，寻找并记录
            if not node.get_first_neighbors():
                self.find_first_neighbors(node_id)

            # 如果顶点未被访问过，标记为已访问，并添加到DFS序列中
            if not visited[node_id]:
                visited[node_id] = True
                dfs_sequence.append(node)

            # 将未访问的第一邻接点加入栈中
            for neighbor in node.get_first_neighbors():
                if not visited[neighbor.get_vertex_id()]:
                    stack.append(neighbor)

        return dfs_sequence

    def bfs(self, start_id):
        """
        使用广度优先搜索（BFS）算法遍历图的顶点，并返回遍历的顺序。

        :param start_id: 广度优先搜索的起始顶点ID。
        :return: BFS遍历的顶点序列。
        """
        # 初始化
        visited = [False] * self.vertices_count  # 记录顶点是否被访问过的列表
        queue = deque()  # 使用队列存储待访问的顶点
        bfs_sequence = []  # 存储BFS遍历的顶点序列

        # 将起始顶点加入队列，并标记为已访问
        queue.append(self.get_vertex(start_id))
        visited[start_id] = True

        # BFS算法
        while queue:
            node = queue.popleft()  # 出队列操作
            bfs_sequence.append(node)

            # 如果当前顶点未找第一邻接点，找到并记录
            if not node.get_first_neighbors():
                self.find_first_neighbors(node.get_vertex_id())

            # 遍历第一邻接点
            for neighbor in node.get_first_neighbors():
                neighbor_id = neighbor.get_vertex_id()
                # 如果邻接点未被访问过，加入队列并标记为已访问
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
        # 先绘制整个图形
        self.draw_by_one_step()

        # 绘制路径中的每一条边
        for index in range(len(path) - 1):
            self.draw_edge(beg=self.get_vertex(path[index]), end=self.get_vertex(path[index + 1]))

        # 如果存在边，则标注起点终点
        if path:
            self.mark_point(path[0], 'beg')
            self.mark_point(path[-1], 'end')
