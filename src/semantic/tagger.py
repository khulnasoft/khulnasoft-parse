from .schema import Symbol

_TAG_PATTERNS: list[tuple[set[str], set[str], str]] = [
    ({"parser", "parse", "lexer", "tokenizer"}, set(), "parser"),
    ({"io", "read", "write", "stream", "file"}, set(), "io"),
    ({"auth", "login", "authenticate", "authorize", "permission"}, set(), "authentication"),
    ({"database", "db", "sql", "query", "orm", "model", "repository"}, set(), "database"),
    ({"cache", "redis", "memcached", "lru"}, set(), "caching"),
    ({"network", "http", "request", "response", "route", "api", "handler", "middleware"}, set(), "networking"),
    ({"error", "exception", "panic", "throw", "try", "catch"}, set(), "error_handling"),
    ({"config", "setting", "option", "env", "flag"}, set(), "configuration"),
    ({"validate", "validation", "sanitize", "check", "assert"}, set(), "validation"),
    ({"test", "spec", "benchmark"}, set(), "testing"),
    ({"log", "logger", "tracing", "monitor"}, set(), "observability"),
    ({"serialize", "deserialize", "marshal", "unmarshal", "encode", "decode", "json", "yaml", "xml"},
     set(), "serialization"),
    ({"encrypt", "decrypt", "hash", "cipher", "crypto"}, set(), "cryptography"),
    ({"convert", "transform", "map", "reduce", "filter"}, set(), "transformation"),
    ({"event", "bus", "pub", "sub", "queue", "message"}, set(), "messaging"),
    ({"pool", "connection", "session", "reconnect"}, set(), "connection_pool"),
    ({"factory", "builder", "singleton", "proxy", "decorator", "adapter"}, set(), "design_pattern"),
    ({"migration", "schema", "seed"}, set(), "migration"),
    ({"template", "render", "view", "component", "ui"}, set(), "presentation"),
    ({"schedule", "cron", "timer", "job", "worker"}, set(), "scheduling"),
]


def tag_symbol(name: str, node_type: str, docstring: str | None = None) -> list[str]:
    tags: set[str] = set()
    name_lower = name.lower()
    doc_lower = (docstring or "").lower()
    text = f"{name_lower} {doc_lower}"

    if node_type in ("function_declaration", "method_declaration", "function_definition"):
        tags.add("function")
    elif node_type in ("class_declaration", "class_definition"):
        tags.add("class")

    for names, types, tag in _TAG_PATTERNS:
        for n in names:
            if n in text:
                tags.add(tag)
                break

    return sorted(tags)


def tag_symbol_full(symbol: Symbol) -> Symbol:
    symbol.tags = tag_symbol(symbol.name, symbol.kind, symbol.docstring)
    return symbol
