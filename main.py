import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Vertex:
    def __init__(self, name, source=False, sink=False):
        self.name = name
        self.source = source
        self.sink = sink


class Edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0
        self.returnEdge = None


class FlowNetwork:
    def __init__(self):
        self.vertices = []
        self.network = {}

    def get_source(self):
        for vertex in self.vertices:
            if vertex.source:
                return vertex
        return None

    def get_sink(self):
        for vertex in self.vertices:
            if vertex.sink:
                return vertex
        return None

    def get_vertex(self, name):
        for vertex in self.vertices:
            if name == vertex.name:
                return vertex

    def vertex_in_network(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return True
        return False

    def get_edges(self):
        allEdges = []
        for vertex in self.network:
            for edge in self.network[vertex]:
                allEdges.append(edge)
        return allEdges

    def add_vertex(self, name, source=False, sink=False):
        if source and sink:
            return "Vertex cannot be source and sink"
        if self.vertex_in_network(name):
            return "Duplicate vertex"
        if source:
            if self.get_source() is not None:
                return "Source already Exists"
        if sink:
            if self.get_sink() is not None:
                return "Sink already Exists"
        new_vertex = Vertex(name, source, sink)
        self.vertices.append(new_vertex)
        self.network[new_vertex.name] = []

    def add_edge(self, start, end, capacity):
        if start == end:
            return "Cannot have same start and end"
        if not self.vertex_in_network(start):
            return "Start vertex has not been added yet"
        if not self.vertex_in_network(end):
            return "End vertex has not been added yet"
        new_edge = Edge(start, end, capacity)
        return_edge = Edge(end, start, 0)
        new_edge.returnEdge = return_edge
        return_edge.returnEdge = new_edge
        vertex = self.get_vertex(start)
        self.network[vertex.name].append(new_edge)
        return_vertex = self.get_vertex(end)
        self.network[return_vertex.name].append(return_edge)

    def get_path(self, start, end, path):
        if start == end:
            return path
        for edge in self.network[start]:
            residual_capacity = edge.capacity - edge.flow
            if residual_capacity > 0 and not (edge, residual_capacity) in path:
                result = self.get_path(edge.end, end, path + [(edge, residual_capacity)])
                if result is not None:
                    return result

    def calculate_max_flow(self):
        source = self.get_source()
        sink = self.get_sink()
        if source is None or sink is None:
            return "Network does not have source and sink"
        path = self.get_path(source.name, sink.name, [])
        while path is not None:
            flow = min(edge[1] for edge in path)
            for edge, res in path:
                edge.flow += flow
                edge.returnEdge.flow -= flow
            path = self.get_path(source.name, sink.name, [])
        return sum(edge.flow for edge in self.network[source.name])


def max_flow(graph_nodes):
    fn = FlowNetwork()
    nodes = set([int(x) for x, y, z in graph_nodes] + [int(y) for x, y, z in graph_nodes])
    start = str(min(nodes))
    finish = str(max(nodes))
    fn.add_vertex(start, True, False)
    fn.add_vertex(finish, False, True)
    [fn.add_vertex(str(x)) for x in nodes if x not in [start, finish]]
    for x, y, z in graph_nodes:
        fn.add_edge(x, y, int(z))
    m = fn.calculate_max_flow()

    G = nx.DiGraph()
    G.add_weighted_edges_from([(int(x), int(y), int(z)) for x, y, z in graph_nodes])
    draw_graph(G, 'start_graph.png')
    G.clear()
    G.add_weighted_edges_from([(e.start, e.end, e.flow) for e in fn.get_edges() if e.flow > 0])
    draw_graph(G, 'graph.png')
    return m


def floyd_alg(graph):
    nodes = set([int(x) for x, y, z in graph] + [int(y) for x, y, z in graph])
    matr = np.zeros((len(nodes), len(nodes)))
    matr.fill(np.inf)
    for x, y, z in graph:
        matr[int(x)-1, int(y)-1] = int(z)
    for k in range(len(nodes)):
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                matr[i, j] = min(matr[i, j], matr[i, k] + matr[k, j])
    G = nx.DiGraph()
    G.add_weighted_edges_from([(int(x), int(y), int(z)) for x, y, z in graph])
    draw_graph(G, 'start_graph.png')
    return matr


def draw_graph(G, filename):
    plt.close()
    pos = nx.circular_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='#CC3333')
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    weight = {(x, y): data['weight'] for x, y, data in list(G.edges(data=True))}
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weight, label_pos=0.5)
    nx.draw_networkx_edges(G, pos, arrows=True)
    plt.axis('off')
    plt.savefig(filename, dpi=110)
