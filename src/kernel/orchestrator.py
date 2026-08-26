from typing import Optional
from src.contracts.types import FileAnalysis, QueryResult
from src.graph.relations import CodeGraph
from src.graph.traversal import impact_analysis, reverse_lookup, forward_lookup, find_paths
from src.index.workspace import WorkspaceIndex
from src.query.engine import QueryEngine
from src.ai.explain import generate_explanation, summarize
from src.watch.incremental_parser import IncrementalParser
from .context import AnalysisContext
from .pipeline import Pipeline, ParseStep, NormalizeStep, AnalyzeStep, GraphStep


class SystemKernel:
    """Central orchestrator — every CLI command flows through this."""

    def __init__(self, workspace: Optional[WorkspaceIndex] = None):
        self.workspace = workspace or WorkspaceIndex()
        self.pipeline = (
            Pipeline()
            .add_step(ParseStep())
            .add_step(NormalizeStep())
            .add_step(AnalyzeStep())
            .add_step(GraphStep())
        )
        self._incremental = IncrementalParser(self.workspace)

    def analyze(self, filepath: str, library: Optional[str] = None) -> AnalysisContext:
        ctx = AnalysisContext(filepath=filepath)
        ctx.__dict__["_library"] = library

        cached = self.workspace.get(filepath)
        if cached:
            ctx.analysis = cached
            ctx.language = cached.language
            ctx.filepath = cached.file
            graph_ctx = AnalysisContext(filepath=filepath)
            graph_ctx.analysis = cached
            GraphStep().execute(graph_ctx)
            ctx.graph = graph_ctx.graph
            return ctx

        ctx = self.pipeline.run(ctx)
        if not ctx.has_error() and ctx.analysis:
            self.workspace.index_file(filepath, ctx.analysis)
        return ctx

    def analyze_incremental(self, filepath: str, library: Optional[str] = None) -> Optional[FileAnalysis]:
        def _parse(fp: str) -> FileAnalysis:
            ctx = self.analyze(fp, library=library)
            if ctx.analysis:
                return ctx.analysis
            raise RuntimeError(ctx.error or "unknown error")
        return self._incremental.parse_if_changed(filepath, _parse)

    def query(self, filepath: str, intent: str, library: Optional[str] = None) -> QueryResult:
        ctx = self.analyze(filepath, library=library)
        if ctx.has_error() or not ctx.analysis:
            return QueryResult(intent=intent, count=0, error=ctx.error)
        qe = QueryEngine(ctx.analysis, graph=ctx.graph)
        return qe.query(intent)

    def query_symbol(self, filepath: str, name: str, library: Optional[str] = None) -> QueryResult:
        ctx = self.analyze(filepath, library=library)
        if ctx.has_error() or not ctx.analysis:
            return QueryResult(intent=f"symbol:{name}", count=0, error=ctx.error)
        qe = QueryEngine(ctx.analysis, graph=ctx.graph)
        return qe.by_symbol(name)

    def query_tag(self, filepath: str, tag: str, library: Optional[str] = None) -> QueryResult:
        ctx = self.analyze(filepath, library=library)
        if ctx.has_error() or not ctx.analysis:
            return QueryResult(intent=f"tag:{tag}", count=0, error=ctx.error)
        qe = QueryEngine(ctx.analysis, graph=ctx.graph)
        return qe.by_tag(tag)

    def explain(self, filepath: str, mode: str = "explain",
                api_key: Optional[str] = None, library: Optional[str] = None,
                include_graph: bool = True) -> str:
        ctx = self.analyze(filepath, library=library)
        if ctx.has_error() or not ctx.analysis:
            return f"Error: {ctx.error}"

        graph = ctx.graph if include_graph else None
        return generate_explanation(ctx.analysis, mode=mode, api_key=api_key, graph=graph)

    def summarize(self, filepath: str, library: Optional[str] = None) -> str:
        ctx = self.analyze(filepath, library=library)
        if ctx.has_error() or not ctx.analysis:
            return f"Error: {ctx.error}"
        return summarize(ctx.analysis)

    def graph_traverse(self, filepath: str, symbol: str, traversal: str = "forward",
                       target: Optional[str] = None, library: Optional[str] = None) -> dict:
        ctx = self.analyze(filepath, library=library)
        if ctx.has_error() or not ctx.graph:
            return {"error": ctx.error or "No graph available"}

        if traversal == "reverse":
            return {"symbol": symbol, "results": reverse_lookup(ctx.graph, symbol)}
        elif traversal == "impact":
            return impact_analysis(ctx.graph, symbol)
        elif traversal == "path" and target:
            return {"symbol": symbol, "target": target,
                    "paths": find_paths(ctx.graph, symbol, target)}
        else:
            return {"symbol": symbol, "results": forward_lookup(ctx.graph, symbol)}

    def report(self, target_dir: str, library: Optional[str] = None) -> dict:
        from pathlib import Path
        reports = []
        extensions = {"py", "js", "ts", "go", "rb", "java", "rs", "c", "cpp", "cs", "kt", "php"}

        for f in sorted(Path(target_dir).rglob("*")):
            if not f.is_file():
                continue
            suffix = f.suffix.lstrip(".")
            if suffix not in extensions:
                continue
            try:
                ctx = self.analyze(str(f), library=library)
                if ctx.analysis:
                    reports.append(ctx.analysis)
            except Exception:
                pass

        from src.graph.builder import build_from_reports
        graph = build_from_reports(reports)
        return {
            "target": target_dir,
            "files_analyzed": len(reports),
            "graph": {
                "nodes": [{"id": n.id, "label": n.label, "kind": n.kind} for n in graph.nodes],
                "edges": [{"source": e.source, "target": e.target, "relation": e.relation} for e in graph.edges],
            },
        }
