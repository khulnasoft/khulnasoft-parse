from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SourceLocation:
    file: str = ""
    start_byte: int = 0
    end_byte: int = 0

    def to_dict(self) -> dict:
        return {"file": self.file, "start_byte": self.start_byte, "end_byte": self.end_byte}


@dataclass
class Complexity:
    cyclomatic: int = 0
    cognitive: int = 0

    def to_dict(self) -> dict:
        return {"cyclomatic": self.cyclomatic, "cognitive": self.cognitive}


@dataclass
class Symbol:
    name: str
    kind: str = "unknown"
    visibility: str = "public"
    tags: list[str] = field(default_factory=list)
    complexity: Optional[Complexity] = None
    location: Optional[SourceLocation] = None
    docstring: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"name": self.name, "kind": self.kind, "visibility": self.visibility, "tags": self.tags}
        if self.complexity:
            d["complexity"] = self.complexity.to_dict()
        if self.location:
            d["location"] = {"file": self.location.file, "start_byte": self.location.start_byte,
                             "end_byte": self.location.end_byte}
        if self.docstring:
            d["docstring"] = self.docstring
        return d


@dataclass
class ImportEdge:
    source: str = ""
    names: list[str] = field(default_factory=list)
    kind: str = "module"

    def to_dict(self) -> dict:
        return {"source": self.source, "names": self.names, "kind": self.kind}


@dataclass
class DependencyEdge:
    source: str = ""
    target: str = ""
    relation: str = ""
    location: Optional[SourceLocation] = None

    def to_dict(self) -> dict:
        d = {"source": self.source, "target": self.target, "relation": self.relation}
        if self.location:
            d["location"] = {"file": self.location.file, "start_byte": self.location.start_byte,
                             "end_byte": self.location.end_byte}
        return d


@dataclass
class FileAnalysis:
    file: str = ""
    language: str = ""
    symbols: list[Symbol] = field(default_factory=list)
    dependencies: list[DependencyEdge] = field(default_factory=list)
    imports: list[ImportEdge] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "language": self.language,
            "symbols": [s.to_dict() for s in self.symbols],
            "dependencies": [d.to_dict() for d in self.dependencies],
            "imports": [i.to_dict() for i in self.imports],
        }


@dataclass
class QueryResult:
    intent: str = ""
    matches: list[dict] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    count: int = 0
    error: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"intent": self.intent, "matches": self.matches, "symbols": self.symbols, "count": self.count}
        if self.error:
            d["error"] = self.error
        return d
