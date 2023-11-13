from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox, QGraphicsDropShadowEffect
from UI.ui_mainwindow import Ui_MainWindow
from PyQt5.QtCore import QCoreApplication, QDateTime, Qt


def refresh():
    """
    刷新ui
    :return:
    """
    QCoreApplication.processEvents()


def create_shadow(blur_radius=0.3, x_offset=0.3, y_offset=0.6):
    """
    创建并返回一个具有阴影效果的 QGraphicsDropShadowEffect 对象。
    :param blur_radius: 模糊半径，控制阴影的模糊程度。
    :param x_offset: 阴影在 x 轴上的偏移量。
    :param y_offset: 阴影在 y 轴上的偏移量。
    :return: 具有指定参数的 QGraphicsDropShadowEffect 对象。
    """
    shadow = QGraphicsDropShadowEffect()  # 创建对象
    shadow.setBlurRadius(blur_radius)  # 设置模糊半径
    shadow.setXOffset(x_offset)  # 设置阴影在 x 轴上的偏移量
    shadow.setYOffset(y_offset)  # 设置阴影在 y 轴上的偏移量
    return shadow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        """
        主窗口的构造函数
        :param parent: 父窗口对象，默认为None
        """
        super(MainWindow, self).__init__(parent)
        self._dots = 0
        self._is_on_dfs = False
        self._is_on_bfs = False
        self._text_history = ''
        self.setupUi(self)

        # 设置主窗口背景色为白色
        self.setStyleSheet("background-color: white;")

        # 显示欢迎信息
        self._welcome()

        # 连接信号槽
        self.openFileButton.clicked.connect(self.read_file)
        self.graph_show_button.clicked.connect(self.show_graph)
        self.graph_show_neighbors_button.clicked.connect(self.show_neighbors)
        self.dfs_button.clicked.connect(self.show_dfs)
        self.bfs_button.clicked.connect(self.show_bfs)
        self.overall_view_button.clicked.connect(self.mplwidget.over_all_view)
        self.mplwidget.timer.timeout.connect(self.process)
        self.mplwidget.timer.timeout.connect(self._update_text)
        self.dijkstra_button.clicked.connect(self.show_dijkstra)
        self.info_board.verticalScrollBar().valueChanged.connect(self.check_scrollbar_visibility)

        # 为各个部件添加阴影效果
        self.mplwidget_border.setGraphicsEffect(create_shadow())
        self.button_border.setGraphicsEffect(create_shadow())
        self.info_board_border.setGraphicsEffect(create_shadow())
        self.openFileButton.setGraphicsEffect(create_shadow())
        self.overall_view_button.setGraphicsEffect(create_shadow())

        # 设置垂直滚动条永不可见
        self.info_board.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def read_file(self) -> bool:
        """
        通过文件对话框选择并读取OFF格式的文件。
        :return: 文件读取成功返回True，否则返回False。
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', './', 'OFF Files (*.off)')
        print(file_name)

        if file_name != '':
            if not file_name.endswith('.off'):
                QMessageBox.warning(self, 'Invalid File', '请选择.off文件读入')
                return False

            # 文件选择有效，清空窗口
            self.clear()
            try:
                # 尝试清空图形数据并读取新文件数据
                self.mplwidget.graph.clear_data()
                self.mplwidget.graph.read_file(file_name)
            except:
                QMessageBox.warning(self, 'Invalid File', '文件损坏！')
                return False

            # 获取文件名，并设置为主窗口标题
            file_name = file_name.split('/')
            self.setWindowTitle(file_name[-1])

            # 提示文件载入成功
            self.add_text2info_board('文件载入成功！')
            return True

        return False

    def show_graph(self):
        """
        显示图形
        :return:
        """
        # 清空绘图区域
        self.mplwidget.clear()

        # 判断是否读入文件
        if self.judge_file():
            # 如果文件有效，清空窗口
            self.clear()

            # 对图形进行全局视图
            self.mplwidget.over_all_view()

            # 绘图
            self.mplwidget.graph.draw_by_one_step()

            # 刷新绘图窗口
            self.mplwidget.draw()

            # 向信息板添加提示
            self.add_text2info_board('绘制完毕！拖动以查看细节！')

            # 设置进度条为最大
            self.progress_bar.setValue(self.progress_bar.maximum())
        else:
            # 如果未读入文件，尝试重新读入
            if self.read_file():
                self.show_graph()
            else:
                # 如果文件未选择或读取取消，向信息板添加提示
                self.add_text2info_board("文件未选择或读取取消。")

    def input_vertex_id(self, text):
        """
        获取用户输入的顶点ID

        :param text: 输入框提示文本
        :return:
        - vertex_id: 用户输入的顶点ID
        - ok: 用户是否确认输入
        """
        vertex_id = -1
        ok = False

        # 循环直到用户输入有效的顶点ID
        while vertex_id < 0 or vertex_id > self.mplwidget.graph.vertices_count - 1:
            vertex_id, ok = QInputDialog.getText(self, '', text)

            # 如果用户取消输入，返回当前输入结果
            if not ok:
                return vertex_id, ok

            # 判断输入是否为整数且在有效范围内
            if vertex_id.isdigit() and 0 <= int(vertex_id) <= self.mplwidget.graph.vertices_count - 1:
                vertex_id = int(vertex_id)
            else:
                # 提示用户重新输入有效范围内的整数
                QMessageBox.warning(self, 'Warning', f'请输入一个在（0-'
                                                     f'{self.mplwidget.graph.vertices_count - 1}）之间的整数')
                vertex_id = -1

        return vertex_id, ok

    def show_neighbors(self):
        """
        显示指定顶点的邻接点
        :return: None
        """
        # 判断是否读入文件
        if self.judge_file():
            # 获得用户输入的顶点ID
            vertex_id, ok = self.input_vertex_id(text=f'请输入你想要展示的点的邻接点（0-'
                                                      f'{self.mplwidget.graph.vertices_count - 1}）：')
            # 用户点击了"OK"按钮，在这里处理输入的文本
            if ok:
                # 向信息板添加已选择的点信息
                self.add_text2info_board(f"已选择的点:{vertex_id}")

                # 清空窗口
                self.clear()

                # 绘制指定顶点的邻接点
                self.mplwidget.graph.draw_neighbors(int(vertex_id))

                # 刷新窗口
                self.mplwidget.draw()

                # 向信息板添加已显示的邻接点信息
                self.add_text2info_board(f"已显示{vertex_id}号点的第一、第二邻接点！")

                # 设置进度条为最大值
                self.progress_bar.setValue(self.progress_bar.maximum())

        else:
            # 如果未读入文件，尝试重新读取文件
            if self.read_file():
                self.show_neighbors()
            else:
                # 如果文件未选择或读取取消，向信息板添加相应提示
                self.add_text2info_board("文件未选择或读取取消。")

    def show_dijkstra(self):
        """
        显示两点之间的测地距离及具体路径。
        :return: None
        """
        # 判断文件是否有效
        if self.judge_file():
            ok1, ok2 = [False] * 2

            # 获取用户输入的起点顶点ID
            vertex_id1, ok1 = self.input_vertex_id(text=f'请输入要计算的测地距离的起点（0-'
                                                        f'{self.mplwidget.graph.vertices_count - 1}）：')

            # 如果用户成功输入起点ID，获取用户输入的终点顶点ID
            if ok1:
                vertex_id2, ok2 = self.input_vertex_id(text=f'请输入要计算的测地距离的终点（0-'
                                                            f'{self.mplwidget.graph.vertices_count - 1}）：')

            # 如果用户成功输入终点ID，进行测地距离计算和绘制
            if ok1 and ok2:
                # 清空窗口
                self.clear()

                # 向信息板添加已选择的点信息
                self.add_text2info_board(f"已选择的点: {vertex_id1} --> {vertex_id2}")

                # 进度条增加
                self.progress_bar.setValue(40)
                refresh()

                # 计算测地距离和路径
                dist, path = self.mplwidget.graph.dijkstra(start=vertex_id1, end=vertex_id2)

                # 进度条增加
                self.progress_bar.setValue(50)
                refresh()

                # 设置图形显示比例
                self.mplwidget.graph.ax.set_box_aspect([1, 1, 1], zoom=1.5)

                # 绘制测地距离路径
                self.mplwidget.graph.dijkstra_draw(path)

                # 进度条增加
                self.progress_bar.setValue(80)
                refresh()

                # 向信息板添加测地距离和具体路径信息
                self.add_text2info_board(f"测地距离：{dist}\n具体路径：" + ' -> '.join(str(i) for i in path))

                # 如果测地距离为无穷大，进行全局视图
                if dist == float('inf'):
                    self.mplwidget.over_all_view()

                # 刷新窗口
                self.mplwidget.draw()

                # 进度更新为最大值
                self.progress_bar.setValue(100)

        else:
            # 如果文件无效，尝试重新读取文件
            if self.read_file():
                self.show_dijkstra()
            else:
                # 如果文件未选择或读取取消，向信息板添加相应提示
                self.add_text2info_board("文件未选择或读取取消。")

    # DONE: 遍历成功后给出成功提示
    def show_dfs(self):
        """
        显示深度优先搜索（DFS）的过程和结果。
        :return: None
        """
        # 判断文件是否有效
        if self.judge_file():
            # 获取用户输入的起点顶点ID
            vertex_id, ok = self.input_vertex_id(text=f"请输入DFS的起点（0-{self.mplwidget.graph.vertices_count - 1}）：")

            # 如果用户成功输入起点ID
            if ok:
                # 迭代DFS，获取DFS遍历的顶点序列
                dfs_seq = self.mplwidget.graph.iterative_dfs(vertex_id)

                # 如果DFS遍历的顶点数量不等于图中的顶点数量，说明图非连通，给出警告提示
                if len(dfs_seq) != self.mplwidget.graph.vertices_count:
                    self.add_text2info_board(f"该图非连通，无法DFS")
                    QMessageBox.warning(self, 'Warning', f'该图非连通，无法DFS')
                    return

                # 清除窗口
                self.clear()

                # 对图形进行全局视图
                self.mplwidget.over_all_view()

                # 获取DFS遍历的面序列
                faces_seqs = self.mplwidget.graph.get_faces_seq(dfs_seq)

                # 标记当前进行DFS
                self._is_on_dfs = True

                # 向信息板添加DFS起点信息
                self.add_text2info_board(f"用户选择的DFS起点：{vertex_id}")

                # 按步骤绘制DFS过程
                self.mplwidget.draw_by_steps(faces_seqs)
        else:
            # 如果文件无效，尝试重新读取文件
            if self.read_file():
                self.show_dfs()
            else:
                # 如果文件未选择或读取取消，向信息板添加相应提示
                self.add_text2info_board("文件未选择或读取取消。")

    def show_bfs(self):
        """
        显示广度优先搜索（BFS）的过程和结果。
        :return: None
        """

        # 判断文件是否有效
        if self.judge_file():
            # 获取用户输入的起点顶点ID
            vertex_id, ok = self.input_vertex_id(text=f"请输入BFS的起点（0-{self.mplwidget.graph.vertices_count - 1}）：")

            # 如果用户成功输入起点ID
            if ok:
                # 进行BFS，获取BFS遍历的顶点序列
                bfs_seq = self.mplwidget.graph.bfs(vertex_id)

                # 如果BFS遍历的顶点数量不等于图中的顶点数量，说明图非连通，给出警告提示
                if len(bfs_seq) != self.mplwidget.graph.vertices_count:
                    self.add_text2info_board(f"该图非连通，无法BFS")
                    QMessageBox.warning(self, 'Warning', f'该图非连通，无法BFS')
                    return

                # 清空窗口
                self.clear()

                # 对图形进行全局视图
                self.mplwidget.over_all_view()

                # 获取BFS遍历的面序列
                faces_seqs = self.mplwidget.graph.get_faces_seq(bfs_seq)

                # 标记当前进行BFS
                self._is_on_bfs = True

                # 向信息板添加BFS起点信息
                self.add_text2info_board(f"用户选择的BFS起点：{vertex_id}")

                # 按步骤绘制BFS过程
                self.mplwidget.draw_by_steps(faces_seqs)
        else:
            # 如果文件无效，尝试重新读取文件
            if self.read_file():
                self.show_bfs()
            else:
                # 如果文件未选择或读取取消，向信息板添加相应提示
                self.add_text2info_board("文件未选择或读取取消。")

    # DONE: 点击按钮后会调用dfs内容，原因是QTimer同时监听两个按钮，应该使用两个属性加以区分
    def process(self):
        """
        在绘制过程中更新进度条和信息板
        :return:
        """
        # 判断是否已经完成整个绘制过程
        if self.mplwidget.faces_index >= len(self.mplwidget.faces):
            # 定时器停止
            self.mplwidget.timer.stop()

            # 恢复信息板显示
            self.info_board.setText(self._text_history)

            # 判断是否在DFS绘制过程中
            if self._is_on_dfs:
                self.add_text2info_board(f"DFS绘制过程完成！")
                self._is_on_dfs = False
            # 判断是否在BFS绘制过程中
            elif self._is_on_bfs:
                self.add_text2info_board(f"BFS绘制过程完成！")
                self._is_on_bfs = False

        # 更新进度条的值
        self.progress_bar.setValue(int(
            self.mplwidget.faces_index / len(self.mplwidget.faces) * self.progress_bar.maximum()
        ))

    def _welcome(self):
        """
        向信息板添加欢迎文本
        :return:
        """
        welcome_text = """欢迎使用三维网格模型几何特性分析程序！
