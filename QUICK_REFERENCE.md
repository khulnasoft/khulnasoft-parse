# Quick Reference Guide

## File Structure Overview
```
khulnasoft-parse/
├── README.md                          # Project overview
├── LICENSE                            # License
│
├── Documentation (NEW/ENHANCED)
├── CODE_REVIEW.md                     # Comprehensive code review
├── CONTRIBUTING.md                    # How to contribute
├── QUERY_PATTERNS.md                  # Query pattern reference
├── ENHANCEMENTS.md                    # Enhancement summary
│
├── Scripts (ENHANCED)
├── download_parse.sh                  # Enhanced: platform detection
├── test.sh                            # Enhanced: better error handling
├── validate_queries.sh                # NEW: Query validation
├── goldens.sh                         # Update golden test files
│
├── Queries
├── queries/
│   ├── *_tags.scm                     # Core definitions
│   ├── *_class_fields.scm             # Class members
│   ├── *_imports.scm                  # Import statements
│   ├── *_functions.scm                # Function patterns
│   ├── *_constructors.scm             # Constructors
│   ├── *_variables.scm                # NEW: Variable declarations
│   ├── *_enums.scm or *_types_enums.scm  # NEW: Enums & types
│   ├── *_types.scm or *_generics.scm  # NEW: Type aliases & generics
│   ├── *_exceptions.scm               # NEW: Exception handling
│   ├── *_decorators.scm               # NEW: Decorators/annotations
│   └── *_injections.scm               # Language injections
│
├── Test Files & Golden References
├── test_files/
│   ├── test.c, test.cpp, test.cs, ...
│   └── test.{lang}
└── goldens/
    ├── test.c.golden, test.cpp.golden, ...
    └── test.{lang}.golden
```

---

## Common Tasks

### Parse a File
```bash
# Basic syntax tree
./parse -file myfile.js -named_only

# With query
./parse -file myfile.js -use_tags_query -tags_query_dir queries -json
```

### Find Specific Patterns
```bash
# Find all functions
./parse -file myfile.py -use_tags_query -tags_query_dir queries \
  | grep "definition.function"

# Find all classes
./parse -file myfile.java -use_tags_query -tags_query_dir queries \
  | grep "definition.class"

# Find exceptions
./parse -file myfile.ts -use_tags_query -tags_query_dir queries \
  | grep "exception"
```

### Test Queries
```bash
# Test all languages
./test.sh

# Test specific language
./test.sh python

# Test with pattern
./test.sh "java|python"
```

### Validate Queries
```bash
# Check all queries
./validate_queries.sh

# Check specific language
./validate_queries.sh python

# Check Go queries
./validate_queries.sh go
```

### Add New Query
```bash
# 1. Edit queries/{language}_newfeature.scm
# 2. Add example code to test_files/test.{lang}
# 3. Run tests
./test.sh {language}
# 4. Regenerate golden (if test passes)
./goldens.sh
```

---

## Query Capture Quick Reference

### Definitions (What is defined?)
```
@definition.class              - Classes, structs, records
@definition.function           - Functions, procedures  
@definition.method             - Methods in classes
@definition.constructor        - Constructors
@definition.interface          - Interfaces, protocols
@definition.enum              - Enums (NEW)
@definition.constant          - Constants (NEW)
@definition.variable          - Variables (NEW)
@definition.exception         - Exception classes (NEW)
@definition.type              - Type aliases (NEW)
@definition.decorator         - Decorators (NEW)
@definition.property          - Properties (NEW)
@definition.exception_handler - Try-catch blocks (NEW)
```

### References (How is something used?)
```
@reference.call      - Function/method calls
@reference.class     - Class instantiation
@reference.type      - Type usage
@reference.exception - Exception throwing (NEW)
@reference.annotation - Annotation usage (NEW)
```

### Metadata (Additional information)
```
@doc                      - Documentation
@khulnasoft.parameters    - Function parameters
@khulnasoft.return_type   - Return type
@body                     - Code body
@name                     - Identifier name
```

---

## Language Coverage Matrix

| Feature | Python | TypeScript | JavaScript | Go | Java | C++ | PHP | Ruby | C# | Perl | Kotlin | Dart | Bash | C |
|---------|--------|-----------|-----------|----|----|-----|----|-----|----|------|--------|------|------|---|
| Classes | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Functions | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Methods | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Constructors | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Interfaces | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Enums | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✓ |
| Types (NEW) | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Exceptions (NEW) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Decorators (NEW) | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Variables (NEW) | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

✓ = Fully supported, ✗ = Not supported, ✓ (NEW) = Newly added

---

## Predicate Reference

