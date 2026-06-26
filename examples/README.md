# Examples

## Prerequisites

```bash
pip install tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-go
```

## Usage

### Parse a source file to JSON AST

```bash
# Auto-detect language from extension
python parse_example.py ../test_files/test.py
python parse_example.py ../test_files/test.js

# Specify language explicitly
python parse_example.py ../test_files/test.py --language python

# S-expression output
python parse_example.py ../test_files/test.py --format sexp

# Use a compiled language .so (classic tree-sitter)
python parse_example.py ../test_files/test.py --library build/my-languages.so
```

### Run the test harness

```bash
# Test the native parse binary (requires ./download_parse.sh first)
python ../tests/parse_test.py --mode native

# Test the Python parser (requires a compiled tree-sitter language .so)
LANGUAGE_SO=build/my-languages.so python ../tests/parse_test.py --mode python

# Run both (Python portion skipped if LANGUAGE_SO is unset)
python ../tests/parse_test.py --mode all
```
