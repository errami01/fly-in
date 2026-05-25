from src.exceptions import GraphError
from src.graph.edge import ConnectionEdge
from src.graph.node import ZoneNode


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, ZoneNode] = {}
        self.edges: dict[tuple[str, str], ConnectionEdge] = {}
        self.start: str | None = None
        self.end: str | None = None

    def add_node(self, node: ZoneNode) -> None:
        if node.name in self.nodes:
            raise GraphError(f"Duplicate node: {node.name}")

        self.nodes[node.name] = node

    def add_edge(self, edge: ConnectionEdge) -> None:
        key = edge.key()

        if key in self.edges:
            raise GraphError("Duplicate connection")

        if edge.start not in self.nodes:
            raise GraphError(f"Unknown node: {edge.start}")

        if edge.end not in self.nodes:
            raise GraphError(f"Unknown node: {edge.end}")

        self.edges[key] = edge

        self.nodes[edge.start].neighbors[edge.end] = edge
        self.nodes[edge.end].neighbors[edge.start] = edge

    def get_edge(self, a: str, b: str) -> ConnectionEdge:
        key = tuple(sorted((a, b)))
        return self.edges[key]