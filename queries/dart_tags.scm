;; We treat mixins and classes as the same
(
  [
    (documentation_comment)
  ]* @doc
  .
  (class_definition
    name: (identifier) @name
    body: (class_body) @body
    type_parameters: (type_parameters)?
  ) @definition.class
  (#select-adjacent! @doc @definition.class)
)

(
  [
    (documentation_comment)
  ]* @doc
  .
  (mixin_declaration
    (mixin)
    .
    (identifier) @name
    (class_body)? @body
  ) @definition.class
  (#select-adjacent! @doc @definition.class)
)

;; Functions
(
  [
    (documentation_comment)
  ]* @doc
  .
  (
    (function_signature
      name: (identifier) @name
      (formal_parameter_list) @khulnasoft.parameters
    )
    .
    (function_body)? @body
  ) @definition.function
  (#select-adjacent! @doc @definition.function)
  (#not-has-parent? @definition.function method_signature)
)

(
  [
    (documentation_comment)
  ]* @doc
  .
  (
    (method_signature
      (function_signature
        name: (identifier) @name
        (formal_parameter_list) @khulnasoft.parameters
      )
    )
    .
    (function_body)? @body
  ) @definition.function
  (#select-adjacent! @doc @definition.function)
)

;; Additional patterns for capturing mixin declarations
(
  [
    (documentation_comment)
  ]* @doc
  .
  (mixin_declaration
    (mixin)
    .
    (identifier) @name
    (class_body)? @body
  ) @definition.mixin
  (#select-adjacent! @doc @definition.mixin)
)
