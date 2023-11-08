from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox
from UI.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._dots = 0
        self._is_on_dfs = False
        self._is_on_bfs = False
        self._text_history = ''
        self.setupUi(self)
        # self.setStyleSheet("background-color: white;")
        self.openFileButton.clicked.connect(self.read_file)
        self.graph_show_button.clicked.connect(self.show_graph)
        self.graph_show_neighbors_button.clicked.connect(self.show_neighbors)
        self.dfs_button.clicked.connect(self.show_dfs)
        self.bfs_button.clicked.connect(self.show_bfs)
        self.mplwidget.timer.timeout.connect(self.process)
        self.mplwidget.timer.timeout.connect(self._update_text)
        self.dijkstra_button.clicked.connect(self.show_dijkstra)
        # self.info_board.ensureCursorVisible()

    def read_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'OFF Files (*.off)')
        print(file_name)
        if file_name:
            if not file_name.endswith('.off'):
                QMessageBox.warning(self, 'Invalid File', '请选择.off文件读入')
                return
            # DONE: 可以提示读文件成功
            self.clear()
            try:
                self.mplwidget.graph.read_file(file_name)

            except:
                QMessageBox.warning(self, 'Invalid File', '文件损坏！')
                return
            file_name = file_name.split('/')
            self.setWindowTitle(file_name[-1])
            self.add_text2info_board('文件载入成功！')

    def show_graph(self):
        self.mplwidget.clear()
        if self.judge_file():
            self.clear()
            self.mplwidget.graph.draw_by_one_step()
            self.mplwidget.draw()
            self.add_text2info_board('绘制完毕！拖动以查看细节！')
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
                QMessageBox.warning(self, 'Warning', f'请输入一个在（0-'
                                                     f'{self.mplwidget.graph.vertices_count - 1}）之间的整数')
                vertex_id = -1
        return vertex_id, ok

    def show_neighbors(self):
        if self.judge_file():
            vertex_id, ok = self.input_vertex_id(text=f'请输入你想要展示的点的邻接点（0-'
                                                      f'{self.mplwidget.graph.vertices_count - 1}）：')
            # 用户点击了"OK"按钮，在这里处理输入的文本
            if ok:
                self.clear()
                self.mplwidget.graph.draw_neighbors(int(vertex_id))
                self.mplwidget.draw()
                self.add_text2info_board(f"已显示{vertex_id}号点的第一、第二邻接点！")

        else:
            self.read_file()
            self.show_neighbors()

    def show_dijkstra(self):
        if self.judge_file():
            ok1, ok2 = [False] * 2
            vertex_id1, ok1 = self.input_vertex_id(text=f'请输入要计算的测地距离的起点（0-'
                                                        f'{self.mplwidget.graph.vertices_count - 1}）：')
            if ok1:
                vertex_id2, ok2 = self.input_vertex_id(text=f'请输入要计算的测地距离的终点（0-'
                                                            f'{self.mplwidget.graph.vertices_count}）：')
            if ok1 and ok2:
                self.clear()
                self.progress_bar.setValue(40)
                dist, path = self.mplwidget.graph.dijkstra(start=vertex_id1, end=vertex_id2)
                self.progress_bar.setValue(50)
                self.mplwidget.graph.dijkstra_draw(path)
                self.progress_bar.setValue(80)
                self.add_text2info_board(f"测地距离：{dist}\n具体路径：" + ' -> '.join(str(i) for i in path))
                self.mplwidget.draw()
                self.progress_bar.setValue(100)

        else:
            self.read_file()
            self.show_dijkstra()

    # DONE: 遍历成功后给出成功提示
    def show_dfs(self):
        if self.judge_file():
            vertex_id, ok = self.input_vertex_id(text=f"请输入DFS的起点（0-{self.mplwidget.graph.vertices_count - 1}）：")
            if ok:
                dfs_seq = self.mplwidget.graph.iterative_dfs(vertex_id)
                self.clear()
                faces_seqs = self.mplwidget.graph.get_faces_seq(dfs_seq)
                self._is_on_dfs = True
                self.mplwidget.draw_by_steps(faces_seqs)
        else:
            self.read_file()
            self.show_dfs()

    def show_bfs(self):
        if self.judge_file():
            vertex_id, ok = self.input_vertex_id(text=f"请输入DFS的起点（0-{self.mplwidget.graph.vertices_count}）：")
            if ok:
                bfs_seq = self.mplwidget.graph.bfs(vertex_id)
                self.clear()
                faces_seqs = self.mplwidget.graph.get_faces_seq(bfs_seq)
                self._is_on_bfs = True
                self.mplwidget.draw_by_steps(faces_seqs)
        else:
            self.read_file()
            self.show_bfs()

    # DONE: 点击按钮后会调用dfs内容，原因是QTimer同时监听两个按钮，应该使用两个属性加以区分
    def process(self):
        if self.mplwidget.faces_index >= len(self.mplwidget.faces):
            self.mplwidget.timer.stop()
            self.info_board.setText(self._text_history)
            if self._is_on_dfs:
                self.add_text2info_board(f"DFS绘制过程完成！")
                self._is_on_dfs = False
            elif self._is_on_bfs:
                self.add_text2info_board(f"BFS绘制过程完成！")
                self._is_on_bfs = False
        self.progress_bar.setValue(int(self.mplwidget.faces_index / len(self.mplwidget.faces) * 100))

    # TODO: 终端模式，显示用户输入内容
    def add_text2info_board(self, text):
        self.info_board.append(text)
        self.info_board.verticalScrollBar().setValue(self.info_board.verticalScrollBar().maximum())
        self._history_text_update()

    def _history_text_update(self):
        self._text_history = self.info_board.toPlainText()

    def clear(self):
        self.mplwidget.clear()
        self.progress_bar.setValue(0)
        # self.info_board.setText('')

    def judge_file(self):
        return bool(self.mplwidget.graph.vertices_count)

    def _update_text(self):
        if self.mplwidget.timer.isActive():
            self._dots = (self._dots + 1) % 4
            self.info_board.setText(self._text_history + f"\n正在处理" + '.' * self._dots)
            self.info_board.verticalScrollBar().setValue(self.info_board.verticalScrollBar().maximum())
