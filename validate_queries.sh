#!/bin/bash
# Script: Query Validation
# Description: Validates tree-sitter queries for syntax errors and correctness
# Usage: ./validate_queries.sh [language_pattern]

set -euo pipefail

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
cd "$SCRIPT_DIR"

# Check if parse binary exists
if [ ! -f "./parse" ]; then
    echo "ERROR: parse binary not found. Run './download_parse.sh' first."
    exit 1
fi

# Validate parse binary with a simple query
if ! ./parse -file /dev/null -help > /dev/null 2>&1; then
    echo "ERROR: parse binary not functional"
    exit 1
fi

LANGUAGE_PATTERN="${1:-.}"
ERRORS=0
WARNINGS=0
CHECKED=0

echo "Validating tree-sitter queries..."
echo "=================================="

# Find all .scm files matching pattern
for query_file in queries/*${LANGUAGE_PATTERN}*.scm; do
    if [ ! -f "$query_file" ]; then
        continue
    fi
    
    filename="$(basename "$query_file")"
    ((CHECKED++))
    
    # Extract language and feature
    if [[ $filename =~ ^([^_]+).*\.scm$ ]]; then
        language="${BASH_REMATCH[1]}"
    else
        language="unknown"
    fi
    
    # Find corresponding test file
    test_file="test_files/test.${language}"
    
    if [ ! -f "$test_file" ]; then
        echo "⚠ SKIP: $filename (no test file for $language)"
        ((WARNINGS++))
        continue
    fi
    
    # Try to run parse with this query file
    echo -n "✓ Checking $filename ... "
    
    if ./parse -file "$test_file" -use_tags_query -tags_query_dir "queries" > /dev/null 2>&1; then
        echo "OK"
    else
        # Extract more info about the error
        error_output=$(./parse -file "$test_file" -use_tags_query -tags_query_dir "queries" 2>&1 || true)
        echo "FAILED"
        echo "  Error: $error_output"
        ((ERRORS++))
    fi
done

echo "=================================="
echo "Results:"
echo "  Files checked: $CHECKED"
echo "  Warnings: $WARNINGS"
echo "  Errors: $ERRORS"

if [ $ERRORS -gt 0 ]; then
    exit 1
fi

exit 0
