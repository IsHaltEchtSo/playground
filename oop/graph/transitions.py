from abc import ABC, abstractmethod
from graph.elements import Edge, Vertex

class MathematicalRepresentation(ABC):
    representation: list(list(int)) = None

    @abstractmethod
    def init_from_vertices_and_edges(vertex_list: list(Vertex), edge_list: list(Edge)) -> list(list(int)):
        """uses V(X) and E(X) to return a mathematical representation of the graph """

    @abstractmethod
    def to_vertices_and_edges(representation: list(list(int))) -> tuple(list(Vertex), list(Edge)):
        """uses a mathematical representation of the graph to return V(X) and E(X) """


class AdjacencyListRepresentation(MathematicalRepresentation):
    def init_from_vertices_and_edges():
        pass

    def to_vertices_and_edges():
        pass


class AdjacencyMatrixRepresentation(MathematicalRepresentation):
    def init_from_vertices_and_edges():
        pass

    def to_vertices_and_edges():
        pass


class IncidenceMatrixRepresentation(MathematicalRepresentation):
    def init_from_vertices_and_edges():
        pass

    def to_vertices_and_edges():
        pass


class EdgeListRepresentation(MathematicalRepresentation):
    def init_from_vertices_and_edges():
        pass

    def to_vertices_and_edges():
        pass