### Type Checking
```scm
(#has-type? @node type1 type2)       ;; One of these types
(#not-has-type? @node type)          ;; Not this type
```

### Parent/Context
```scm
(#not-has-parent? @node parent_type) ;; Not inside parent
```

### Text Matching
```scm
(#match? @node "regex_pattern")      ;; Matches regex
(#not-match? @node "pattern")        ;; Doesn't match
(#eq? @node "exact")                 ;; Exact text match
(#not-eq? @node "text")              ;; Not equal
```

### Capture Operations
```scm
(#select-adjacent! @doc @node)       ;; Link doc to node
(#set! property value)               ;; Set custom property
```

---

## Common Patterns

### Capture Function with Documentation
```scm
(
  (comment)* @doc
  .
  (function_definition
    name: (identifier) @name
    parameters: (_) @khulnasoft.parameters) @definition.function
  (#select-adjacent! @doc @definition.function)
)
```

### Exclude Patterns (Don't Match Inside)
```scm
(assignment
  left: (identifier) @name
  right: (_) @value) @definition.variable
(#not-has-parent? @definition.variable function_definition class_definition)
```

### Export Detection
```scm
(export_statement
  declaration: (function_declaration
    name: (identifier) @name) @_) @definition.function
(#set! is_export true)
```

### Constant Detection (UPPERCASE)
```scm
(assignment
  left: (identifier) @name
  right: (_) @value) @definition.constant
(#match? @name "^[A-Z][A-Z0-9_]*$")
```

---

## Debugging Tips

### Check AST Structure
```bash
# See raw syntax tree
./parse -file myfile.py -named_only

# Pretty print specific node
./parse -file myfile.py -named_only | grep -A 10 "function"
```

### Test Query on File
```bash
# Run single query
./parse -file test_files/test.py -use_tags_query \
  -tags_query_dir queries -json

# Filter output
./parse -file test_files/test.py -use_tags_query \
  -tags_query_dir queries | grep "my_function"
```

### Compare Against Golden
```bash
# Generate test output
./parse -file test_files/test.py -use_tags_query \
  -tags_query_dir queries > /tmp/test.out

# Compare
diff goldens/test.py.golden /tmp/test.out
```

### Validate Query Syntax
```bash
# Check if queries work
./validate_queries.sh python

# See errors
./validate_queries.sh python 2>&1 | head -20
```

---

## Performance Tips

1. **Use Specific Patterns**: Avoid wildcards in node types
2. **Filter Early**: Use predicates to exclude non-matches
3. **Cache Results**: Store output for repeated queries
4. **Batch Operations**: Parse multiple files efficiently
5. **Filter Output**: Pipe to grep for large result sets

---

## Contributing

1. **Read** [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
2. **Check** [QUERY_PATTERNS.md](QUERY_PATTERNS.md) for patterns
3. **Create** new `.scm` files in `queries/`
4. **Test** with `./validate_queries.sh` 
5. **Run** `./test.sh` to verify
6. **Update** golden files if needed
7. **Submit** pull request with documentation

---

## Resources

- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [Query Syntax Guide](https://tree-sitter.github.io/tree-sitter/query-syntax)
- [Language Grammars](https://github.com/tree-sitter)
- [CONTRIBUTING.md](CONTRIBUTING.md) - Local contribution guide
- [QUERY_PATTERNS.md](QUERY_PATTERNS.md) - Pattern reference

---

## Changelog - New in This Release

### New Query Files (12 total)
- `python_variables.scm`, `python_decorators.scm`, `python_exceptions.scm`
- `typescript_types.scm`, `typescript_generics.scm`, `typescript_exceptions.scm`
- `go_types_enums.scm`, `go_exceptions.scm`
- `java_enums_annotations.scm`, `java_exceptions.scm`
- `cpp_enums.scm`, `cpp_exceptions.scm`

### New Capture Types (10 total)
- `@definition.variable`, `@definition.constant`, `@definition.enum`
- `@definition.exception`, `@definition.decorator`, `@definition.property`
- `@definition.exception_handler`, `@definition.annotation_type`, `@definition.type_parameter`
- `@reference.annotation`, `@reference.exception`

### Enhanced Scripts
- `download_parse.sh` - Platform detection, better error handling
- `test.sh` - Result counting, pattern filtering, validation
- `validate_queries.sh` - New query validation tool

### New Documentation (4 files)
- `CODE_REVIEW.md` - Comprehensive analysis
- `CONTRIBUTING.md` - Contribution guidelines
- `QUERY_PATTERNS.md` - Pattern reference
- `ENHANCEMENTS.md` - Enhancement summary
- `QUICK_REFERENCE.md` - This file
