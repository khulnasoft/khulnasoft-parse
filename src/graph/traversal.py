from collections import deque
from .relations import CodeGraph


def reverse_lookup(graph: CodeGraph, symbol: str) -> list[dict]:
    """Find everything that depends on a given symbol."""
    results = []
    for e in graph.edges:
        if e.target == symbol:
            results.append({"caller": e.source, "relation": e.relation, "target": e.target})
    return results


def forward_lookup(graph: CodeGraph, symbol: str) -> list[dict]:
    """Find everything a given symbol depends on."""
    results = []
    for e in graph.edges:
        if e.source == symbol:
            results.append({"caller": e.source, "relation": e.relation, "target": e.target})
    return results


def find_paths(graph: CodeGraph, source: str, target: str, max_depth: int = 10) -> list[list[str]]:
    """Find all call/import paths from source to target using BFS."""
    adj: dict[str, list[str]] = {}
    for e in graph.edges:
        adj.setdefault(e.source, []).append(e.target)

    if source not in adj:
        return []

    paths = []
    queue = deque([(source, [source])])
    visited = {source}

    while queue:
        node, path = queue.popleft()
        if len(path) > max_depth:
            continue
        if node == target:
            paths.append(path)
            continue
        for neighbor in adj.get(node, []):
            new_path = path + [neighbor]
            if neighbor == target:
                paths.append(new_path)
            elif neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return paths


def impact_analysis(graph: CodeGraph, symbol: str, depth: int = 3) -> dict:
    """Find all symbols that would be affected if `symbol` changes."""
    reverse_adj: dict[str, list[str]] = {}
    forward_adj: dict[str, list[str]] = {}
    for e in graph.edges:
        reverse_adj.setdefault(e.target, []).append(e.source)
        forward_adj.setdefault(e.source, []).append(e.target)

    dependents = _bfs_collect(reverse_adj, symbol, depth)
    dependencies = _bfs_collect(forward_adj, symbol, depth)

    return {
        "symbol": symbol,
        "dependents": list(dependents),
        "dependencies": list(dependencies),
        "impact_count": len(dependents),
        "dependency_count": len(dependencies),
    }


def _bfs_collect(adj: dict[str, list[str]], start: str, max_depth: int) -> set[str]:
    collected = set()
    queue = deque([(start, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for neighbor in adj.get(node, []):
            if neighbor not in collected:
                collected.add(neighbor)
                queue.append((neighbor, depth + 1))
    return collected


def subgraph(graph: CodeGraph, symbols: list[str], depth: int = 1) -> CodeGraph:
    """Extract a subgraph containing only the given symbols and their neighbors up to `depth`."""
    keep_nodes = set(symbols)
    boundary = set(symbols)

    for _ in range(depth):
        for e in graph.edges:
            if e.source in boundary:
                keep_nodes.add(e.target)
            if e.target in boundary:
                keep_nodes.add(e.source)
        boundary = keep_nodes - boundary

    sub = CodeGraph()
    for n in graph.nodes:
        if n.id in keep_nodes:
            sub.add_node(n)
    for e in graph.edges:
        if e.source in keep_nodes and e.target in keep_nodes:
            sub.add_edge(e)
    return sub
