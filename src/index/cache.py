from typing import Optional
from src.contracts.types import FileAnalysis


class AnalysisCache:
    def __init__(self, max_entries: int = 1000):
        self._store: dict[str, FileAnalysis] = {}
        self._max = max_entries

    def get(self, filepath: str) -> Optional[FileAnalysis]:
        return self._store.get(filepath)

    def set(self, filepath: str, analysis: FileAnalysis) -> None:
        if len(self._store) >= self._max:
            self._evict()
        self._store[filepath] = analysis

    def invalidate(self, filepath: str) -> None:
        self._store.pop(filepath, None)

    def clear(self) -> None:
        self._store.clear()

    def has(self, filepath: str) -> bool:
        return filepath in self._store

    def _evict(self) -> None:
        if self._store:
            self._store.pop(next(iter(self._store)))
