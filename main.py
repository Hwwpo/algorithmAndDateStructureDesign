import sys

from mesh import Mesh
from graph import Graph, hold_on
from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    # graph = Graph()
    # graph.read_file('Bunny.off')
    # # graph.draw_neighbors(400)
    # # graph.draw_by_one_step()
    # # dfs_sequence = graph.bfs(4000)
    # # bfs_sequence = graph.bfs(0)
    # # graph.draw_neighbors(0)
    # _, path = graph.dijkstra(start=0, end=10)
    # print(path)
    # graph.dijkstra_draw(path)
    # print(bfs_sequence)
    # graph.draw(dfs_sequence)
    # graph.draw_by_one_step()
    # graph.add_comment(0)
    # graph.draw_edge(graph.edges[0])
    # graph.draw_by_one_step()
    # graph.draw_neighbors(0)

    # path, length = graph.dijkstra(0, 10)
    # print(path, length)
    # graph.draw(graph.bfs(0))
    # graph.draw(bfs_sequence)
    # for vertex in dfs_sequence:
    #     graph.draw_edge(vertex.get_vertex_id())

    # graph.find_first_neighbors(0)
    # graph.find_second_neighbors(4000)
    # print(*graph.vertices[4000].get_first_neighbors(), sep="\n")
    # print("\n")
    # print(*graph.vertices[4000].get_second_neighbors(), sep="\n")
    # print("\n")
    # # print(mesh.faces)
    # # graph = Graph()
    # graph.draw_by_one_step()
    # # # graph.get_adjacent_point(0)
    # # displayed_point = int(input(
    # #     f"Please choose a point to display its first and second adjacent point(0-{mesh.vertices_count - 1}): "
    # # ))
    # graph.draw_neighbors(0)
    # graph.draw_edge(0, 'w')
    # graph.add_comment(0)
    # graph.add_comment(displayed_point)
    # hold_on()
    pass
