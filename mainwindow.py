import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("background-color: white;")
        self.openFileButton.clicked.connect(self.read_file)
        self.graph_show_button.clicked.connect(self.show_graph)
        self.graph_show_neighbors_button.clicked.connect(self.show_neighbors)
        self.dfs_button.clicked.connect(self.show_dfs())

    def read_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')
        print(file_name)
        if file_name[0]:
            # TODO: 可以提示读文件成功
            self.mplwidget.graph.read_file(file_name[0])
        file_name = file_name[0].split('/')
        self.setWindowTitle(file_name[-1])

    def show_graph(self):
        self.mplwidget.clear()
        if self.judge_file():
            self.mplwidget.clear()
            self.mplwidget.graph.draw_by_one_step()
            self.mplwidget.draw()
        else:
            self.read_file()
            self.show_graph()

    def show_neighbors(self):
        if self.judge_file():
            vertex_id = -1
            while vertex_id < 0 or vertex_id > 7690:
                vertex_id, ok = QInputDialog.getText(self, '', '请输入你想要展示的点的邻接点（0-7690）：')
                if not ok:
                    return

                if vertex_id.isdigit() and 0 <= int(vertex_id) <= 7690:
                    vertex_id = int(vertex_id)
                else:
                    QMessageBox.warning(self, 'Warning', '请输入一个在（0-7690）之间的整数')
                    vertex_id = -1
            # 用户点击了"OK"按钮，在这里处理输入的文本
            if ok:
                self.mplwidget.clear()
                self.mplwidget.graph.draw_neighbors(int(vertex_id))
                self.mplwidget.draw()
        else:
            self.read_file()
            self.show_neighbors()

    def show_dfs(self):
        if self.judge_file():
            self.mplwidget.graph.iterative_dfs(0)
        else:
            self.read_file()
            self.show_dfs()
    def judge_file(self):
        return bool(self.mplwidget.graph.vertices_count)
