from dataclasses import dataclass, field
from typing import Optional
from .parser import ASTNode, ParseResult


@dataclass
class NormalizedNode:
    id: str
    type: str
    name: Optional[str] = None
    start_byte: int = 0
    end_byte: int = 0
    children: list["NormalizedNode"] = field(default_factory=list)


_ID_COUNTER: int = 0


def _next_id() -> str:
    global _ID_COUNTER
    _ID_COUNTER += 1
    return f"n{_ID_COUNTER}"


def _extract_name(node: ASTNode) -> Optional[str]:
    name_keywords = {"name", "identifier", "property_identifier", "type_identifier"}
    for c in node.children:
        if c.type in name_keywords and c.text:
            return c.text.strip()
    if node.type in name_keywords and node.text:
        return node.text.strip()
    return None


def _normalize_node(node: ASTNode) -> NormalizedNode:
    nid = _next_id()
    normalized = NormalizedNode(
        id=nid,
        type=node.type,
        name=_extract_name(node) if node.is_named else None,
        start_byte=node.start_byte,
        end_byte=node.end_byte,
    )
    if node.children:
        for c in node.children:
            if c.is_named:
                normalized.children.append(_normalize_node(c))
    return normalized


def normalize(result: ParseResult) -> list[NormalizedNode]:
    global _ID_COUNTER
    _ID_COUNTER = 0
    root = _normalize_node(result.root)
    return root.children


def normalize_full(result: ParseResult) -> NormalizedNode:
    global _ID_COUNTER
    _ID_COUNTER = 0
    return _normalize_node(result.root)


def node_to_dict(node: NormalizedNode) -> dict:
    d = {"id": node.id, "type": node.type, "start_byte": node.start_byte, "end_byte": node.end_byte}
    if node.name:
        d["name"] = node.name
    if node.children:
        d["children"] = [node_to_dict(c) for c in node.children]
    return d
