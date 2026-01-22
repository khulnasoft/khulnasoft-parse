# Adoption Guide - Using Enhanced Queries

## Overview
This guide helps you leverage the new query capabilities added to khulnasoft-parse.

---

## What's New?

### New Capture Types
The project now captures:
- **Variables**: `@definition.variable`
- **Constants**: `@definition.constant`
- **Enums**: `@definition.enum`
- **Exceptions**: Exception handling patterns
- **Decorators**: Function/class decorators
- **Type Aliases**: Custom type definitions
- **Generic Types**: Parameterized types

### New Query Files
12 new `.scm` files covering advanced patterns:
- Python: Variables, decorators, exceptions (3 files)
- TypeScript/JS: Types, generics, exceptions (3 files)
- Go: Types/enums, exceptions (2 files)
- Java: Enums/annotations, exceptions (2 files)
- C++: Enums, exceptions (2 files)

### Enhanced Tools
- Better error handling in scripts
- Query validation tool
- Improved documentation

---

## Getting Started

### Step 1: Download Latest Parser
```bash
./download_parse.sh v0.0.17
# Or latest: ./download_parse.sh latest
```

### Step 2: Verify Installation
```bash
# Test your setup
./test.sh

# Validate queries
./validate_queries.sh
```

### Step 3: Try New Features
```bash
# Parse with all queries (including new ones)
./parse -file examples/example.js -use_tags_query -tags_query_dir queries -json

# Find all variables
./parse -file myfile.py -use_tags_query -tags_query_dir queries | grep "variable"

# Find all enums
./parse -file myfile.java -use_tags_query -tags_query_dir queries | grep "enum"
```

---

## Use Cases

### Use Case 1: Code Analysis Tool
Extract all definitions for documentation generation:

```bash
#!/bin/bash
FILE=$1

echo "=== Classes ==="
./parse -file "$FILE" -use_tags_query -tags_query_dir queries | \
  grep "definition.class" | head -10

echo "=== Functions ==="
./parse -file "$FILE" -use_tags_query -tags_query_dir queries | \
  grep "definition.function" | head -10

echo "=== Exceptions ==="
./parse -file "$FILE" -use_tags_query -tags_query_dir queries | \
  grep "exception" | head -10
```

### Use Case 2: Code Quality Scanner
Find potential issues with exception handling:

```bash
#!/bin/bash
# Find all functions that might throw exceptions
for file in $(find . -name "*.java"); do
  throws=$(./parse -file "$file" -use_tags_query -tags_query_dir queries | \
    grep -c "declares_throws" || echo 0)
  if [ "$throws" -gt 0 ]; then
    echo "$file has $throws methods that declare throws"
  fi
done
```

### Use Case 3: Type Safety Audit
Track generic type usage:

```bash
#!/bin/bash
# Find all generic functions in TypeScript
for file in $(find . -name "*.ts"); do
  generics=$(./parse -file "$file" -use_tags_query -tags_query_dir queries | \
    grep "is_generic" | wc -l)
  echo "$file: $generics generic functions"
done
```

### Use Case 4: Documentation Generator
Extract all exported definitions:

```bash
#!/bin/bash
FILE=$1

./parse -file "$FILE" -use_tags_query -tags_query_dir queries -json | \
  jq 'select(.custom_properties.is_export == true) | 
      {name: .captures.name[0].text, type: .captures.definition_type[0].text}' \
  -r
```

### Use Case 5: Error Handling Coverage
Find try-catch blocks:

```bash
#!/bin/bash
# Analyze exception handling
./parse -file "$1" -use_tags_query -tags_query_dir queries | \
  grep -o "definition.exception_handler" | wc -l | \
  xargs echo "Exception handlers found:"
```

---

## Integration Examples

### Integration with grep/jq Pipeline
```bash
# Find all methods with documentation
./parse -file myfile.java -use_tags_query -tags_query_dir queries -json | \
  jq 'select(.captures.doc != null) | 
      {name: .captures.name[0].text, doc: .captures.doc[0].text}'

# List all enums
./parse -file myfile.ts -use_tags_query -tags_query_dir queries -json | \
  jq 'select(.captures.definition_enum != null) | 
      .captures.name[0].text'
```

### Integration with IDEs
Many IDEs support custom language servers. Use khulnasoft-parse as backend:

```python
# Example LSP implementation
def get_symbols(file_path):
    result = subprocess.run([
        './parse', 
        '-file', file_path,
        '-use_tags_query',
        '-tags_query_dir', 'queries',
        '-json'
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)
```

### Integration with CI/CD
Add to your CI pipeline to enforce code quality:

```yaml
# GitHub Actions example
- name: Check Exception Handling
  run: |
    ./validate_queries.sh
    ./parse -file src/main.java -use_tags_query -tags_query_dir queries \
      | grep -c "exception_handler" || exit 1
```

---

## Advanced Usage

### Custom Query for Your Codebase
Create language-specific patterns:

```scm
;; queries/myproject_patterns.scm
;; Capture deprecated API usage patterns

(call_expression
  function: (identifier) @deprecated_api
  (#match? @deprecated_api "^old_.*")
) @reference.deprecated
```

Then use it:
```bash
./parse -file myfile.py -tags_query_file queries/myproject_patterns.scm
```

### Batch Processing
Process entire repository:

```bash
#!/bin/bash
echo "Language,File,Classes,Functions,Exceptions"

for file in $(find . -name "*.py" -o -name "*.ts" -o -name "*.java"); do
  lang=$(echo "$file" | rev | cut -d. -f1 | rev)
  classes=$(./parse -file "$file" -use_tags_query -tags_query_dir queries | \
    grep -c "definition.class" || echo 0)
  functions=$(./parse -file "$file" -use_tags_query -tags_query_dir queries | \
    grep -c "definition.function" || echo 0)
  exceptions=$(./parse -file "$file" -use_tags_query -tags_query_dir queries | \
    grep -c "exception" || echo 0)
  
  echo "$lang,$file,$classes,$functions,$exceptions"
done
```

