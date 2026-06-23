#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path
from tree_sitter import Language, Parser

_HAS_SET_LANGUAGE = hasattr(Parser, "set_language")


def _make_parser(language):
    if _HAS_SET_LANGUAGE:
        p = Parser()
        p.set_language(language)
        return p
    return Parser(language)


def node_to_json(node, source_bytes):
    d = {
        "type": node.type,
        "start_byte": node.start_byte,
        "end_byte": node.end_byte,
        "start_point": list(node.start_point),
        "end_point": list(node.end_point),
        "is_named": node.is_named,
    }
    if node.child_count == 0:
        text = source_bytes[node.start_byte:node.end_byte].decode("utf-8", "replace")
        d["text"] = text
    if node.child_count > 0:
        d["children"] = [node_to_json(node.child(i), source_bytes) for i in range(node.child_count)]
    return d


def node_to_sexp(node, source_bytes, indent=0):
    pad = "  " * indent
    if node.is_named:
        label = node.type
    else:
        label = f"'{source_bytes[node.start_byte:node.end_byte].decode('utf-8', 'replace')}'"
    if node.child_count == 0:
        text = source_bytes[node.start_byte:node.end_byte].decode("utf-8", "replace")
        return f"{pad}({label} {json.dumps(text)})"
    parts = [f"{pad}({label}"]
    for i in range(node.child_count):
        parts.append(node_to_sexp(node.child(i), source_bytes, indent + 1))
    parts.append(f"{pad})")
    return "\n".join(parts)


def get_language(lang_name: str, lang_lib: str | None):
    if lang_lib:
        if _HAS_SET_LANGUAGE:
            return Language(lang_lib, lang_name)
        import ctypes
        lib = ctypes.CDLL(lang_lib)
        func_name = f"tree_sitter_{lang_name.replace('-', '_')}"
        func = getattr(lib, func_name)
        func.restype = ctypes.py_object
        capsule = func()
        return Language(capsule)
    import importlib
    mod = importlib.import_module(f"tree_sitter_{lang_name}")
    return Language(mod.language())


def main():
    parser = argparse.ArgumentParser(description="Parse source file with tree-sitter")
    parser.add_argument("file", help="Path to source file")
    parser.add_argument("--language", "-l", help="Language name (auto-detected from extension if omitted)")
    parser.add_argument("--library", "-L", help="Path to compiled language .so")
    parser.add_argument("--format", "-f", choices=["json", "sexp"], default="json", help="Output format")
    args = parser.parse_args()

    src_path = Path(args.file)
    source = src_path.read_bytes()

    lang_name = args.language or src_path.suffix.lstrip(".") or "python"
    lang_name = {"js": "javascript", "ts": "typescript", "py": "python", "rb": "ruby"}.get(lang_name, lang_name)

    language = get_language(lang_name, args.library)
    parser_inst = _make_parser(language)
    tree = parser_inst.parse(source)

    if args.format == "sexp":
        print(node_to_sexp(tree.root_node, source))
    else:
        ast = node_to_json(tree.root_node, source)
        print(json.dumps(ast, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
