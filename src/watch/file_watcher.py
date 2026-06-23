import os
import time
from pathlib import Path
from typing import Callable, Optional


class FileWatcher:
    def __init__(self, root: str, extensions: set[str] | None = None, poll_interval: float = 1.0):
        self.root = Path(root)
        self.extensions = extensions or {".py", ".js", ".ts", ".go", ".rb", ".java", ".rs", ".c", ".cpp"}
        self.poll_interval = poll_interval
        self._mtimes: dict[str, float] = {}
        self._running = False

    def _get_files(self) -> list[Path]:
        files = []
        for ext in self.extensions:
            files.extend(self.root.rglob(f"*{ext}"))
        return files

    def _snapshot(self) -> dict[str, float]:
        snap = {}
        for f in self._get_files():
            try:
                snap[str(f)] = os.path.getmtime(f)
            except OSError:
                pass
        return snap

    def poll(self, on_change: Callable[[str], None]) -> list[str]:
        """Check for changes and call on_change for each changed file. Returns list of changed paths."""
        current = self._snapshot()
        changed = []
        for path, mtime in current.items():
            old = self._mtimes.get(path)
            if old is None or mtime > old:
                changed.append(path)
                on_change(path)
        self._mtimes = current
        return changed

    def watch(self, on_change: Callable[[str], None]) -> None:
        """Continuously poll for changes."""
        self._mtimes = self._snapshot()
        self._running = True
        print(f"Watching {self.root} for changes (extensions: {self.extensions})...")
        try:
            while self._running:
                changed = self.poll(on_change)
                if changed:
                    print(f"  Detected changes: {len(changed)} file(s)")
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            print("\nWatcher stopped.")
            self._running = False

    def stop(self) -> None:
        self._running = False
