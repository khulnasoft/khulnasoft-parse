from src.contracts.types import FileAnalysis, QueryResult
from src.graph.relations import CodeGraph
from src.graph.traversal import forward_lookup, reverse_lookup, find_paths
from .intent_map import resolve_intent, list_intents


class QueryEngine:
    def __init__(self, analysis: FileAnalysis, graph: CodeGraph | None = None):
        self.analysis = analysis
        self.graph = graph

    def query(self, intent: str) -> QueryResult:
        """Two-stage query: intent → semantic filters → graph traversal."""
        config = resolve_intent(intent)
        if not config:
            return QueryResult(intent=intent, count=0)

        # Stage 1: Intent → semantic filters
        target_tags = set(config.get("tags", []))
        keywords = config.get("keywords", [])

        matches = []
        matched_symbols = set()

        for sym in self.analysis.symbols:
            score = 0
            reasons = []

            if target_tags and target_tags.intersection(sym.tags):
                score += 2
                reasons.append("tag_match")

            text = f"{sym.name} {sym.docstring or ''}".lower()
            for kw in keywords:
                if kw.lower() in text:
                    score += 1
                    reasons.append(f"keyword:{kw}")
                    break

            if score > 0:
                matched_symbols.add(sym.name)
                matches.append({
                    "symbol": sym.name,
                    "kind": sym.kind,
                    "tags": sym.tags,
                    "score": score,
                    "reasons": reasons,
                    "intent": intent,
                })

        # Stage 2: Graph traversal for matched symbols
        graph_edges = []
        if self.graph and matched_symbols:
            for sym_name in list(matched_symbols)[:5]:
                for e in self.graph.edges:
                    if e.source == sym_name:
                        graph_edges.append({"source": e.source, "target": e.target, "relation": e.relation})
                    elif e.target == sym_name:
                        graph_edges.append({"source": e.source, "target": e.target, "relation": e.relation})

        return QueryResult(
            intent=intent,
            matches=matches,
            symbols=sorted(matched_symbols),
            count=len(matches),
        )

    def by_symbol(self, name: str) -> QueryResult:
        matches = []
        for sym in self.analysis.symbols:
            if name.lower() in sym.name.lower():
                matches.append({
                    "symbol": sym.name,
                    "kind": sym.kind,
                    "tags": sym.tags,
                    "location": sym.location.to_dict() if sym.location else None,
                })
        return QueryResult(intent=f"symbol:{name}", matches=matches,
                           symbols=[m["symbol"] for m in matches], count=len(matches))

    def by_tag(self, tag: str) -> QueryResult:
        matches = []
        for sym in self.analysis.symbols:
            if tag in sym.tags:
                matches.append({"symbol": sym.name, "kind": sym.kind, "tags": sym.tags})
        return QueryResult(intent=f"tag:{tag}", matches=matches,
                           symbols=[m["symbol"] for m in matches], count=len(matches))

    def graph_query(self, symbol: str, direction: str = "forward") -> list[dict]:
        if not self.graph:
            return []
        if direction == "reverse":
            return reverse_lookup(self.graph, symbol)
        elif direction == "path":
            return []
        return forward_lookup(self.graph, symbol)
