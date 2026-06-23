from abc import ABC, abstractmethod
from typing import Optional
from .types import FileAnalysis, QueryResult


class ParserInterface(ABC):
    @abstractmethod
    def parse_file(self, filepath: str) -> FileAnalysis:
        ...

    @abstractmethod
    def parse_bytes(self, source: bytes, filepath: str = "<input>") -> FileAnalysis:
        ...


class AnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, analysis: FileAnalysis) -> FileAnalysis:
        ...


class GraphInterface(ABC):
    @abstractmethod
    def build(self, analyses: list[FileAnalysis]) -> "CodeGraph":
        ...

    @abstractmethod
    def find_path(self, source: str, target: str) -> list[list[str]]:
        ...

    @abstractmethod
    def reverse_lookup(self, symbol: str) -> list[str]:
        ...


class QueryInterface(ABC):
    @abstractmethod
    def query(self, intent: str, analysis: FileAnalysis) -> QueryResult:
        ...


class AIInterface(ABC):
    @abstractmethod
    def analyze(self, analysis: FileAnalysis, mode: str = "explain") -> str:
        ...


class IndexInterface(ABC):
    @abstractmethod
    def store(self, analysis: FileAnalysis) -> None:
        ...

    @abstractmethod
    def load(self, filepath: str) -> Optional[FileAnalysis]:
        ...

    @abstractmethod
    def search_by_tag(self, tag: str) -> list[FileAnalysis]:
        ...

    @abstractmethod
    def search_by_name(self, name: str) -> list[FileAnalysis]:
        ...
