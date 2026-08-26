import json
from src.core.parser import ParseResult
from src.core.ast_normalizer import normalize
from src.core.tree_sitter_utils import ts_node_to_astnode
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

    result = ParseResult(source_path=filepath, language=lang_name,
                         root=ts_node_to_astnode(tree.root_node, src),
                         source_text=src.decode("utf-8", "replace"))

    normalized = normalize(result)
    report = analyze(result, normalized)

    if args.get("summary"):
        print(summarize(report))
        return

    explanation = generate_explanation(report, mode=mode, api_key=api_key)
    print(explanation)
