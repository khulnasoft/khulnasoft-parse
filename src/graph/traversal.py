from collections import deque
from .relations import CodeGraph


def _match_id(stored_id: str, query: str) -> bool:
    """Match a graph node ID against a query.

    Graph node IDs are file-qualified (``file.py:symbol_name``).
    Matches if the full ID equals *query* or if the bare symbol
    portion (after the last ``:``) equals *query*.
    """
    return stored_id == query or stored_id.split(":", 1)[-1] == query


def reverse_lookup(graph: CodeGraph, symbol: str) -> list[dict]:
    """Find everything that depends on a given symbol."""
    results = []
    for e in graph.edges:
        if _match_id(e.target, symbol):
            results.append({"caller": e.source, "relation": e.relation, "target": e.target})
    return results


def forward_lookup(graph: CodeGraph, symbol: str) -> list[dict]:
    """Find everything a given symbol depends on."""
    results = []
    for e in graph.edges:
        if _match_id(e.source, symbol):
            results.append({"caller": e.source, "relation": e.relation, "target": e.target})
    return results


def find_paths(graph: CodeGraph, source: str, target: str, max_depth: int = 10) -> list[list[str]]:
    """Enumerate all simple paths from source to target (no repeated nodes per path).

    Uses DFS with per-path cycle detection so alternative routes through shared
    intermediate nodes are not pruned.
    """
    adj: dict[str, list[str]] = {}
    for e in graph.edges:
        adj.setdefault(e.source, []).append(e.target)

    matched_source = next((nid for nid in adj if _match_id(nid, source)), None)
    if matched_source is None:
        return []

    paths: list[list[str]] = []

    def dfs(current: str, path: list[str]) -> None:
        if len(path) > max_depth:
            return
        if _match_id(current, target):
            paths.append(list(path))
            return
        for neighbor in adj.get(current, []):
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    dfs(matched_source, [matched_source])
    return paths


def impact_analysis(graph: CodeGraph, symbol: str, depth: int = 3) -> dict:
    """Find all symbols that would be affected if *symbol* changes."""
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
    matched_start = _find_first_id(adj, start)
    if matched_start is None:
        return collected
    queue = deque([(matched_start, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for neighbor in adj.get(node, []):
            if neighbor not in collected:
                collected.add(neighbor)
                queue.append((neighbor, depth + 1))
    return collected


def _find_first_id(ids: dict[str, list[str]] | set[str], query: str) -> str | None:
    """Return the first stored ID matching *query*, or *query* itself."""
    for stored in ids:
        if _match_id(stored, query):
            return stored
    return query


def subgraph(graph: CodeGraph, symbols: list[str], depth: int = 1) -> CodeGraph:
    """Extract a subgraph containing only the given symbols and their neighbours up to *depth*."""
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
