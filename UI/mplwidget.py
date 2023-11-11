from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from core.graph import Graph, AXIS_SHOW
from PyQt5.QtCore import QTimer


class MPLWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        该类实现了在Qt中的窗口中使用PLT绘制图形
        :param parent: 窗口的父类
        :param width: 窗口的宽度，单位为inch
        :param height:窗口的高度，单位为inch
        :param dpi:每inch的像素数量
        """
        # 创建Graph对象，用于绘制图形
        self.graph = Graph()
        super(MPLWidget, self).__init__(self.graph.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # 创建一个定时器，用于分步画图
        self.timer = QTimer(self)
        # 定时器每计时一定时间就画一部分图
        self.timer.timeout.connect(self.draw_portions)
        self.setFixedSize(width * dpi, height * dpi)
        self.draw()

    def clear(self):
        """
        清空窗口上的图形
        :return:
        """
        self.graph.ax.clear()
        # 清除完后隐藏坐标轴
        plt.axis(AXIS_SHOW)
        # 计时器停止计时
        self.timer.stop()
        # 刷新界面
        self.draw()

    def over_all_view(self):
        """
        设置整体视图范围
        :return:
        """
        self.graph.ax.set_xlim([self.graph.min_lim, self.graph.max_lim])
        self.graph.ax.set_ylim([self.graph.min_lim, self.graph.max_lim])
        self.graph.ax.set_zlim([self.graph.min_lim, self.graph.max_lim])
        self.draw()

    def draw_by_steps(self, faces: list):
        """

        :param faces: face类的集合，按照索引顺序绘制
        :return:
        """
        # 计算帧数，即每画的一部分中，有多少个面
        fps = int(len(faces) / 150)
        # 按照计算出来的帧数将faces划分
        self.faces = [faces[i:i + fps] for i in range(0, len(faces), fps)]
        # 设置计时器间隔，即每过多长时间画一笔
        self.timer.setInterval(int(2000 / len(self.faces)))
        # 开始计时/绘画
        self.timer.start()
        # 从第0个划分开始
        self.faces_index = 0

    def draw_portions(self) -> None:
        """
        根据面的顺序逐步画图
        :return: None
        """
        if self.faces_index < len(self.faces):
            # 获取当前帧的面的位置信息
            location = [face.location for face in self.faces[self.faces_index]]
            self.graph.add_face(location, edge_color='g')
            # 刷新界面，使之显示
            self.draw()
            # 继续下一个划分
            self.faces_index += 1
