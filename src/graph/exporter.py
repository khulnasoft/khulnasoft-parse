import json
from .relations import CodeGraph


def to_json(graph: CodeGraph, indent: int = 2) -> str:
    return json.dumps({
        "nodes": [
            {"id": n.id, "label": n.label, "kind": n.kind, "file": n.file,
             "start_byte": n.start_byte, "end_byte": n.end_byte}
            for n in graph.nodes
        ],
        "edges": [
            {"source": e.source, "target": e.target, "relation": e.relation}
            for e in graph.edges
        ],
    }, indent=indent, ensure_ascii=False)


def to_d3(graph: CodeGraph) -> str:
    return json.dumps({
        "nodes": [{"id": n.id, "label": n.label, "group": n.kind} for n in graph.nodes],
        "links": [{"source": e.source, "target": e.target, "relation": e.relation} for e in graph.edges],
    }, indent=2, ensure_ascii=False)


def to_gexf(graph: CodeGraph) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">',
        "  <graph mode=\"static\" defaultedgetype=\"directed\">",
        "    <nodes>",
    ]
    for n in graph.nodes:
        lines.append(f'      <node id="{n.id}" label="{n.label}"/>')
    lines.append("    </nodes>")
    lines.append("    <edges>")
    for i, e in enumerate(graph.edges):
        lines.append(f'      <edge id="{i}" source="{e.source}" target="{e.target}" label="{e.relation}"/>')
    lines.append("    </edges>")
    lines.extend(["  </graph>", "</gexf>"])
    return "\n".join(lines)
