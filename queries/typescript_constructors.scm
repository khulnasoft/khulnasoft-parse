(
  (comment)* @doc
  .
  (_
    name: (property_identifier) @name
    parameters: (formal_parameters) @khulnasoft.parameters
    return_type: ([
      (type_annotation (_) @khulnasoft.return_type)
      (asserts_annotation (_) @khulnasoft.return_type)
      (type_predicate_annotation (_) @khulnasoft.return_type)
    ])?
    body: (_)? @body) @definition.constructor
  (#eq? @name "constructor")
  (#has-type? @definition.constructor method_definition method_signature abstract_method_signature)
  (#select-adjacent! @doc @definition.constructor)
)
