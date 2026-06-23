import os
from pathlib import Path
from typing import Optional
from src.contracts.types import FileAnalysis
from .store import AnalysisStore
from .cache import AnalysisCache


PARSEABLE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".go", ".rb", ".java", ".rs",
                        ".c", ".cpp", ".cs", ".kt", ".php", ".swift", ".vue"}


class WorkspaceIndex:
    def __init__(self, root: str | None = None, db_path: str | None = None):
        self.root = Path(root or os.getcwd()).resolve()
        self.store = AnalysisStore(db_path=db_path)
        self.cache = AnalysisCache()

    def index_file(self, filepath: str, analysis: FileAnalysis) -> None:
        self.cache.set(filepath, analysis)
        self.store.store(analysis)

    def get(self, filepath: str) -> Optional[FileAnalysis]:
        cached = self.cache.get(filepath)
        if cached:
            return cached
        stored = self.store.load(filepath)
        if stored:
            self.cache.set(filepath, stored)
        return stored

    def search_by_tag(self, tag: str) -> list[FileAnalysis]:
        return self.store.search_by_tag(tag)

    def search_by_name(self, name: str) -> list[FileAnalysis]:
        return self.store.search_by_name(name)

    def list_indexed_files(self) -> list[str]:
        return self.store.list_files()

    def is_parseable(self, filepath: str) -> bool:
        return Path(filepath).suffix.lower() in PARSEABLE_EXTENSIONS

    def find_source_files(self) -> list[Path]:
        files = []
        for ext in PARSEABLE_EXTENSIONS:
            files.extend(self.root.rglob(f"*{ext}"))
        return sorted(set(files))
