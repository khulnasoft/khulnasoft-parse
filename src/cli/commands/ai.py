import json
from src.core.parser import BaseParser, ParseResult, ASTNode
from src.core.ast_normalizer import normalize
from src.semantic.analyzer import analyze
from src.ai.explain import generate_explanation, summarize


def run(args: dict) -> None:
    filepath = args.get("file")
    mode = args.get("mode", "explain")
    api_key = args.get("api_key") or __import__("os").environ.get("AI_API_KEY")

    from examples.parse_example import get_language as _gl, _make_parser as _mp
    from pathlib import Path

    src = Path(filepath).read_bytes()
    lang_name = Path(filepath).suffix.lstrip(".") or "python"
    lang_name = {"js": "javascript", "ts": "typescript", "py": "python", "rb": "ruby"}.get(lang_name, lang_name)
    library = args.get("library")

    language = _gl(lang_name, library)
    parser_inst = _mp(language)
    tree = parser_inst.parse(src)

    from src.core.ast_normalizer import normalize
    from src.semantic.analyzer import analyze

    result = ParseResult(source_path=filepath, language=lang_name,
                         root=ASTNode(type=tree.root_node.type,
                                      start_byte=tree.root_node.start_byte,
                                      end_byte=tree.root_node.end_byte,
                                      start_point=tree.root_node.start_point,
                                      end_point=tree.root_node.end_point,
                                      is_named=tree.root_node.is_named,
                                      children=[_to_astn(tree.root_node.child(i), src) for i in range(tree.root_node.child_count) if tree.root_node.child(i).is_named]),
                         source_text=src.decode("utf-8", "replace"))

    normalized = normalize(result)
    report = analyze(result, normalized)

    if args.get("summary"):
        print(summarize(report))
        return

    explanation = generate_explanation(report, mode=mode, api_key=api_key)
    print(explanation)


def _to_astn(ts_node, src: bytes):
    children = []
    for i in range(ts_node.child_count):
        c = ts_node.child(i)
        if c.is_named:
            children.append(_to_astn(c, src))
    text = None
    if ts_node.child_count == 0:
        text = src[ts_node.start_byte:ts_node.end_byte].decode("utf-8", "replace")
    return ASTNode(
        type=ts_node.type,
        start_byte=ts_node.start_byte,
        end_byte=ts_node.end_byte,
        start_point=ts_node.start_point,
        end_point=ts_node.end_point,
        is_named=ts_node.is_named,
        text=text,
        children=children,
    )
