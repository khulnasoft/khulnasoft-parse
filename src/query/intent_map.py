INTENT_MAP: dict[str, dict] = {
    "authentication": {
        "tags": ["authentication"],
        "keywords": ["login", "logout", "signup", "register", "password", "token", "jwt", "session", "oauth"],
        "patterns": ["import.*auth", "import.*jwt", "import.*oauth", "def login", "def authenticate"],
    },
    "database": {
        "tags": ["database"],
        "keywords": ["sql", "query", "select", "insert", "update", "delete", "orm", "model", "repository"],
        "patterns": ["import.*sql", "import.*db", "class.*Model", "def.*query"],
    },
    "error_handling": {
        "tags": ["error_handling"],
        "keywords": ["error", "exception", "panic", "throw", "try", "catch", "fail"],
        "patterns": ["try:", "except", "throw new", "if.*error"],
    },
    "networking": {
        "tags": ["networking"],
        "keywords": ["http", "request", "response", "route", "api", "handler", "middleware", "server"],
        "patterns": ["import.*http", "def.*handler", "app.get", "app.post", "router"],
    },
    "testing": {
        "tags": ["testing"],
        "keywords": ["test", "spec", "assert", "expect", "mock", "it(", "describe"],
        "patterns": ["def test_", "it(", "describe(", "assert."],
    },
    "caching": {
        "tags": ["caching"],
        "keywords": ["cache", "redis", "memcached", "lru", "ttl"],
        "patterns": ["import.*cache", "import.*redis"],
    },
    "serialization": {
        "tags": ["serialization"],
        "keywords": ["json", "yaml", "xml", "marshal", "unmarshal", "serialize", "deserialize"],
        "patterns": ["import.*json", "json.dumps", "json.loads", "marshal"],
    },
    "configuration": {
        "tags": ["configuration"],
        "keywords": ["config", "setting", "option", "env", "flag", "yaml", "toml"],
        "patterns": ["import.*config", "os.getenv", "os.environ"],
    },
}


def resolve_intent(intent: str) -> dict | None:
    intent_lower = intent.lower().replace("-", "_").replace(" ", "_")
    return INTENT_MAP.get(intent_lower)


def list_intents() -> list[str]:
    return sorted(INTENT_MAP.keys())


def match_intents(symbol_tags: list[str], symbol_name: str, docstring: str | None = None) -> list[str]:
    matched = []
    text = " ".join(symbol_tags).lower()
    text += f" {symbol_name.lower()}"
    if docstring:
        text += f" {docstring.lower()}"
    for intent_name, intent_config in INTENT_MAP.items():
        for kw in intent_config["keywords"]:
            if kw.lower() in text:
                matched.append(intent_name)
                break
    return matched
