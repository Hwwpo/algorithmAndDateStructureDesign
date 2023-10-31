from mesh import Mesh
from graph import Graph, hold_on

if __name__ == '__main__':
    mesh = Mesh('Bunny.off')
    graph = Graph()
    graph.draw()
    graph.draw_edge(0)

    hold_on()
    pass
