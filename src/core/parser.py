from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ASTNode:
    type: str
    start_byte: int
    end_byte: int
    start_point: tuple[int, int]
    end_point: tuple[int, int]
    is_named: bool
    text: Optional[str] = None
    children: list["ASTNode"] = field(default_factory=list)


@dataclass
class ParseResult:
    source_path: str
    language: str
    root: ASTNode
    source_text: str


class BaseParser(ABC):
    @abstractmethod
    def parse_file(self, filepath: str) -> ParseResult:
        ...

    @abstractmethod
    def parse_bytes(self, source: bytes, filepath: str = "<input>") -> ParseResult:
        ...
