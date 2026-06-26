import json
from src.core.parser import ParseResult
from src.core.ast_normalizer import normalize, normalize_full, node_to_dict
from src.core.tree_sitter_utils import ts_node_to_astnode
from src.semantic.analyzer import analyze
from src.graph.builder import build
from src.graph.exporter import to_json as graph_json, to_d3
from src.graph.traversal import reverse_lookup, forward_lookup, find_paths, impact_analysis
from src.query.engine import QueryEngine


def run(args: dict) -> None:
    filepath = args.get("file")
    mode = args.get("mode", "ast")

    from examples.parse_example import get_language as _gl, _make_parser as _mp
    from pathlib import Path

    src = Path(filepath).read_bytes()
    lang_name = Path(filepath).suffix.lstrip(".") or "python"
    lang_name = {"js": "javascript", "ts": "typescript", "py": "python", "rb": "ruby"}.get(lang_name, lang_name)
    library = args.get("library")

    language = _gl(lang_name, library)
    parser_inst = _mp(language)
    tree = parser_inst.parse(src)

    result = ParseResult(source_path=filepath, language=lang_name,
                         root=ts_node_to_astnode(tree.root_node, src),
                         source_text=src.decode("utf-8", "replace"))

    if mode == "ast":
        full = normalize_full(result)
        print(json.dumps(node_to_dict(full), indent=2))
    elif mode == "semantic":
        normalized = normalize(result)
        report = analyze(result, normalized)
        print(json.dumps(report.to_dict(), indent=2))
    elif mode == "graph":
        normalized = normalize(result)
        report = analyze(result, normalized)
        graph = build(report)
        fmt = args.get("graph_format", "json")
        if fmt == "d3":
            print(to_d3(graph))
        else:
            print(graph_json(graph))
    elif mode == "query":
        normalized = normalize(result)
        report = analyze(result, normalized)
        query_str = args.get("query", "")
        qe = QueryEngine(report)
        if query_str.startswith("intent:"):
            qr = qe.query(query_str[7:])
        elif query_str.startswith("tag:"):
            qr = qe.by_tag(query_str[4:])
        else:
            qr = qe.by_symbol(query_str)
        print(json.dumps(qr.to_dict(), indent=2))
    elif mode == "traverse":
        normalized = normalize(result)
        report = analyze(result, normalized)
        graph = build(report)
        traversal_type = args.get("traverse", "forward")
        symbol = args.get("symbol", "")
        if traversal_type == "reverse":
            results = reverse_lookup(graph, symbol)
        elif traversal_type == "impact":
            results = impact_analysis(graph, symbol)
        elif traversal_type == "path":
            target = args.get("target", "")
            results = find_paths(graph, symbol, target)
        else:
            results = forward_lookup(graph, symbol)
        print(json.dumps(results, indent=2))
    else:
        print(f"Unknown inspect mode: {mode}")
