;; Class declarations
(
  (comment)* @doc
  .
  (class_declaration
    name: (identifier) @name
    body: (class_body) @body) @definition.class
  (#select-adjacent! @doc @definition.class)
)