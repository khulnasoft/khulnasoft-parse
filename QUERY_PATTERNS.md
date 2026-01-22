# Query Patterns Documentation

## Overview
This document provides detailed documentation for all tree-sitter query patterns used in khulnasoft-parse.

## Standard Capture Types

### Definition Captures (`@definition.*`)
Used to identify points where identifiers are defined or introduced.

| Capture Type | Purpose | Supported Languages |
|---|---|---|
| `@definition.class` | Class/struct/record definitions | All |
| `@definition.function` | Function/procedure definitions | Most |
| `@definition.method` | Method definitions | Most |
| `@definition.constructor` | Constructor definitions | Python, Java, C#, TypeScript, Kotlin |
| `@definition.interface` | Interface definitions | TypeScript, Java, Go, C#, Kotlin |
| `@definition.namespace` | Namespace/module definitions | TypeScript, C++, C#, PHP |
| `@definition.module` | Module definitions | TypeScript, Python, Ruby |
| `@definition.type` | Type alias definitions | TypeScript, Go |
| `@definition.constant` | Constant definitions | All (new) |
| `@definition.enum` | Enum definitions | All languages (new) |
| `@definition.import` | Import statements | Most |
| `@definition.include` | Include directives | C/C++ |
| `@definition.package` | Package declarations | Java, Go |
| `@definition.variable` | Variable declarations | All (new) |
| `@definition.exception` | Exception class definitions | All (new) |
| `@definition.decorator` | Decorator/annotation application | Python, TypeScript/JavaScript (new) |
| `@definition.property` | Property definitions | TypeScript/JavaScript (new) |
| `@definition.exception_handler` | Try-catch-finally blocks | All (new) |
| `@definition.annotation_type` | Annotation type definitions | Java (new) |
| `@definition.type_parameter` | Generic type parameters | TypeScript (new) |

### Reference Captures (`@reference.*`)
Used to identify points where identifiers are used or referenced.

| Capture Type | Purpose |
|---|---|
| `@reference.call` | Function/method calls |
| `@reference.class` | Class instantiation/usage |
| `@reference.type` | Type references |
| `@reference.import` | Import usage |
| `@reference.function` | Function references |
| `@reference.annotation` | Annotation usage |
| `@reference.exception` | Exception throwing/references |

### Metadata Captures
Additional information attached to definitions.

| Capture Type | Purpose | Example |
|---|---|---|
| `@doc` | Documentation/comments | `/// Doc comment` |
| `@khulnasoft.parameters` | Function parameters | `(a, b, c)` |
| `@khulnasoft.return_type` | Return type annotation | `-> int` |
| `@body` | Function/class body | `{ ... }` |
| `@name` | Identifier name | `myFunction` |
| `@parent` | Parent class name | For inherited/interface methods |

### Custom Properties (`#set! key value`)
Properties set during query execution.

| Property | Values | Meaning |
|---|---|---|
| `is_export` | `true` | Definition is exported |
| `is_generic` | `true` | Definition has type parameters |
| `is_global` | `true` | Variable has global scope |
| `is_struct` | `true` | Type is a struct |
| `is_scoped` | `true` | Scoped enum (C++11) |
| `is_rethrow` | `true` | Re-throwing exception |
| `is_defer` | `true` | Deferred operation |
| `returns_error` | `true` | Function returns error (Go pattern) |
| `declares_throws` | `true` | Method declares throws (Java) |
| `handler_type` | `try_catch`, `try_finally`, etc. | Type of exception handler |
| `decorator_target` | `function`, `class` | Target of decorator |
| `is_property` | `true` | Definition is a property |
| `interface_impl` | `true` | Method implements interface |

---

## Language-Specific Patterns

### Python Patterns

#### Class Definition
```scm
(
  (class_definition
    name: (identifier) @name
    body: (block . (expression_statement . (string) @doc .)?) @body)
  ) @definition.class
)
```

#### Function Definition
```scm
(
  (function_definition
    name: (identifier) @name
    parameters: (parameters) @khulnasoft.parameters
    body: (block . (expression_statement . (string) @doc .)?)
  ) @definition.function
)
```

#### Decorated Function (new)
```scm
(
  (decorated_definition
    (decorator "@" (identifier) @decorator_name)
    definition: (function_definition
      name: (identifier) @name
    )
  ) @definition.decorator
)
```

#### Variable Declaration (new)
```scm
(
  (assignment
    left: (identifier) @name
    right: (_) @value
  ) @definition.variable
  (#not-has-parent? @definition.variable function_definition class_definition)
)
```

#### Exception Handling (new)
```scm
(
  (try_statement
    body: (_) @body
    (except_clause
      exception_type: (_)? @exception_type
      (_)? @exception_name
      body: (_) @handler
    ) @reference.exception+
  ) @definition.exception_handler
)
```

### TypeScript/JavaScript Patterns

#### Type Alias (new)
```scm
(type_alias_declaration
  name: (type_identifier) @name
  value: (_) @type_definition
) @definition.type
```

#### Interface Declaration (new)
```scm
(interface_declaration
  name: (type_identifier) @name
  body: (object_type) @body
) @definition.interface
```

#### Enum Declaration (new)
```scm
(enum_declaration
  name: (identifier) @name
  body: (enum_body) @body
) @definition.enum
```

