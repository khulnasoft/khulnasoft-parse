from dataclasses import dataclass
from typing import Optional


@dataclass
class GraphNode:
    id: str
    label: str
    kind: str
    file: str = ""
    start_byte: int = 0
    end_byte: int = 0


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str


@dataclass
class CodeGraph:
    nodes: list[GraphNode] = None
    edges: list[GraphEdge] = None

    def __post_init__(self):
        if self.nodes is None:
            self.nodes = []
        if self.edges is None:
            self.edges = []

    def add_node(self, node: GraphNode) -> None:
        if not any(n.id == node.id for n in self.nodes):
            self.nodes.append(node)

    def add_edge(self, edge: GraphEdge) -> None:
        if not any(e.source == edge.source and e.target == edge.target and e.relation == edge.relation
                   for e in self.edges):
            self.edges.append(edge)
