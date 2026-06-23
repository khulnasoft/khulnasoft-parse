import json
from .parser import ASTNode, ParseResult


def node_to_dict(node: ASTNode) -> dict:
    d = {
        "type": node.type,
        "start_byte": node.start_byte,
        "end_byte": node.end_byte,
        "start_point": list(node.start_point),
        "end_point": list(node.end_point),
        "is_named": node.is_named,
    }
    if node.text is not None:
        d["text"] = node.text
    if node.children:
        d["children"] = [node_to_dict(c) for c in node.children]
    return d


def to_json(result: ParseResult, indent: int = 2) -> str:
    return json.dumps(
        {"source_path": result.source_path, "language": result.language, "root": node_to_dict(result.root)},
        indent=indent,
        ensure_ascii=False,
    )


def to_sexp(node: ASTNode, indent: int = 0) -> str:
    pad = "  " * indent
    label = node.type
    if node.children:
        parts = [f"{pad}({label}"]
        for c in node.children:
            parts.append(to_sexp(c, indent + 1))
        parts.append(f"{pad})")
        return "\n".join(parts)
    text = json.dumps(node.text or "")
    return f"{pad}({label} {text})"


def normalize(result: ParseResult) -> dict:
    decls, imports = [], []

    def walk(node: ASTNode, depth: int = 0):
        t = node.type
        if t in ("function_declaration", "method_declaration", "class_declaration", "function_definition",
                 "class_definition"):
            name = ""
            for c in node.children:
                if c.type in ("name", "identifier"):
                    name = c.text or ""
                    break
            decls.append({"type": t, "name": name, "start_byte": node.start_byte, "end_byte": node.end_byte})
        if "import" in t and node.children:
            imports.append({"type": t, "start_byte": node.start_byte, "end_byte": node.end_byte})
        for c in node.children:
            walk(c, depth + 1)

    walk(result.root)
    return {"language": result.language, "declarations": decls, "imports": imports}