### Performance Analysis
Track code complexity metrics:

```bash
#!/bin/bash
FILE=$1

METHODS=$(./parse -file "$FILE" -use_tags_query -tags_query_dir queries | \
  grep -c "definition.method" || echo 0)
VARIABLES=$(./parse -file "$FILE" -use_tags_query -tags_query_dir queries | \
  grep -c "definition.variable" || echo 0)
EXCEPTIONS=$(./parse -file "$FILE" -use_tags_query -tags_query_dir queries | \
  grep -c "exception_handler" || echo 0)

echo "Methods: $METHODS"
echo "Variables: $VARIABLES"
echo "Exception Handlers: $EXCEPTIONS"
echo "Complexity Score: $((METHODS + VARIABLES/2 + EXCEPTIONS))"
```

---

## Troubleshooting

### Query Not Matching
1. Check syntax tree: `./parse -file test.py -named_only`
2. Validate query: `./validate_queries.sh python`
3. Review pattern: `QUERY_PATTERNS.md`

### Parser Crashes
1. Verify binary: `./parse -help`
2. Check file encoding: `file myfile.py`
3. Try smaller test file

### Results Not Expected
1. Check for specific language: `./parse -file file.ts` (not `.js`)
2. Use correct query directory: `-tags_query_dir queries`
3. Pipe to `less` to see full output

### Performance Issues
1. Use pattern filtering: `./test.sh python` (not all tests)
2. Filter output: pipe to `grep` for specific captures
3. Process smaller files first

---

## Best Practices

### Query Development
1. Start with tree structure: `./parse -file test -named_only`
2. Develop incrementally: test one pattern at a time
3. Use test files: update `test_files/test.{lang}`
4. Validate syntax: `./validate_queries.sh {lang}`
5. Document patterns: add comments in `.scm` files

### Pipeline Development
1. Cache results when possible
2. Filter output early to reduce data volume
3. Use JSON format for structured processing
4. Version your queries alongside code
5. Test with real codebase samples

### Performance Optimization
1. Use specific node types (avoid wildcards)
2. Apply predicates early to filter
3. Process files in parallel when possible
4. Cache parse results for same file
5. Use simple queries, combine with grep/jq

---

## Migration Checklist

- [ ] Read CONTRIBUTING.md
- [ ] Run `./test.sh` to verify setup
- [ ] Run `./validate_queries.sh` to check all queries
- [ ] Try example: `./parse -file examples/example.js -use_tags_query -tags_query_dir queries`
- [ ] Explore new captures: grep for `definition.variable`, `definition.enum`, etc.
- [ ] Read QUERY_PATTERNS.md for available patterns
- [ ] Create first custom query in `queries/my_lang_custom.scm`
- [ ] Test custom query: `./validate_queries.sh my_lang`
- [ ] Integrate into your tool/pipeline
- [ ] Document your usage patterns

---

## Support & Resources

- **Documentation**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Patterns Reference**: See [QUERY_PATTERNS.md](QUERY_PATTERNS.md)
- **Quick Help**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Code Review**: See [CODE_REVIEW.md](CODE_REVIEW.md)
- **Tree-sitter Docs**: https://tree-sitter.github.io/tree-sitter/

---

## Examples Repository

Add these examples to your codebase:

### Example 1: Extract All Definitions
```python
#!/usr/bin/env python3
import subprocess
import json
import sys

def extract_definitions(file_path):
    result = subprocess.run([
        './parse', '-file', file_path,
        '-use_tags_query', '-tags_query_dir', 'queries',
        '-json'
    ], capture_output=True, text=True)
    
    data = json.loads(result.stdout)
    return {
        'classes': data.get('captures', {}).get('definition.class', []),
        'functions': data.get('captures', {}).get('definition.function', []),
        'variables': data.get('captures', {}).get('definition.variable', []),
        'exceptions': data.get('captures', {}).get('exception', []),
    }

if __name__ == '__main__':
    defs = extract_definitions(sys.argv[1])
    print(f"Classes: {len(defs['classes'])}")
    print(f"Functions: {len(defs['functions'])}")
    print(f"Variables: {len(defs['variables'])}")
    print(f"Exception Handlers: {len(defs['exceptions'])}")
```

### Example 2: Code Metrics Report
```bash
#!/bin/bash
# Generate code metrics for repository

LANGUAGES=("*.py" "*.ts" "*.java" "*.go" "*.cpp")

for pattern in "${LANGUAGES[@]}"; do
    echo "=== Analyzing $pattern files ==="
    
    for file in $(find . -name "$pattern" 2>/dev/null); do
        classes=$(./parse -file "$file" -use_tags_query -tags_query_dir queries \
          | grep -c "definition.class" || echo 0)
        methods=$(./parse -file "$file" -use_tags_query -tags_query_dir queries \
          | grep -c "definition.method" || echo 0)
        functions=$(./parse -file "$file" -use_tags_query -tags_query_dir queries \
          | grep -c "definition.function" || echo 0)
        
        if [ $((classes + methods + functions)) -gt 0 ]; then
            echo "$file: Classes=$classes Methods=$methods Functions=$functions"
        fi
    done
done
```

---

## Next Steps

1. **Explore** - Try the new queries on your codebase
2. **Integrate** - Add to your tools and pipelines
3. **Contribute** - Add queries for your use cases
4. **Optimize** - Tune for your specific needs
5. **Share** - Document and share results with team

Happy parsing! 🎉
