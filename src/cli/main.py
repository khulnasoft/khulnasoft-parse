#!/usr/bin/env python3
import argparse
import json
import sys
from src.kernel.orchestrator import SystemKernel


kernel = SystemKernel()


def cmd_parse(args: dict) -> None:
    ctx = kernel.analyze(args["file"], library=args.get("library"))
    if ctx.has_error():
        print(f"Error: {ctx.error}", file=sys.stderr)
        sys.exit(1)

    output = args.get("output", "ast")
    if output == "ast":
        from src.core.ast_normalizer import normalize_full, node_to_dict
        full = normalize_full(ctx.parse_result) if ctx.parse_result else None
        print(json.dumps(node_to_dict(full) if full else {}, indent=2))
    elif output == "normalized":
        from src.core.ast_normalizer import node_to_dict
        print(json.dumps([node_to_dict(n) for n in ctx.normalized_nodes], indent=2))
    elif output == "semantic":
        print(json.dumps(ctx.analysis.to_dict() if ctx.analysis else {}, indent=2))
    elif output == "sexp":
        from src.core.ast_util import to_sexp
        if ctx.parse_result:
            print(to_sexp(ctx.parse_result.root))


def cmd_inspect(args: dict) -> None:
    mode = args.get("mode", "ast")
    filepath = args["file"]
    library = args.get("library")

    if mode == "ast":
        ctx = kernel.analyze(filepath, library=library)
        if ctx.has_error():
            print(f"Error: {ctx.error}", file=sys.stderr)
            sys.exit(1)
        from src.core.ast_normalizer import normalize_full, node_to_dict
        full = normalize_full(ctx.parse_result) if ctx.parse_result else None
        print(json.dumps(node_to_dict(full) if full else {}, indent=2))
    elif mode == "semantic":
        ctx = kernel.analyze(filepath, library=library)
        if ctx.has_error():
            print(f"Error: {ctx.error}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(ctx.analysis.to_dict() if ctx.analysis else {}, indent=2))
    elif mode == "graph":
        ctx = kernel.analyze(filepath, library=library)
        if ctx.has_error():
            print(f"Error: {ctx.error}", file=sys.stderr)
            sys.exit(1)
        fmt = args.get("graph_format", "json")
        if fmt == "d3":
            from src.graph.exporter import to_d3
            print(to_d3(ctx.graph) if ctx.graph else "{}")
        else:
            from src.graph.exporter import to_json as graph_json
            print(graph_json(ctx.graph) if ctx.graph else "{}")
    elif mode == "query":
        query_str = args.get("query", "")
        if query_str.startswith("intent:"):
            qr = kernel.query(filepath, query_str[7:], library=library)
        elif query_str.startswith("tag:"):
            qr = kernel.query_tag(filepath, query_str[4:], library=library)
        else:
            qr = kernel.query_symbol(filepath, query_str, library=library)
        print(json.dumps(qr.to_dict(), indent=2))
    elif mode == "traverse":
        traversal = args.get("traverse", "forward")
        symbol = args.get("symbol", "")
        target = args.get("target")
        result = kernel.graph_traverse(filepath, symbol, traversal=traversal,
                                       target=target, library=library)
        print(json.dumps(result, indent=2))


def cmd_ai(args: dict) -> None:
    filepath = args["file"]
    mode = args.get("mode", "explain")
    api_key = args.get("api_key") or __import__("os").environ.get("AI_API_KEY")
    library = args.get("library")

    if args.get("summary"):
        print(kernel.summarize(filepath, library=library))
        return

    result = kernel.explain(filepath, mode=mode, api_key=api_key, library=library)
    print(result)


def cmd_report(args: dict) -> None:
    target = args.get("target", ".")
    library = args.get("library")
    result = kernel.report(target, library=library)
    print(json.dumps(result, indent=2))


def cmd_diff(args: dict) -> None:
    file_a = args["file_a"]
    file_b = args["file_b"]

    from src.cli.commands.diff import run as diff_run
    diff_run(args)


def main():
    parser = argparse.ArgumentParser(
        prog="parse",
        description="Semantic Code Intelligence Engine v2 — Kernel Orchestrated",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="Parse a file and output AST / semantic data")
    p_parse.add_argument("file")
    p_parse.add_argument("--output", "-o", choices=["ast", "normalized", "semantic", "sexp"], default="ast")
    p_parse.add_argument("--library", "-L")
    p_parse.set_defaults(func="parse")

    p_inspect = sub.add_parser("inspect", help="Inspect with semantic/graph/query/traverse modes")
    p_inspect.add_argument("file")
    p_inspect.add_argument("--mode", "-m", choices=["ast", "semantic", "graph", "query", "traverse"], default="ast")
    p_inspect.add_argument("--query", "-q", help="Query string (prefix with intent:/tag: or bare symbol name)")
    p_inspect.add_argument("--graph-format", choices=["json", "d3"], default="json")
    p_inspect.add_argument("--traverse", "-t", help="Graph traversal: reverse|forward|impact|path")
    p_inspect.add_argument("--symbol", "-s", help="Symbol name for graph traversal")
    p_inspect.add_argument("--target", help="Target symbol for path query")
    p_inspect.add_argument("--library", "-L")
    p_inspect.set_defaults(func="inspect")

    p_ai = sub.add_parser("ai", help="AI analysis: explain, review, or design")
    p_ai.add_argument("file")
    p_ai.add_argument("--mode", "-m", choices=["explain", "review", "design"], default="explain")
    p_ai.add_argument("--api-key")
    p_ai.add_argument("--summary", action="store_true", help="Print text summary")
    p_ai.add_argument("--library", "-L")
    p_ai.set_defaults(func="ai")

    p_report = sub.add_parser("report", help="Generate architecture report for a directory")
    p_report.add_argument("target", nargs="?", default=".")
    p_report.add_argument("--library", "-L")
    p_report.set_defaults(func="report")

    p_diff = sub.add_parser("diff", help="AST diff between two files")
    p_diff.add_argument("file_a")
    p_diff.add_argument("file_b")
    p_diff.add_argument("--json", action="store_true")
    p_diff.set_defaults(func="diff")

    args = parser.parse_args()
    cmd = args.func
    cmd_args = vars(args)

    dispatch = {
        "parse": cmd_parse,
        "inspect": cmd_inspect,
        "ai": cmd_ai,
        "report": cmd_report,
        "diff": cmd_diff,
    }
    dispatch[cmd](cmd_args)


if __name__ == "__main__":
    main()
