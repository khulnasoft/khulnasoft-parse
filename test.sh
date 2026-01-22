#!/usr/bin/bash
set -uo pipefail

# Script: Test Query Correctness
# Description: Compares current parse output against golden files
# Usage: ./test.sh [test_file_pattern]

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
cd "$SCRIPT_DIR"

# Validate parse binary exists
if [ ! -f "./parse" ]; then
    echo "ERROR: parse binary not found. Run './download_parse.sh' first."
    exit 1
fi

# Validate test files exist
if [ ! -d "test_files" ]; then
    echo "ERROR: test_files directory not found."
    exit 1
fi

# Validate queries directory exists
if [ ! -d "queries" ]; then
    echo "ERROR: queries directory not found."
    exit 1
fi

# Optional: filter test files by pattern
TEST_PATTERN="${1:-.}"
# Escape regex special characters in TEST_PATTERN for safe grep usage
# But preserve default pattern to match any file
if [ "$TEST_PATTERN" = "." ]; then
    TEST_PATTERN_ESCAPED="."
else
    TEST_PATTERN_ESCAPED=$(printf '%s\n' "$TEST_PATTERN" | sed 's/[[\.^$*/]/\\&/g')
fi
FAILED_TESTS=0
PASSED_TESTS=0

echo "Running tests matching pattern: $TEST_PATTERN"
echo "=============================================="

for test_file in test_files/*; do
    test_file="$(basename "$test_file")"
    
    # Skip if doesn't match pattern
    if ! echo "$test_file" | grep -q "$TEST_PATTERN_ESCAPED"; then
        continue
    fi
    
    echo -n "Testing $test_file ... "
    
    # Generate temporary output and capture stderr for debugging
    error_log="/tmp/parse_error_$$.log"
    if ! ./parse -file "test_files/$test_file" -use_tags_query -tags_query_dir "queries" > "goldens/$test_file.golden.tmp" 2> "$error_log"; then
        echo "FAILED (parse error)"
        # Log error details for debugging without exposing to normal output
        if [ -s "$error_log" ]; then
            echo "  [Debug: $(head -c 100 "$error_log")...]" >&2
        fi
        ((FAILED_TESTS++))
        rm -f "goldens/$test_file.golden.tmp" "$error_log"
        continue
    fi
    rm -f "$error_log"
    if diff -q "goldens/$test_file.golden" "goldens/$test_file.golden.tmp" > /dev/null; then
        echo "PASSED"
        ((PASSED_TESTS++))
        rm -f "goldens/$test_file.golden.tmp"
    else
        echo "FAILED (diff mismatch)"
        ((FAILED_TESTS++))
        echo "Differences:"
        diff -u "goldens/$test_file.golden" "goldens/$test_file.golden.tmp" || true
        rm -f "goldens/$test_file.golden.tmp"
    fi
done

echo "=============================================="
echo "Results: $PASSED_TESTS passed, $FAILED_TESTS failed"

if [ $FAILED_TESTS -gt 0 ]; then
    exit 1
fi
exit 0
