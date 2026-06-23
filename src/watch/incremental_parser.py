import os
from pathlib import Path
from typing import Optional

from src.contracts.types import FileAnalysis
from src.index.workspace import WorkspaceIndex


class IncrementalParser:
    """Parses files only when they've changed since last parse."""

    def __init__(self, workspace: WorkspaceIndex):
        self.workspace = workspace
        self._timestamps: dict[str, float] = {}

    def needs_reparse(self, filepath: str) -> bool:
        try:
            current_mtime = os.path.getmtime(filepath)
            last_mtime = self._timestamps.get(filepath)
            return last_mtime is None or current_mtime > last_mtime
        except OSError:
            return True

    def parse_if_changed(self, filepath: str, parser_fn) -> Optional[FileAnalysis]:
        if not self.needs_reparse(filepath):
            cached = self.workspace.get(filepath)
            if cached:
                return cached
        try:
            analysis = parser_fn(filepath)
            self.workspace.index_file(filepath, analysis)
            self._timestamps[filepath] = os.path.getmtime(filepath)
            return analysis
        except Exception as e:
            print(f"  PARSE ERROR {filepath}: {e}")
            return None

    def parse_all(self, parser_fn) -> list[FileAnalysis]:
        results = []
        for f in self.workspace.find_source_files():
            fp = str(f)
            analysis = self.parse_if_changed(fp, parser_fn)
            if analysis:
                results.append(analysis)
        return results