#### Generic Function (new)
```scm
(function_declaration
  name: (identifier) @name
  type_parameters: (type_parameters) @type_parameters
  parameters: (_) @khulnasoft.parameters
) @definition.function
(#set! is_generic true)
```

#### Exception Handling (new)
```scm
(try_statement
  body: (statement_block) @body
  (catch_clause
    parameter: (_) @error_param
    body: (statement_block) @catch_body
  ) @reference.exception+
) @definition.exception_handler
```

### Go Patterns

#### Type Alias (new)
```scm
(type_declaration
  (type_spec
    name: (type_identifier) @name
    type: (_) @type_definition
  ) @definition.type
  (#not-match? @definition.type "^type (struct|interface)")
)
```

#### Const Block with Iota (new)
```scm
(const_declaration
  (const_spec
    name: (identifier) @name
    value: (identifier) @enum_value
    (#eq? @enum_value "iota")
  ) @definition.enum
)
```

#### Error Handling Pattern (new)
```scm
(if_statement
  condition: (binary_expression
    left: (identifier) @error_var
    operator: "!="
    right: (identifier) @nil_check
    (#eq? @error_var "err")
    (#eq? @nil_check "nil")
  ) @reference.exception
)
```

### Java Patterns

#### Enum Declaration (new)
```scm
(enum_declaration
  name: (identifier) @name
  body: (enum_body
    (enum_constant
      name: (identifier) @constant_name
    )* @constants
  ) @body
) @definition.enum
```

#### Annotation (new)
```scm
(annotation
  name: (identifier) @annotation_name
) @reference.annotation
.
(method_declaration
  name: (identifier) @method_name
) @definition.method
(#set! has_annotation true)
```

#### Exception Handling (new)
```scm
(try_statement
  body: (block) @body
  (catch_clause
    (catch_formal_parameter
      type: (type_identifier) @exception_type
      name: (identifier) @exception_var
    )
    body: (block) @catch_body
  ) @reference.exception+
) @definition.exception_handler
```

#### Method Throws Declaration (new)
```scm
(method_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @khulnasoft.parameters
  throws: (throws
    (type_identifier) @exception_type
  )+ @exceptions
) @definition.method
(#set! declares_throws true)
```

### C++ Patterns

#### Enum Declaration (new)
```scm
(enum_specifier
  name: (identifier) @name
  body: (enumerator_list
    (enumerator
      name: (identifier) @constant_name
      value: (_)? @constant_value
    )* @constants
  ) @body
) @definition.enum
```

#### Scoped Enum C++11 (new)
```scm
(enum_specifier
  name: (scoped_identifier
    scope: (namespace_identifier) @namespace
    name: (identifier) @enum_name
  )
  body: (enumerator_list) @body
) @definition.enum
(#set! is_scoped true)
```

#### Try-Catch (new)
```scm
(try_statement
  body: (compound_statement) @body
  (catch_clause
    (parameter_declaration
      type: (_) @exception_type
      declarator: (identifier)? @exception_var
    )
    body: (compound_statement) @catch_body
  ) @reference.exception+
) @definition.exception_handler
```

#### Exception Specification (new)
```scm
(function_definition
  (function_declarator
    declarator: (identifier) @function_name
    parameters: (_) @parameters
    (noexcept_specifier)? @noexcept
  )
) @definition.function
(#set! no_except true)
```

---

## Common Predicates Reference

### Type Checking
```scm
(#has-type? @node type1 type2)      ;; Match multiple types
(#not-has-type? @node type)          ;; Exclude type
```

### Parent/Sibling Checks
```scm
(#not-has-parent? @node parent_type) ;; Not child of parent
```

### Text Matching
```scm
(#match? @node "regex_pattern")      ;; Regex match
(#not-match? @node "regex")          ;; Regex not match
(#eq? @node "exact_string")          ;; Exact string match
(#not-eq? @node "string")            ;; Not equal
```

### Capture Selection
```scm
(#select-adjacent! @doc @definition) ;; Link adjacent doc to definition
```

### Custom Properties
```scm
(#set! property_name value)          ;; Set metadata property
```

---

## Best Practices

1. **Documentation First**: Always capture `@doc` when available
2. **Complete Metadata**: Capture parameters and return types
3. **Consistency**: Use standard capture names across languages
4. **Specificity**: Use precise node types and predicates
5. **Testing**: Verify queries with actual code examples
6. **Performance**: Avoid overly broad patterns
7. **Comments**: Document complex patterns in `.scm` files

---

## Query Files Organization

### Main Query Files
- `{language}_tags.scm` - Core definitions and references

### Feature-Specific Files (new)
- `{language}_variables.scm` - Variable declarations (new)
- `{language}_enums.scm` - Enum definitions (new)
- `{language}_types.scm` - Type aliases and definitions (new)
- `{language}_exceptions.scm` - Exception handling (new)
- `{language}_decorators.scm` - Decorators/annotations (new)
- `{language}_generics.scm` - Generic types (new)
- `{language}_imports.scm` - Import statements
- `{language}_class_fields.scm` - Class members
- `{language}_constructors.scm` - Constructors
- `{language}_functions.scm` - Function patterns
- `{language}_injections.scm` - Language injections

---

## Adding New Queries

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.
