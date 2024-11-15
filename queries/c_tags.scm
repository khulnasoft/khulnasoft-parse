;; Basic function definitions
(
  (comment)* @doc
  .
  (function_definition
    type: (_)? @khulnasoft.return_type
    declarator: (function_declarator
      declarator: (identifier) @name
      parameters: (parameter_list) @khulnasoft.parameters
    )
    body: (_)? @body
  ) @definition.function
  (#select-adjacent! @doc @definition.function)
)

;; Function to pointer
(
  (comment)* @doc
  .
  (function_definition
    type: (_)? @khulnasoft.return_type
    declarator: (pointer_declarator
      declarator: (function_declarator
        declarator: (identifier) @name
        parameters: (parameter_list) @khulnasoft.parameters
      )
    )
    body: (_)? @body
  ) @definition.function
  (#select-adjacent! @doc @definition.function)
)

;; Imports

(
  (preproc_include
    path: (_) @name
  ) @definition.import
)
