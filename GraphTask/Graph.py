# class representation of non-directed graph

class Graph():

    def __init__(self):
        self.dictOfVertices = {}  # to nie Java

    def add_vertex(self, vertex):
        if vertex not in self.dictOfVertices:
            self.dictOfVertices[vertex] = []

    def add_edge(self, edge):
        # this is non-directed graph so we have to add vertex2 to values of key = vertex1
        # and vertex1 to values of key = vertex2

        vertex1, vertex2 = edge
        if vertex1 in self.dictOfVertices:
            if vertex2 not in self.dictOfVertices[vertex1]: # a gdyby użyć zbioru zamiast listy?
                self.dictOfVertices[vertex1].append(vertex2)
        else:
            # if vertex is not found, new is created
            self.dictOfVertices[vertex1] = [vertex2]

        if vertex2 in self.dictOfVertices:
            if vertex1 not in self.dictOfVertices[vertex2]:
                self.dictOfVertices[vertex2].append(vertex1)
        else:
            # if vertex is not found, new is created
            self.dictOfVertices[vertex2] = [vertex1]

    def delete_edge(self, edge):
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.dictOfVertices:
            if vertex2 in self.dictOfVertices[vertex1]:
                self.dictOfVertices[vertex1].remove(vertex2)
                # we know that if vertex2 is in dictOfVertices[vertex1], then vertex1 is in dictOfVertices[vertex2]
                # we don't need to check that because add_edge function works in that way
                self.dictOfVertices[vertex2].remove(vertex1)

    def delete_vertex(self, vertex):
        if vertex in self.dictOfVertices:
            for neighbour in self.dictOfVertices[vertex]:
                self.dictOfVertices[neighbour].remove(vertex)
            del self.dictOfVertices[vertex]

    def get_neighbours(self, vertex):
        neighbours = []
        if vertex in self.dictOfVertices:
            for neighbour in self.dictOfVertices[vertex]:
                neighbours.append(neighbour)
        else:
            return None
        return neighbours

    def dfs(self, vertex):
        return DfsIterator(self, vertex)

    def bfs(self, vertex):
        return BfsIterator(self, vertex)


class DfsIterator:
    def __init__(self, graph, vertex):
        self.graph = graph
        self.visited_vertexes = []
        self.stack = [vertex]
        self.dfs_list = []

        while self.stack:
            current_vertex = self.stack.pop()
            if current_vertex not in self.visited_vertexes:
                self.visited_vertexes.append(current_vertex)
                self.dfs_list.append(current_vertex)
            for neighbour in self.graph.dictOfVertices[current_vertex]:
                if neighbour not in self.visited_vertexes:
                    self.stack.append(neighbour)

    def __next__(self):
        try:
            return self.dfs_list.pop(0)
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


class BfsIterator:
    def __init__(self, graph, vertex):
        self.graph = graph
        self.visited_vertexes = []
        self.queue = [vertex]  # collections.deque
        self.bfs_list = []

        while self.queue:
            current_vertex = self.queue.pop(0)
            if current_vertex not in self.visited_vertexes:
                self.visited_vertexes.append(current_vertex)
                self.bfs_list.append(current_vertex)
            for neighbour in self.graph.dictOfVertices[current_vertex]:
                if neighbour not in self.visited_vertexes:
                    self.queue.append(neighbour)

    def __next__(self):
        try:
            return self.bfs_list.pop(0)
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self














