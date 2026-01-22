;; C/C++ Enum Definitions
;; Captures enum declarations and constants

;; 0. Enum declarations
(
  (enum_specifier
    name: (identifier) @name
    body: (enumerator_list
      (enumerator
        name: (identifier) @constant_name
        value: (_)? @constant_value)* @constants) @body) @definition.enum
)

;; 1. Typedef enum
(
  (declaration
    (storage_class_specifier)? @storage
    (enum_specifier
      name: (identifier)? @enum_name
      body: (enumerator_list) @body) @_
    declarator: (identifier) @typedef_name) @definition.enum
  (#eq? @storage "typedef")
)

;; 2. Anonymous enum with typedef
(
  (declaration
    (storage_class_specifier)? @storage
    (enum_specifier
      body: (enumerator_list
        (enumerator
          name: (identifier) @constant_name)+ @constants) @body) @_
    declarator: (identifier) @typedef_name) @definition.enum
  (#eq? @storage "typedef")
)

;; 3. Enum constants
(
  (enumerator
    name: (identifier) @name
    value: (number_literal) @value) @definition.constant
)

;; 4. Scoped enum (C++11)
(
  (enum_specifier
    name: (scoped_identifier
      scope: (namespace_identifier) @namespace
      name: (identifier) @enum_name) @_
    body: (enumerator_list) @body) @definition.enum
  (#set! is_scoped true)
)
