;; Java Enums and Annotation Queries
;; Captures enum definitions and annotations/attributes

;; 0. Enum declarations
(
  (enum_declaration
    name: (identifier) @name
    body: (enum_body
      (enum_constant
        name: (identifier) @constant_name)* @constants) @body) @definition.enum
)

;; 1. Enum constants
(
  (enum_body
    (enum_constant
      name: (identifier) @name
      arguments: (arguments)? @constructor_args) @definition.constant)
)

;; 2. Annotation on class
(
  (annotation
    name: (identifier) @annotation_name) @_
  .
  (class_declaration
    name: (identifier) @class_name) @definition.class
  (#set! has_annotation true)
)

;; 3. Annotation on method
(
  (annotation
    name: (identifier) @annotation_name) @reference.annotation
  .
  (method_declaration
    name: (identifier) @method_name) @definition.method
  (#set! has_annotation true)
)

;; 4. Annotation on field
(
  (annotation
    name: (identifier) @annotation_name) @reference.annotation
  .
  (field_declaration
    declarator: (variable_declarator
      name: (identifier) @field_name)) @definition.variable
  (#set! has_annotation true)
)

;; 5. Parameterized annotation
(
  (annotation
    name: (identifier) @annotation_name
    arguments: (annotation_argument_list
      (element_value_pair
        key: (identifier) @key
        value: (_) @value)*)) @reference.annotation
)

;; 6. Interface definition
(
  (interface_declaration
    name: (identifier) @name
    body: (interface_body) @body) @definition.interface
)

;; 7. Annotation type definition
(
  (annotation_type_declaration
    name: (identifier) @name
    body: (annotation_type_body
      (annotation_type_element_declaration
        name: (identifier) @element_name)* @elements) @body) @definition.annotation_type
)
