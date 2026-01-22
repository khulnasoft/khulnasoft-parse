#!/usr/bin/bash -e
set -euo pipefail

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
FAILED_TESTS=0
PASSED_TESTS=0

echo "Running tests matching pattern: $TEST_PATTERN"
echo "=============================================="

for test_file in test_files/*; do
    test_file="$(basename "$test_file")"
    
    # Skip if doesn't match pattern
    if ! echo "$test_file" | grep -q "$TEST_PATTERN"; then
        continue
    fi
    
    echo -n "Testing $test_file ... "
    
    # Generate temporary output
    if ! ./parse -file "test_files/$test_file" -use_tags_query -tags_query_dir "queries" > "goldens/$test_file.golden.tmp" 2>/dev/null; then
        echo "FAILED (parse error)"
        ((FAILED_TESTS++))
        rm -f "goldens/$test_file.golden.tmp"
        continue
    fi
    
    # Compare with golden file
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
