#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LANGUAGE_SO = os.environ.get("LANGUAGE_SO")
TEST_FILES = REPO_ROOT / "test_files"


def has_parse_binary() -> bool:
    return (REPO_ROOT / "parse").is_file()


def skip_if_no_parse():
    if not has_parse_binary():
        print("SKIP: no parse binary found (run ./download_parse.sh)")
        return True
    return False


def skip_if_no_lang_so():
    if not LANGUAGE_SO:
        print("SKIP: LANGUAGE_SO not set — skipping parse-dependent tests")
        return True
    return False


def test_python_parse_script():
    sys.path.insert(0, str(REPO_ROOT / "examples"))
    import parse_example
    for py_file in TEST_FILES.glob("*.py"):
        tree = parse_example.get_language("python", LANGUAGE_SO)
        parser = parse_example._make_parser(tree)
        src = py_file.read_bytes()
        parsed = parser.parse(src)
        ast = parse_example.node_to_json(parsed.root_node, src)
        assert "type" in ast and "children" in ast
        print(f"  OK {py_file.name} ({len(json.dumps(ast))} chars)")


def test_native_parse_binary():
    import subprocess
    for f in sorted(TEST_FILES.iterdir()):
        if not f.is_file():
            continue
        result = subprocess.run(
            [str(REPO_ROOT / "parse"), "-file", str(f)],
            capture_output=True, timeout=30,
        )
        assert result.returncode == 0, f"parse failed on {f.name}: {result.stderr.decode()}"
        out = result.stdout.decode()
        assert len(out) > 0, f"empty output for {f.name}"
        print(f"  OK {f.name} ({len(out)} chars)")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run khulnasoft-parse tests")
    parser.add_argument("--mode", choices=["python", "native", "all"], default="all")
    args = parser.parse_args()

    if args.mode in ("python", "all"):
        print("=== Python parser example tests ===")
        if not skip_if_no_lang_so():
            test_python_parse_script()

    if args.mode in ("native", "all"):
        print("=== Native parse binary tests ===")
        if not skip_if_no_parse():
            test_native_parse_binary()

    print("\nAll tests passed.")


if __name__ == "__main__":
    main()
