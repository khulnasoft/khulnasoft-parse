#!/usr/bin/env python3
"""
Minimal example: parse a source file with tree-sitter and print a JSON-like AST.

Notes:
- Requires `tree_sitter` Python package (pip install tree_sitter).
- Requires a compiled language .so/.dylib for the target language.
  You can build with tree-sitter CLI or pre-download language library build.
- Update LANGUAGE_SO and LANGUAGE_NAME below.
"""
import json
import sys
from tree_sitter import Language, Parser

# Path to a compiled shared library containing one or more languages.
# Example: build/my-languages.so which includes 'python' or 'javascript' grammars.
LANGUAGE_SO = "build/my-languages.so"   # <- change to your path
LANGUAGE_NAME = "python"                # <- change to language name in the library

def node_to_dict(node, src_bytes):
    d = {
        "type": node.type,
        "start_point": node.start_point,
        "end_point": node.end_point,
        "is_named": node.is_named,
    }
    # If node is a leaf, include its text (trimmed)
    if node.child_count == 0:
        text = src_bytes[node.start_byte:node.end_byte].decode("utf8", "replace")
        d["text"] = text
    if node.child_count:
        d["children"] = [node_to_dict(node.child(i), src_bytes) for i in range(node.child_count)]
    return d

def main():
    if len(sys.argv) < 2:
        print("Usage: parse_example.py <source-file>")
        sys.exit(2)
    src_path = sys.argv[1]
    src = open(src_path, "rb").read()
    # Load language
    Language.build_library  # hint: ensure build step done separately
    LANG = Language(LANGUAGE_SO, LANGUAGE_NAME)
    parser = Parser()
    parser.set_language(LANG)
    tree = parser.parse(src)
    root = tree.root_node
    ast = node_to_dict(root, src)
    print(json.dumps(ast, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
