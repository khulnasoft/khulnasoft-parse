from dataclasses import dataclass, field
from typing import Optional
from src.contracts.types import FileAnalysis
from src.core.parser import ParseResult
from src.core.ast_normalizer import NormalizedNode
from src.graph.relations import CodeGraph
from src.contracts.types import QueryResult


@dataclass
class AnalysisContext:
    filepath: str = ""
    language: str = ""
    source_text: str = ""

    parse_result: Optional[ParseResult] = None
    normalized_nodes: list[NormalizedNode] = field(default_factory=list)
    analysis: Optional[FileAnalysis] = None
    graph: Optional[CodeGraph] = None

    error: Optional[str] = None

    def has_error(self) -> bool:
        return self.error is not None

    def summary(self) -> str:
        lines = [f"File: {self.filepath}", f"Language: {self.language}"]
        if self.analysis:
            lines.append(f"Symbols: {len(self.analysis.symbols)}")
            lines.append(f"Dependencies: {len(self.analysis.dependencies)}")
            lines.append(f"Imports: {len(self.analysis.imports)}")
        if self.graph:
            lines.append(f"Graph nodes: {len(self.graph.nodes)}")
            lines.append(f"Graph edges: {len(self.graph.edges)}")
        if self.error:
            lines.append(f"Error: {self.error}")
        return "\n".join(lines)
