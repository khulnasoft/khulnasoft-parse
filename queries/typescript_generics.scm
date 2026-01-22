;; TypeScript/JavaScript Generic Parameters
;; Captures generic type usage and constraints

;; 0. Function with generics
(
  (function_declaration
    name: (identifier) @name
    type_parameters: (type_parameters) @type_parameters
    parameters: (_) @khulnasoft.parameters) @definition.function
  (#set! is_generic true)
)

;; 1. Class with generics
(
  (class_declaration
    name: (type_identifier) @name
    type_parameters: (type_parameters) @type_parameters
    body: (class_body) @body) @definition.class
  (#set! is_generic true)
)

;; 2. Generic type parameter with constraints
(
  (type_parameter
    name: (type_identifier) @name
    constraint: (_) @constraint) @definition.type_parameter
)

;; 3. Generic interface
(
  (interface_declaration
    name: (type_identifier) @name
    type_parameters: (type_parameters) @type_parameters
    body: (object_type) @body) @definition.interface
  (#set! is_generic true)
)

;; 4. Generic type reference
(
  (generic_type
    name: (type_identifier) @name
    type_arguments: (type_arguments
      (type) @type_arg)+) @reference.type
)
