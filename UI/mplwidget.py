from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from core.graph import Graph, AXIS_SHOW
from PyQt5.QtCore import QTimer
FPS = 100


class MPLWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.graph = Graph()
        super(MPLWidget, self).__init__(self.graph.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.draw_portions)

    def clear(self):
        self.graph.ax.clear()
        plt.axis(AXIS_SHOW)
        self.graph.ax.set_box_aspect([1, 1, 1])
        self.timer.stop()
        self.draw()

    def draw_by_steps(self, faces: list):
        self.timer.setInterval(100)
        self.faces = [faces[i:i+FPS] for i in range(0, len(faces), FPS)]
        self.timer.start()
        self.faces_index = 0

    def draw_portions(self) -> None:
        """
        根据面的顺序逐步画图
        :param faces: 面的集合
        :return: None
        """
        if self.faces_index < len(self.faces):
            location = [face.location for face in self.faces[self.faces_index]]
            self.graph.add_face(location, edge_color='g')
            self.draw()
            self.faces_index += 1
