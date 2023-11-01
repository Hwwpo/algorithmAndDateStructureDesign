from mesh import Mesh
from graph import Graph, hold_on

if __name__ == '__main__':
    mesh = Mesh('Bunny.off')
    # print(mesh.faces)
    graph = Graph()
    graph.draw_by_one_step()
    # # graph.get_adjacent_point(0)
    # displayed_point = int(input(
    #     f"Please choose a point to display its first and second adjacent point(0-{mesh.vertices_count - 1}): "
    # ))
    graph.draw_edge(0)
    # graph.add_comment(displayed_point)
    hold_on()
    pass
