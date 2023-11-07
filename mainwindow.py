import time

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setStyleSheet("background-color: white;")
        self.openFileButton.clicked.connect(self.read_file)
        self.graph_show_button.clicked.connect(self.show_graph)
        self.graph_show_neighbors_button.clicked.connect(self.show_neighbors)
        self.dfs_button.clicked.connect(self.show_dfs)
        self.bfs_button.clicked.connect(self.show_bfs)
        self.mplwidget.timer.timeout.connect(self.dfs_process)
        self.mplwidget.timer.timeout.connect(self.bfs_process)
        self.dijkstra_button.clicked.connect(self.show_dijkstra)

    def read_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')
        print(file_name)
        if file_name[0]:
            # TODO: 可以提示读文件成功
            self.clear()
            self.mplwidget.graph.read_file(file_name[0])
        file_name = file_name[0].split('/')
        self.setWindowTitle(file_name[-1])

    def show_graph(self):
        self.mplwidget.clear()
        if self.judge_file():
            self.clear()
            self.mplwidget.graph.draw_by_one_step()
            self.mplwidget.draw()
        else:
            self.read_file()
            self.show_graph()

    def input_vertex_id(self, text):
        vertex_id = -1
        ok = False
        while vertex_id < 0 or vertex_id > 7690:
            vertex_id, ok = QInputDialog.getText(self, '', text)
            if not ok:
                return vertex_id, ok

            if vertex_id.isdigit() and 0 <= int(vertex_id) <= 7690:
                vertex_id = int(vertex_id)
            else:
                QMessageBox.warning(self, 'Warning', '请输入一个在（0-7690）之间的整数')
                vertex_id = -1
        return vertex_id, ok

    def show_neighbors(self):
        if self.judge_file():
            vertex_id, ok = self.input_vertex_id(text='请输入你想要展示的点的邻接点（0-7690）：')
            # 用户点击了"OK"按钮，在这里处理输入的文本
            if ok:
                self.clear()
                self.mplwidget.graph.draw_neighbors(int(vertex_id))
                self.mplwidget.draw()
        else:
            self.read_file()
            self.show_neighbors()

    def show_dijkstra(self):
        if self.judge_file():
            ok1, ok2 = [False] * 2
            vertex_id1, ok1 = self.input_vertex_id(text='请输入要计算的测地距离的起点（0-7690）：')
            if ok1:
                vertex_id2, ok2 = self.input_vertex_id(text='请输入要计算的测地距离的终点（0-7690）：')
            if ok1 and ok2:
                self.clear()
                self.progress_bar.setValue(40)
                dist, path = self.mplwidget.graph.dijkstra(start=vertex_id1, end=vertex_id2)
                self.progress_bar.setValue(50)
                self.mplwidget.graph.dijkstra_draw(path)
                self.progress_bar.setValue(80)
                self.info_board.setText(f"测地距离：{dist}\n具体路径：" + ' -> '.join(str(i) for i in path))
                self.mplwidget.draw()
                self.progress_bar.setValue(100)

        else:
            self.read_file()
            self.show_dijkstra()

    # TODO: 遍历成功后给出成功提示
    def show_dfs(self):
        if self.judge_file():
            dfs_seq = self.mplwidget.graph.iterative_dfs(0)
            self.clear()
            faces_seqs = self.mplwidget.graph.get_faces_seq(dfs_seq)
            self.mplwidget.draw_by_steps(faces_seqs)
        else:
            self.read_file()
            self.show_dfs()

    def dfs_process(self):
        if self.mplwidget.faces_index >= len(self.mplwidget.faces):
            self.mplwidget.timer.stop()

        self.progress_bar.setValue(int(self.mplwidget.faces_index / len(self.mplwidget.faces) * 100))

    def show_bfs(self):
        if self.judge_file():
            bfs_seq = self.mplwidget.graph.bfs(0)
            self.clear()
            faces_seqs = self.mplwidget.graph.get_faces_seq(bfs_seq)
            self.mplwidget.draw_by_steps(faces_seqs)
        else:
            self.read_file()
            self.show_bfs()
    # TODO: 点击按钮后会调用dfs内容，原因是QTimer同时监听两个按钮，应该使用两个属性加以区分
    def bfs_process(self):
        if self.mplwidget.faces_index >= len(self.mplwidget.faces):
            self.mplwidget.timer.stop()

        self.progress_bar.setValue(int(self.mplwidget.faces_index / len(self.mplwidget.faces) * 100))
    def clear(self):
        self.mplwidget.clear()
        self.progress_bar.setValue(0)
        self.info_board.setText('')

    def judge_file(self):
        return bool(self.mplwidget.graph.vertices_count)
