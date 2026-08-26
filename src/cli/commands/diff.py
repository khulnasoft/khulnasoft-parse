import json
import subprocess
import sys

from src.core.parser import ParseResult, ASTNode


def _flatten(node, prefix=""):
    items = {}
    pid = f"{prefix}/{node.type}"
    items[pid] = node
    for i, c in enumerate(node.children):
        items.update(_flatten(c, f"{pid}/{i}"))
    return items


def _parse_sexp(sexp: str, src: bytes) -> ASTNode:
    import re
    lines = sexp.strip().split("\n")
    stack = []
    root = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == ")":
            continue
        match = re.match(r'^\((\w+)\s+\[.*?\]\s+\[.*?\]\s+"(.*?)"\)$', stripped)
        if match:
            node = ASTNode(type=match.group(1), start_byte=0, end_byte=0, start_point=(0, 0), end_point=(0, 0),
                           is_named=True, text=match.group(2))
            if stack:
                stack[-1].children.append(node)
            else:
                root = node
            continue
        match = re.match(r'^\((\w+)\s', stripped)
        if match:
            node = ASTNode(type=match.group(1), start_byte=0, end_byte=0, start_point=(0, 0), end_point=(0, 0),
                           is_named=True)
            if stack:
                stack[-1].children.append(node)
            stack.append(node)
            if root is None:
                root = node
    return root or ASTNode(type="program", start_byte=0, end_byte=0, start_point=(0, 0), end_point=(0, 0), is_named=True)


def _parse_via_binary(fp: str) -> ParseResult:
    parse_bin = "./parse"
    try:
        r = subprocess.run([parse_bin, "-file", fp], capture_output=True, timeout=30)
    except FileNotFoundError:
        print(f"Error: '{parse_bin}' binary not found. Run ./download_parse.sh first.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"Error: '{parse_bin}' timed out on {fp}", file=sys.stderr)
        sys.exit(1)

    if r.returncode != 0:
        stderr = r.stderr.decode().strip()
        print(f"Error: '{parse_bin}' failed on {fp}: {stderr}", file=sys.stderr)
        sys.exit(1)

    stdout = r.stdout.decode().strip()
    if not stdout:
        print(f"Error: '{parse_bin}' produced empty output for {fp}", file=sys.stderr)
        sys.exit(1)

    text = open(fp, "rb").read()
    return ParseResult(source_path=fp, language="?", root=_parse_sexp(stdout, text), source_text=text.decode())


def run(args: dict) -> None:
    file_a = args.get("file_a")
    file_b = args.get("file_b")

    result_a = _parse_via_binary(file_a)
    result_b = _parse_via_binary(file_b)

    nodes_a = _flatten(result_a.root)
    nodes_b = _flatten(result_b.root)

    keys_a = set(nodes_a)
    keys_b = set(nodes_b)

    added = keys_b - keys_a
    removed = keys_a - keys_b

    common = keys_a & keys_b
    modified = []
    for k in common:
        na = nodes_a[k]
        nb = nodes_b[k]
        if na.type != nb.type or (na.text or "") != (nb.text or ""):
            modified.append(k)

    diff = {
        "file_a": file_a,
        "file_b": file_b,
        "added": sorted(added),
        "removed": sorted(removed),
        "modified": sorted(modified),
        "summary": {
            "total_a": len(nodes_a),
            "total_b": len(nodes_b),
            "added_count": len(added),
            "removed_count": len(removed),
            "modified_count": len(modified),
        },
    }
    if args.get("json"):
        print(json.dumps(diff, indent=2))
    else:
        print(f"Diff: {file_a} -> {file_b}")
        print(f"  Added:   {len(added)} nodes")
        print(f"  Removed: {len(removed)} nodes")
        print(f"  Modified: {len(modified)} nodes")
        if added:
            print("\n  Added nodes:")
            for k in sorted(added)[:10]:
                print(f"    + {k}")
        if removed:
            print("\n  Removed nodes:")
            for k in sorted(removed)[:10]:
                print(f"    - {k}")
