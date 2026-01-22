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

# Validate parse binary is executable
if [ ! -x "./parse" ]; then
    echo "ERROR: parse binary not executable. Set permissions with: chmod +x ./parse"
    exit 1
fi

LANGUAGE_PATTERN="${1:-.}"
# Escape regex special characters for safe glob expansion
# Preserve default pattern to match all files
if [ "$LANGUAGE_PATTERN" = "." ]; then
    LANGUAGE_PATTERN_SAFE=""
else
    LANGUAGE_PATTERN_SAFE=$(printf '%s\n' "$LANGUAGE_PATTERN" | sed 's/[[\.^$*]/\\&/g')
fi
ERRORS=0
WARNINGS=0
CHECKED=0

echo "Validating tree-sitter queries..."
echo "=================================="

# Find all .scm files matching pattern
for query_file in queries/*${LANGUAGE_PATTERN_SAFE}*.scm; do
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
    
    # Capture error details in temporary file for secure handling
    error_log="/tmp/query_error_$$.log"
    if ./parse -file "$test_file" -use_tags_query -tags_query_dir "queries" > /dev/null 2> "$error_log"; then
        echo "OK"
    else
        echo "FAILED"
        # Extract and sanitize error output - show first line only to prevent information leakage
        if [ -s "$error_log" ]; then
            error_line=$(head -1 "$error_log" | cut -c1-120)
            echo "  Error: $error_line"
        else
            echo "  Error: Unknown error (no details available)"
        fi
        ((ERRORS++))
    fi
    rm -f "$error_log"
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
