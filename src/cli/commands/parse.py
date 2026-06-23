import json
from src.core.parser import ParseResult, ASTNode
from src.core.ast_normalizer import normalize, normalize_full, node_to_dict
from src.semantic.analyzer import analyze


def run(args: dict) -> None:
    filepath = args.get("file")
    output = args.get("output", "ast")

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
                         root=ASTNode(type=tree.root_node.type, start_byte=tree.root_node.start_byte,
                                      end_byte=tree.root_node.end_byte, start_point=tree.root_node.start_point,
                                      end_point=tree.root_node.end_point, is_named=tree.root_node.is_named,
                                      children=[_ts_to_astn(tree.root_node.child(i), src)
                                                for i in range(tree.root_node.child_count)
                                                if tree.root_node.child(i).is_named]),
                         source_text=src.decode("utf-8", "replace"))

    if output == "ast":
        full = normalize_full(result)
        print(json.dumps(node_to_dict(full), indent=2))
    elif output == "normalized":
        normalized = normalize(result)
        print(json.dumps([node_to_dict(n) for n in normalized], indent=2))
    elif output == "semantic":
        normalized = normalize(result)
        report = analyze(result, normalized)
        print(json.dumps(report.to_dict(), indent=2))
    elif output == "sexp":
        from src.core.ast_util import to_sexp
        result_obj = ParseResult(source_path=filepath, language=lang_name,
                                 root=_ts_to_astn(tree.root_node, src), source_text=src.decode("utf-8", "replace"))
        print(to_sexp(result_obj.root))
    else:
        print(f"Unknown output format: {output}")


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
