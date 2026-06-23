from src.contracts.types import FileAnalysis
from src.graph.relations import CodeGraph
from .engine import AIEngine


def generate_explanation(analysis: FileAnalysis, mode: str = "explain",
                         api_key: str | None = None, graph: CodeGraph | None = None) -> str:
    engine = AIEngine(api_key=api_key)
    return engine.analyze(analysis, mode=mode, graph=graph)


def summarize(analysis: FileAnalysis) -> str:
    lines = [f"File: {analysis.file}", f"Language: {analysis.language}", ""]
    if analysis.symbols:
        lines.append(f"Symbols ({len(analysis.symbols)}):")
        for s in analysis.symbols:
            tags = f" [{', '.join(s.tags)}]" if s.tags else ""
            comp = ""
            if s.complexity:
                comp = f" (cyclo={s.complexity.cyclomatic}, cog={s.complexity.cognitive})"
            loc = ""
            if s.location:
                loc = f" [{s.location.start_byte}-{s.location.end_byte}]"
            lines.append(f"  {s.visibility} {s.kind} {s.name}{comp}{tags}{loc}")
    if analysis.imports:
        lines.append(f"\nImports ({len(analysis.imports)}):")
        for i in analysis.imports:
            lines.append(f"  from {i.source} import {', '.join(i.names) if i.names else '*'}")
    if analysis.dependencies:
        lines.append(f"\nDependencies ({len(analysis.dependencies)}):")
        for d in analysis.dependencies:
            lines.append(f"  {d.source} -> {d.target} ({d.relation})")
    return "\n".join(lines)