这个程序可以帮助您分析三维物体模型的特性，包括邻接点查找、测地距离计算、图结构遍历和三维图形显示。
请导入您的三维物体模型文件（如Bunny.off），然后开始探索其几何特性。如果需要帮助，请查看帮助文档或按下相应的按钮，我们随时为您提供支持。
祝您使用愉快！
"""
        self.add_text2info_board(text=welcome_text, with_time=False)

    # DONE: 终端模式，显示用户输入内容

    def add_text2info_board(self, text, with_time=True):
        """
        向信息板添加文本，并可选择是否显示时间戳。
        :param text: 要添加的文本内容。
        :param with_time: 是否显示时间戳，默认为True。
        :return: None
        """
        # 判断是否显示时间
        if with_time:
            # 获取当前时间
            datetime = QDateTime().currentDateTime()
            current_time = datetime.toString("yyyy-MM-dd hh:mm:ss")

            # 添加带时间戳的文本到信息板
            self.info_board.append(current_time + ': ' + text)
        else:
            # 直接添加文本到信息板
            self.info_board.append(text)

        # 将滚动条滑动到最底部
        self.info_board.verticalScrollBar().setValue(self.info_board.verticalScrollBar().maximum())

        # 更新历史文本
        self._history_text_update()

    def _history_text_update(self):
        """
        更新历史文本。
        :return: None
        """
        # 将信息板的文本内容更新到历史文本变量中
        self._text_history = self.info_board.toPlainText()

    def clear(self):
        """
        清空窗口
        :return:
        """
        # 清空绘图板
        self.mplwidget.clear()

        # 设置进度条为0
        self.progress_bar.setValue(0)

    def judge_file(self):
        """
        判断是否读入文件
        :return: True: 已读入文件
        """
        return bool(self.mplwidget.graph.vertices_count)

    def _update_text(self):
        """
        在定时器活动时更新文本。
        :return:
        """
        # 如果定时器处于活动状态
        if self.mplwidget.timer.isActive():
            # 更新处理中的文本，显示不同数量的点
            self._dots = (self._dots + 1) % 4
            self.info_board.setText(self._text_history + f"\n正在处理" + '.' * self._dots)

            # 将滚动条滑动到最底部
            self.info_board.verticalScrollBar().setValue(self.info_board.verticalScrollBar().maximum())

    def check_scrollbar_visibility(self):
        """
        检查滚动条的可见性，并根据内容是否超出范围设置滚动条的显示策略。
        :return:
        """
        # 判断内容是否超出范围
        is_content_overflowing = self.info_board.verticalScrollBar().maximum() > self.info_board.height()

        # 根据内容是否超出范围来设置滚动条的显示策略
        if is_content_overflowing:
            self.info_board.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        else:
            self.info_board.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
