import json
import sqlite3
import os
from pathlib import Path
from typing import Optional
from src.contracts.types import FileAnalysis, Symbol, DependencyEdge, ImportEdge, SourceLocation


class AnalysisStore:
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = os.environ.get("PARSE_INDEX_DB", str(Path.cwd() / ".parse" / "index.db"))
        self.db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        c = self._conn
        c.execute("""CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY, language TEXT NOT NULL,
            analysis TEXT NOT NULL, updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT NOT NULL,
            name TEXT NOT NULL, kind TEXT NOT NULL, visibility TEXT DEFAULT 'public',
            tags TEXT DEFAULT '[]', start_byte INTEGER DEFAULT 0, end_byte INTEGER DEFAULT 0
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS deps (
            id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT NOT NULL,
            source TEXT NOT NULL, target TEXT NOT NULL, relation TEXT NOT NULL
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS idx_sym_name ON symbols(name)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_sym_tag ON symbols(tags)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_dep_target ON deps(target)")
        self._conn.commit()

    def store(self, analysis: FileAnalysis) -> None:
        c = self._conn
        c.execute("INSERT OR REPLACE INTO files (path, language, analysis) VALUES (?, ?, ?)",
                  (analysis.file, analysis.language, json.dumps(analysis.to_dict())))
        c.execute("DELETE FROM symbols WHERE file_path = ?", (analysis.file,))
        c.execute("DELETE FROM deps WHERE file_path = ?", (analysis.file,))
        for sym in analysis.symbols:
            c.execute(
                "INSERT INTO symbols (file_path, name, kind, visibility, tags, start_byte, end_byte) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (analysis.file, sym.name, sym.kind, sym.visibility, json.dumps(sym.tags),
                 sym.location.start_byte if sym.location else 0,
                 sym.location.end_byte if sym.location else 0))
        for dep in analysis.dependencies:
            c.execute("INSERT INTO deps (file_path, source, target, relation) VALUES (?, ?, ?, ?)",
                      (analysis.file, dep.source, dep.target, dep.relation))
        self._conn.commit()

    def load(self, filepath: str) -> Optional[FileAnalysis]:
        row = self._conn.execute(
            "SELECT analysis FROM files WHERE path = ?", (filepath,)).fetchone()
        if row:
            return self._analysis_from_dict(json.loads(row[0]))
        return None

    def search_by_tag(self, tag: str) -> list[FileAnalysis]:
        rows = self._conn.execute(
            "SELECT analysis FROM files WHERE path IN "
            "(SELECT DISTINCT file_path FROM symbols WHERE tags LIKE ?)",
            (f"%{tag}%",)).fetchall()
        return [self._analysis_from_dict(json.loads(r[0])) for r in rows]

    def search_by_name(self, name: str) -> list[FileAnalysis]:
        rows = self._conn.execute(
            "SELECT analysis FROM files WHERE path IN "
            "(SELECT DISTINCT file_path FROM symbols WHERE name LIKE ?)",
            (f"%{name}%",)).fetchall()
        return [self._analysis_from_dict(json.loads(r[0])) for r in rows]

    def list_files(self) -> list[str]:
        return [r[0] for r in self._conn.execute(
            "SELECT path FROM files ORDER BY path").fetchall()]

    def close(self):
        self._conn.close()

    @staticmethod
    def _analysis_from_dict(d: dict) -> FileAnalysis:
        from src.contracts.types import Complexity
        symbols = []
        for s in d.get("symbols", []):
            loc = None
            if "location" in s:
                loc_raw = s["location"]
                loc = SourceLocation(
                    file=loc_raw.get("file", d.get("file", "")),
                    start_byte=loc_raw.get("start_byte", 0),
                    end_byte=loc_raw.get("end_byte", 0),
                )
            elif "start_byte" in s:
                loc = SourceLocation(file=d.get("file", ""), start_byte=s.get("start_byte", 0),
                                     end_byte=s.get("end_byte", 0))
            complexity = None
            if "complexity" in s and s["complexity"]:
                complexity = Complexity(cyclomatic=s["complexity"].get("cyclomatic", 0),
                                        cognitive=s["complexity"].get("cognitive", 0))
            symbols.append(Symbol(
                name=s["name"], kind=s.get("kind", "unknown"),
                visibility=s.get("visibility", "public"), tags=s.get("tags", []),
                location=loc, complexity=complexity, docstring=s.get("docstring"),
            ))
        deps = []
        for dd in d.get("dependencies", []):
            dep_loc = None
            if "location" in dd and dd["location"]:
                dep_loc = SourceLocation(
                    file=dd["location"].get("file", ""),
                    start_byte=dd["location"].get("start_byte", 0),
                    end_byte=dd["location"].get("end_byte", 0),
                )
            deps.append(DependencyEdge(source=dd["source"], target=dd["target"],
                                       relation=dd.get("relation", ""), location=dep_loc))
        imports = [ImportEdge(source=i["source"], names=i.get("names", []), kind=i.get("kind", "module"))
                   for i in d.get("imports", [])]
        return FileAnalysis(file=d.get("file", ""), language=d.get("language", ""),
                            symbols=symbols, dependencies=deps, imports=imports)
