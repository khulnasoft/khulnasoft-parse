from src.core.ast_normalizer import NormalizedNode
from src.core.parser import ParseResult
from src.contracts.types import FileAnalysis, Symbol, DependencyEdge, ImportEdge, SourceLocation, Complexity
from .tagger import tag_symbol


def _classify_node_type(node_type: str) -> str:
    if node_type in ("function_declaration", "function_definition", "arrow_function"):
        return "function"
    if node_type in ("class_declaration", "class_definition"):
        return "class"
    if node_type in ("method_declaration", "method_definition"):
        return "method"
    if node_type in ("variable_declaration", "assignment", "let", "const", "var"):
        return "variable"
    if node_type in ("interface_declaration", "type_definition", "struct"):
        return "type"
    return node_type


def _classify_visibility(node_type: str, name: str | None) -> str:
    if name and name.startswith("__") and name.endswith("__"):
        return "public"
    if name and name.startswith("__"):
        return "protected"
    if name and name.startswith("_"):
        return "private"
    return "public"


def _estimate_cyclomatic(node: NormalizedNode) -> int:
    score = 1
    branching = {"if_statement", "else_clause", "for_statement", "while_statement",
                 "case", "switch_statement", "catch_clause", "conditional_expression",
                 "try_statement"}
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type in branching:
            score += 1
        stack.extend(n.children)
    return score


def _estimate_cognitive(node: NormalizedNode) -> int:
    score = 0
    nesting_bonus = {"if_statement": 1, "for_statement": 1, "while_statement": 1,
                     "try_statement": 1, "catch_clause": 1}
    stack = [(node, 0)]
    while stack:
        n, depth = stack.pop()
        base = nesting_bonus.get(n.type, 0)
        if base:
            score += base + depth
        for c in n.children:
            stack.append((c, depth + (1 if base else 0)))
    return score


def _collect_deps(node: NormalizedNode, enclosing: str) -> list[DependencyEdge]:
    deps = []
    call_stack = [(node, enclosing)]
    while call_stack:
        n, caller = call_stack.pop()
        if n.type in ("call_expression", "call"):
            callee = ""
            for c in n.children:
                if c.type in ("identifier", "field_expression", "attribute", "method"):
                    callee = c.name or c.type
                    break
            if callee:
                deps.append(DependencyEdge(
                    source=caller, target=callee, relation="calls",
                    location=SourceLocation(start_byte=n.start_byte, end_byte=n.end_byte),
                ))
        call_stack.extend((c, caller) for c in n.children)
    return deps


def _collect_imports(result: ParseResult) -> list[ImportEdge]:
    imports = []
    stack = [result.root]
    while stack:
        n = stack.pop()
        t = n.type
        if "import" in t or "require" in t:
            source = ""
            names = []
            for c in n.children:
                if c.type in ("string", "string_literal", "source") and c.text:
                    source = c.text.strip("\"'")
                if c.type in ("identifier", "dotted_name", "name") and c.text:
                    names.append(c.text.strip())
            kind = "module"
            if "from" in t:
                kind = "named"
            if names or source:
                imports.append(ImportEdge(source=source, names=names, kind=kind))
        stack.extend(c for c in n.children)
    return imports


def _find_docstring(normalized: NormalizedNode) -> str | None:
    if normalized.children:
        first = normalized.children[0]
        if first.type == "comment" and first.name:
            return first.name
        if first.type == "expression_statement" and first.children:
            child = first.children[0]
            if child.type in ("string", "string_literal") and child.name:
                return child.name
    return None


def analyze(result: ParseResult, normalized: list[NormalizedNode]) -> FileAnalysis:
    imports = _collect_imports(result)
    analysis = FileAnalysis(file=result.source_path, language=result.language, imports=imports)

    def walk(nodes: list[NormalizedNode], depth: int = 0):
        for n in nodes:
            t = _classify_node_type(n.type)
            if t in ("function", "class", "method", "type"):
                visibility = _classify_visibility(t, n.name)
                doc = _find_docstring(n)
                sym = Symbol(
                    name=n.name or n.type,
                    kind=t,
                    visibility=visibility,
                    location=SourceLocation(file=result.source_path, start_byte=n.start_byte, end_byte=n.end_byte),
                    docstring=doc,
                    complexity=Complexity(
                        cyclomatic=_estimate_cyclomatic(n),
                        cognitive=_estimate_cognitive(n),
                    ),
                )
                sym.tags = tag_symbol(sym.name, sym.kind, sym.docstring)
                analysis.symbols.append(sym)
                deps = _collect_deps(n, sym.name)
                analysis.dependencies.extend(deps)
            walk(n.children, depth + 1)

    walk(normalized)
    return analysis
