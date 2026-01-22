;; Class declarations
(
  (comment)* @doc
  .
  (class_declaration
    name: (identifier) @name
    body: (class_body) @body) @definition.class
  (#select-adjacent! @doc @definition.class)
)

;; Function calls
(
  (call_expression
    function: (identifier) @name) @reference.call
  (#not-match? @name "^(require)$")
)

;; Member function calls
(
  (call_expression
    function: (member_expression
      property: (property_identifier) @name)
    arguments: (_)) @reference.call
)

;; Class constructors
(new_expression
  constructor: (_) @name) @reference.class

