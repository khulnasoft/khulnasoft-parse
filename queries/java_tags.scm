(program
  (package_declaration
    "package"
    .
    (_) @name
    .
    ";") @definition.package
  (#lineage-from-name! ".")
) @khulnasoft.lineage_node

;; Class and record
(
  [
    (line_comment)
    (block_comment)
  ]* @doc
  .
  (class_declaration
    name: (identifier) @name
    body: (class_body)? @body
  ) @definition.class
  (#select-adjacent! @doc @definition.class)
)

(
  [
    (line_comment)
    (block_comment)
  ]* @doc
  .
  (record_declaration
    name: (identifier) @name
    parameters: (formal_parameters) @body
    body: (class_body)? @body
  ) @definition.class
  (#select-adjacent! @doc @definition.class)
)

(
  [
    (line_comment)
    (block_comment)
  ]* @doc
  .
  (interface_declaration
    name: (identifier) @name) @definition.interface
  (#select-adjacent! @doc @definition.interface)
)

(
  [
    (line_comment)
    (block_comment)
  ]* @doc
  .
  (method_declaration
    name: (identifier) @name
    parameters: (formal_parameters) @khulnasoft.parameters
    body: (block)? @body) @definition.method
  (#select-adjacent! @doc @definition.method)
)

;; Additional patterns for capturing record declarations
(
  [
    (line_comment)
    (block_comment)
  ]* @doc
  .
  (record_declaration
    name: (identifier) @name
    parameters: (formal_parameters) @khulnasoft.parameters
    body: (class_body)? @body
  ) @definition.record
  (#select-adjacent! @doc @definition.record)
)
