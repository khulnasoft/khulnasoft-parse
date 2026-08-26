# 🔬 khulnasoft-parse

<p>
  <b>🧬 Multi‑layer Static + Semantic + Graph + AI Code Intelligence Engine</b>
</p>

[![Visual Studio](https://img.shields.io/visual-studio-marketplace/i/khulnasoft.khulnasoft?label=Visual%20Studio&logo=visualstudio)](https://marketplace.visualstudio.com/items?itemName=khulnasoft.khulnasoft)
[![JetBrains](https://img.shields.io/jetbrains/plugin/d/20540?label=JetBrains)](https://plugins.jetbrains.com/plugin/20540-khulnasoft/)
[![Open VSX](https://img.shields.io/open-vsx/dt/khulnasoft/khulnasoft?label=Open%20VSX)](https://open-vsx.org/extension/khulnasoft/khulnasoft)

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        🖥️  CLI Layer                            │
│   parse │ inspect │ query │ ai │ report │ diff │ watch          │
└───────────────────────────┬──────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                    🧠  System Kernel                             │
│               Pipeline: Parse → Normalize → Analyze → Graph      │
└───────────────────────────┬──────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┬────────────────┐
              ▼             ▼             ▼                ▼
┌─────────────────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐
│  📐  AST Engine     │ │ 🧬      │ │ 🌐       │ │ 🤖           │
│  (tree-sitter)      │ │ Semantic│ │ Graph    │ │ AI Engine    │
│  30+ languages      │ │ Layer   │ │ Engine   │ │ explain      │
│                     │ │ tags    │ │ traversal│ │ review       │
│                     │ │ intent  │ │ impact   │ │ design       │
└─────────────────────┘ └─────────┘ └──────────┘ └──────────────┘
                            │             │
                            └──────┬──────┘
                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                    💾  Index / Memory Layer                      │
│              SQLite Store │ LRU Cache │ Workspace Manager        │
│              File Watcher │ Incremental Parser                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Capability | v1 | v2 |
|---|---|---|
| AST parsing (30+ languages) | ✅ | ✅🔥 |
| Tree‑sitter query engine | ✅ | ✅ unified |
| **Semantic understanding** | ❌ | ✅ tags + intents |
| **Dependency graph** | ❌ | ✅ traversal + impact analysis |
| **AI reasoning** | ❌ | ✅ explain / review / design |
| **Intent‑based search** | ❌ | ✅ `--intent "auth"` |
| **AST diff** | ❌ | ✅ `parse diff old.py new.py` |
| **Repo memory / caching** | ❌ | ✅ SQLite index |
| **Incremental / watch mode** | ❌ | ✅ file watcher |

---

## ⚡ Quick Start

```bash
# 1. Download the native parser binary
./download_parse.sh

# 2. Parse a file — see AST
./parse -file examples/example.js -named_only

# 3. Parse with semantic analysis (v2)
pip install tree-sitter tree-sitter-python tree-sitter-javascript
python -m src.cli.main parse test_files/test.py --output semantic

# 4. AI-powered code review (dry run)
python -m src.cli.main ai test_files/test.py --mode review

# 5. Dependency graph
python -m src.cli.main inspect test_files/test.py --mode graph

# 6. Intent‑based query
python -m src.cli.main inspect test.py --mode query --query "intent:database"
```

---

## 🧬 v2 Modules

| Module | Path | Purpose |
|---|---|---|
| **Core** | `src/core/` | Tree‑sitter wrapper, AST normalization |
| **Semantic** | `src/semantic/` | Tags, intent inference, code analysis |
| **Graph** | `src/graph/` | Builder, traversal, impact analysis, export (JSON/D3/Gexf) |
| **Query** | `src/query/` | 2‑stage engine: intent → filters → graph traversal |
| **Index** | `src/index/` | SQLite store, LRU cache, workspace manager |
| **AI** | `src/ai/` | LLM wrapper, prompts, graph‑native explain/review/design |
| **Watch** | `src/watch/` | File watcher, incremental parser |
| **Contracts** | `src/contracts/` | Unified data types & interfaces (system contract) |
| **Kernel** | `src/kernel/` | Orchestrator, context, pipeline (the "brain") |
| **CLI** | `src/cli/` | Entrypoint, 5 commands |

---

## 📋 CLI Commands

```text
parse   <file>          Parse → normalized / semantic / sexp output
inspect <file>          AST / semantic / graph / query / traverse modes
ai      <file>          AI explanation, code review, or design reconstruction
report  <dir>           Architecture report + dependency graph for a directory
diff    <old> <new>     AST‑level diff with added / removed / modified nodes
```

---

## 🔍 Query Support

Queries follow [tree‑sitter code navigation conventions](https://tree-sitter.github.io/tree-sitter/code-navigation-systems).  
Most captures include `@doc`. `@definition.*` also captures `@khulnasoft.parameters`.

| Capture | Python | TS | JS | Go | Java | C++ | PHP | Ruby | C# | Perl | Kotlin | Dart | Bash | C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `@definition.class` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `@definition.function` | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | N/A | N/A | ✓ | ✓ | ✓ | ✓ | ✓ |
| `@definition.method` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `@definition.import` | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | N/A | ✓ | ✗ | ✓ | ✓ | ✗ | N/A | ✓ |
| `@reference.call` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

<sup>Full table with all 16 captures → see [QUERY_PATTERNS.md](./QUERY_PATTERNS.md)</sup>

### Query predicates

```text
#eq? / #not-eq?         Value equality check
#has-parent?            Parent node type check
#match? / #not-match?   Regex match
#select-adjacent!       Select contiguous nodes
#set!                   Metadata side‑effect
#strip!                 Regex text removal
```

---

## 🌐 Supported Languages (30+)

```
ada  c  cpp  csharp  css  dart  go  hcl  html  java  javascript
json  julia  kotlin  latex  markdown  ocaml  ocaml_interface  perl
php  protobuf  python  ruby  rust  shell  svelte  swift  toml
tree_sitter_query  tsx  typescript  vue  yaml
```

---

## 🧪 Testing

```bash
# Native parse binary tests
./test.sh

# Python parser tests (requires LANGUAGE_SO or skips gracefully)
python tests/parse_test.py --mode all
```

---

## 🤝 Contributing

1. Add test patterns in `test_files/`
2. Inspect the AST with `./parse -file test_files/<file>`
3. Write or update queries in `queries/`
4. Run `./goldens.sh` to validate
5. Open a PR!

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://khulnasoft.com">KhulnaSoft</a> &amp; contributors · 
  <a href="https://github.com/khulnasoft/khulnasoft-parse/issues">Report issue</a> · 
  <a href="https://khulnasoft.canny.io/feature-requests/">Request feature</a></sub>
</p>
