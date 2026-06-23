from .parser import ASTNode


def ts_node_to_astnode(ts_node, source_bytes: bytes) -> ASTNode:
    children = []
    for i in range(ts_node.child_count):
        c = ts_node.child(i)
        if c.is_named:
            children.append(ts_node_to_astnode(c, source_bytes))
    text = None
    if ts_node.child_count == 0:
        text = source_bytes[ts_node.start_byte:ts_node.end_byte].decode("utf-8", "replace")
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
