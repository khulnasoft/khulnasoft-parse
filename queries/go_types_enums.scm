;; Go Enum-like Constants and Type Aliases
;; Captures const blocks, iota, and type definitions

;; 0. Const block declarations
(
  (const_declaration
    (const_spec
      name: (identifier) @name
      value: (_) @value) @definition.constant)+
)

;; 1. Iota-based enums (enum-like pattern)
(
  (const_declaration
    (const_spec
      name: (identifier) @name
      value: (identifier) @enum_value
      (#eq? @enum_value "iota")) @definition.enum)
)

;; 2. Type alias definitions
(
  (type_declaration
    (type_spec
      name: (type_identifier) @name
      type: (_) @type_definition
      (#not-match? @type_definition "^(struct|interface)")) @definition.type)
)

;; 3. Interface type definitions
(
  (type_declaration
    (type_spec
      name: (type_identifier) @name
      type: (interface_type
        (interface_method_receiver_list)? @body))) @definition.interface
)

;; 4. Struct as enum-like type
(
  (type_declaration
    (type_spec
      name: (type_identifier) @name
      type: (struct_type
        (field_declaration_list) @body))) @definition.type
  (#set! is_struct true)
)

;; 5. Exported constants
(
  (const_declaration
    (const_spec
      name: (identifier) @name
      (#match? @name "^[A-Z]")
      value: (_) @value) @definition.constant)
)

;; 6. Interface implementation check
(
  (method_declaration
    receiver: (parameter_list
      (parameter_declaration
        type: (type_identifier) @receiver_type))
    name: (field_identifier) @method_name) @definition.method
  (#set! interface_impl true)
)
