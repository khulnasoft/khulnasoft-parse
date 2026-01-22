;; Python Variable Definitions
;; Captures module-level and significant variable declarations

;; 0. Module-level variable assignments (not in class/function)
(
  (module
    (assignment
      left: (identifier) @name
      right: (_) @value) @definition.variable)
  (#not-has-parent? @definition.variable function_definition class_definition)
)

;; 1. Annotated variables with type hints
(
  (annotated_assignment
    name: (identifier) @name
    type: (type) @khulnasoft.type_annotation
    value: (_)? @value) @definition.variable
  (#not-has-parent? @definition.variable function_definition class_definition)
)

;; 2. Class-level variables
(
  (class_definition
    body: (block
      (assignment
        left: (identifier) @name
        right: (_) @value) @definition.variable))
)

;; 3. Constant-like variables (UPPERCASE naming)
(
  (assignment
    left: (identifier) @name
    right: (_) @value) @definition.constant
  (#match? @name "^[A-Z][A-Z0-9_]*$")
  (#not-has-parent? @definition.constant function_definition)
)

;; 4. Global keyword variables
(
  (global_statement
    name: (identifier) @name) @definition.variable
  (#set! is_global true)
)
