from graph.transitions import MathematicalRepresentation

class Vertex:
    label_id: int

    def connected_vertices(self):
        pass

    def disconnected_vertices(self):
        pass

    def incident_edges(self):
        pass


class Edge:
    vertex_pair: tuple(Vertex)

    def adjacent_edges(self):
        pass

    def disjoint_edges(self):
        pass


class Graph:
    vertex_list: list(Vertex)
    edge_list: list(Edge)
    # interesting_properties: list(AI.pattern_recognition)


    # configure from adjacency list // adjacency matrix // incidence matrix // edge list
    def load_from(self, repr: MathematicalRepresentation) -> None:
        self.vertex_list, self.edge_list = MathematicalRepresentation.to_vertices_and_edges()

    # represent as adjacency list // adjacency matrix // incidence matrix // edge list
    def represent_as(self, repr: MathematicalRepresentation) -> None:
        return MathematicalRepresentation.from_vertices_and_edges(self.vertex_list, self.edge_list)

    # check graph for loops and multiplicity (multiple edges)
    def is_simple(self) -> bool:
        pass


class GraphOperator:
    pass