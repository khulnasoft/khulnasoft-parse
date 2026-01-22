# Contributing Guide

## Overview
This guide helps you contribute new queries and enhancements to khulnasoft-parse.

## File Structure

### Query Files Organization
```
queries/
├── {language}_tags.scm           # Main definitions and references
├── {language}_class_fields.scm   # Class member extraction
├── {language}_imports.scm        # Import/include statements
├── {language}_functions.scm      # Function-specific patterns
├── {language}_constructors.scm   # Constructor patterns
├── {language}_{feature}.scm      # Feature-specific queries
└── {language}_injections.scm     # Language injection queries (HTML, Vue, Markdown)
```

## Query Pattern Guidelines

### 1. Documentation Captures (@doc)
Always capture documentation with patterns:
```scm
(
  (comment)* @doc
  .
  (definition_node ...) @definition.type
)
```

### 2. Parameter Captures (@khulnasoft.parameters)
For functions/methods, capture parameters:
```scm
(function_definition
  parameters: (parameter_list) @khulnasoft.parameters)
```

### 3. Naming Convention
- `@definition.{type}`: Class, function, method, constructor, interface, namespace, module, type, constant, enum, import, include, package, variable, exception, property
- `@reference.{type}`: call, class, type, import, function
- `@doc`: Documentation strings/comments
- `@khulnasoft.parameters`: Function parameters
- `@khulnasoft.return_type`: Return type annotation
- `@body`: Function/class body

### 4. Predicates
Use these predicates for filtering:
```scm
(#has-type? @node type1 type2)      ; Node is of type1 or type2
(#not-has-parent? @node parent)      ; Node's parent is not this type
(#not-has-type? @node type)          ; Node is not this type
(#match? @node "regex")              ; Text matches regex
(#not-match? @node "regex")          ; Text doesn't match regex
(#eq? @node "value")                 ; Text equals value
(#not-eq? @node "value")             ; Text doesn't equal value
(#select-adjacent! @doc @node)       ; Select doc adjacent to node
(#set! is_export true)               ; Set custom property
```

## Adding New Queries

### Step 1: Identify the Pattern
Use tree-sitter CLI to explore your language's AST:
```bash
./parse -file example.{ext} -named_only
```

### Step 2: Write the Query
Create or update the appropriate `.scm` file in `queries/`

### Step 3: Test the Query
```bash
# Run against your specific file
./parse -file test_files/test.{ext} -use_tags_query -tags_query_dir queries

# Run all tests
./test.sh
```

### Step 4: Update Test Files
If adding new patterns, update `test_files/test.{ext}` and regenerate:
```bash
./goldens.sh  # Regenerate golden files
```

## Common Query Patterns

### Function Definition with Documentation
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

### Class with Body Extraction
```scm
(
  (class_definition
    name: (identifier) @name
    body: (class_body) @body) @definition.class
)
```

### Import with Named Items
```scm
(import_statement
  (import_specifier
    name: (identifier) @name
    alias: (identifier)? @alias))
```

### Method Call (Reference)
```scm
(call_expression
  function: (member_expression
    property: (property_identifier) @name)) @reference.call
```

## Language-Specific Notes

### Python
- Use `decorated_definition` to handle decorators
- Docstrings are `expression_statement` with `string` child
- `__init__` should be marked as constructor, not function

### JavaScript/TypeScript
- Handle both `class_declaration` and `export_statement` wrappers
- Arrow functions: `arrow_function` node
- Methods vs functions distinction via parent context

### Java
- All methods are within classes
- Use `method_declaration` node
- Constructors: `constructor_declaration` node

### Go
- Comment handling requires special regex matching
- Methods have `receiver` parameter
- Use `field_declaration_list` for struct fields

### C/C++
- Classes are `struct` or `class` nodes
- Use preprocessing for macro handling
- Special handling for function pointers

## Testing Your Changes

### 1. Create Test Case
Add test to `test_files/test.{ext}`:
```python
# Example for Python
def my_function(param1, param2):
    """Function documentation."""
    pass
```

### 2. Run Parser
```bash
./parse -file test_files/test.py -use_tags_query -tags_query_dir queries
```

### 3. Verify Output
Output should include:
```
Name: "my_function"
Doc: "Function documentation."
Definition (definition.function):
def my_function(param1, param2):
Parameters: (param1, param2)
```

### 4. Update Golden File
After validation, regenerate:
```bash
./parse -file test_files/test.py -use_tags_query -tags_query_dir queries > goldens/test.py.golden
./test.sh  # Verify
```

## Quality Checklist

- [ ] Query follows naming conventions
- [ ] Documentation captured when applicable
- [ ] Parameters/return types captured for functions
- [ ] Test case added to appropriate test file
- [ ] Golden file updated
- [ ] All tests pass (`./test.sh`)
- [ ] Query handles edge cases (empty bodies, decorators, etc.)
- [ ] No false positives or negatives
- [ ] Consistent with similar queries in other languages

## Submitting Changes

1. Create a feature branch
2. Add/modify queries in `queries/`
3. Update test files in `test_files/`
4. Regenerate golden files (`./goldens.sh`)
5. Run full test suite (`./test.sh`)
6. Document changes in commit message
7. Submit pull request with:
   - Description of changes
   - Rationale for new queries
   - Test results
   - Example outputs

## Common Issues

### Query Doesn't Match Anything
- Verify node names with `./parse -file test.{ext} -named_only`
- Check for typos in node type names
- Ensure parent/sibling relationships are correct

### False Positives
- Add more specific predicates
- Use `#not-has-parent?` or `#not-has-type?`
- Check regex patterns with `#match?`

### Performance Issues
- Avoid overly broad patterns
- Use specific node types instead of wildcards
- Test with larger files

## Resources

- [Tree-sitter Query Syntax](https://tree-sitter.github.io/tree-sitter/query-syntax)
- [Tree-sitter Predicates](https://tree-sitter.github.io/tree-sitter/using-parsers#query-predicates)
- [Language Grammars](https://github.com/tree-sitter)
- [khulnasoft-parse Issues](https://github.com/KhulnaSoft/khulnasoft-parse/issues)
