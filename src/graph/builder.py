from src.contracts.types import FileAnalysis
from .relations import CodeGraph, GraphNode, GraphEdge


def build(analysis: FileAnalysis) -> CodeGraph:
    graph = CodeGraph()

    for sym in analysis.symbols:
        loc = sym.location
        graph.add_node(GraphNode(
            id=sym.name,
            label=sym.name,
            kind=sym.kind,
            file=analysis.file,
            start_byte=loc.start_byte if loc else 0,
            end_byte=loc.end_byte if loc else 0,
        ))

    for imp in analysis.imports:
        for name in imp.names:
            graph.add_edge(GraphEdge(
                source=analysis.file, target=name, relation="imports",
            ))

    for dep in analysis.dependencies:
        graph.add_edge(GraphEdge(
            source=dep.source, target=dep.target, relation=dep.relation,
        ))

    return graph


def build_from_reports(analyses: list[FileAnalysis]) -> CodeGraph:
    graph = CodeGraph()
    for a in analyses:
        sub = build(a)
        for n in sub.nodes:
            graph.add_node(n)
        for e in sub.edges:
            graph.add_edge(e)
    return graph
