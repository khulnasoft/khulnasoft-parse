import json
from pathlib import Path
from src.core.parser import ParseResult, ASTNode
from src.core.ast_normalizer import normalize
from src.semantic.analyzer import analyze
from src.graph.builder import build, build_from_reports
from src.graph.exporter import to_json as graph_json


def run(args: dict) -> None:
    target = Path(args.get("target", "."))
    library = args.get("library")

    from examples.parse_example import get_language as _gl, _make_parser as _mp

    reports = []
    extensions = {"py", "js", "ts", "go", "rb", "java", "rs", "c", "cpp", "cs", "kt", "php"}

    for f in sorted(target.rglob("*")):
        if not f.is_file():
            continue
        suffix = f.suffix.lstrip(".")
        if suffix not in extensions:
            continue

        try:
            src = f.read_bytes()
            lang_name = {"js": "javascript", "ts": "typescript", "py": "python",
                         "rb": "ruby", "rs": "rust"}.get(suffix, suffix)
            language = _gl(lang_name, library)
            parser_inst = _mp(language)
            tree = parser_inst.parse(src)

            result = ParseResult(source_path=str(f), language=lang_name,
                                 root=_ts_to_astn(tree.root_node, src), source_text=src.decode("utf-8", "replace"))
            normalized = normalize(result)
            report = analyze(result, normalized)
            reports.append(report)
        except Exception as e:
            print(f"  SKIP {f}: {e}", file=__import__("sys").stderr)

    if not reports:
        print(json.dumps({"error": "No parseable files found", "target": str(target)}))
        return

    if args.get("graph"):
        graph = build_from_reports(reports)
        print(graph_json(graph))
    else:
        combined = {
            "target": str(target),
            "files_analyzed": len(reports),
            "reports": [r.to_dict() for r in reports],
        }
        print(json.dumps(combined, indent=2))


def _ts_to_astn(ts_node, src: bytes):
    children = []
    for i in range(ts_node.child_count):
        c = ts_node.child(i)
        if c.is_named:
            children.append(_ts_to_astn(c, src))
    text = None
    if ts_node.child_count == 0:
        text = src[ts_node.start_byte:ts_node.end_byte].decode("utf-8", "replace")
    return ASTNode(type=ts_node.type, start_byte=ts_node.start_byte, end_byte=ts_node.end_byte,
                   start_point=ts_node.start_point, end_point=ts_node.end_point, is_named=ts_node.is_named,
                   text=text, children=children)
