from Graph import Graph

if __name__ == '__main__':

    graph = Graph()

    graph.add_vertex(0)
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)

    graph.add_edge((0, 1))
    graph.add_edge((0, 4))
    graph.add_edge((1, 2))
    graph.add_edge((2, 3))
    graph.add_edge((1, 3))
    graph.add_edge((4, 2))
    graph.add_edge((4, 5))
    graph.add_edge((2, 5))
    graph.add_edge((5, 6))

    print("Representation of a graph")
    print(graph.dictOfVertices)

    print("BFS from root")
    for node in graph.bfs(0):
        print (node)

    print("DFS from root")
    for node in graph.dfs(0):
        print(node)

    print("BFS from 3 node, 4 next nodes")
    node = graph.bfs(3)
    print(next(node))
    print(next(node))
    print(next(node))
    print(next(node))

    print("Get neighbours of vertex 1")
    print(graph.get_neighbours(1))

    print("Graph after deleting vertex 5 and edge between 0 and 1")
    graph.delete_vertex(5)
    graph.delete_edge((0, 1))
    print(graph.dictOfVertices)