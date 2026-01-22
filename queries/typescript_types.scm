;; TypeScript/JavaScript Type Aliases and Interfaces
;; Captures type definitions, interfaces, and generic types

;; 0. Type alias declarations
(
  (type_alias_declaration
    name: (type_identifier) @name
    value: (_) @type_definition) @definition.type
)

;; 1. Interface declarations (TypeScript)
(
  (interface_declaration
    name: (type_identifier) @name
    body: (object_type) @body) @definition.interface
)

;; 2. Generic type parameters
(
  (type_parameters
    (type_parameter
      name: (type_identifier) @name) @definition.type_parameter)
)

;; 3. Enum declarations
(
  (enum_declaration
    name: (identifier) @name
    body: (enum_body) @body) @definition.enum
)

;; 4. Exported type aliases
(
  (export_statement
    declaration: (type_alias_declaration
      name: (type_identifier) @name
      value: (_) @type_definition) @_) @definition.type
  (#set! is_export true)
)

;; 5. Exported interfaces
(
  (export_statement
    declaration: (interface_declaration
      name: (type_identifier) @name
      body: (object_type) @body) @_) @definition.interface
  (#set! is_export true)
)

;; 6. Exported enums
(
  (export_statement
    declaration: (enum_declaration
      name: (identifier) @name
      body: (enum_body) @body) @_) @definition.enum
  (#set! is_export true)
)

;; 7. Union type definitions
(
  (union_type
    (identifier) @member_type)+ @definition.type
  (#set! type_kind "union")
)

;; 8. Intersection type definitions
(
  (intersection_type
    (identifier) @member_type)+ @definition.type
  (#set! type_kind "intersection")
)
