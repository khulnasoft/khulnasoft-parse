;; Go Exception/Error Handling Queries
;; Captures error returns and error handling patterns

;; 0. Error return pattern (standard Go)
(
  (function_declaration
    name: (identifier) @name
    parameters: (parameter_list) @khulnasoft.parameters
    result: (parameter_list
      (parameter_declaration
        type: (identifier) @return_type
        (#eq? @return_type "error"))) @definition.function
  (#set! returns_error true)
)

;; 1. Named error return values
(
  (method_declaration
    receiver: (parameter_list
      (parameter_declaration
        type: (type_identifier)))
    name: (field_identifier) @method_name
    result: (parameter_list
      (parameter_declaration
        name: (identifier)? @error_name
        type: (identifier) @_
        (#eq? @_ "error"))) @definition.method
  (#set! returns_error true)
)

;; 2. Error check pattern (if err != nil)
(
  (if_statement
    condition: (binary_expression
      left: (identifier) @error_var
      operator: "!="
      right: (identifier) @nil_check
      (#eq? @nil_check "nil")) @reference.exception
    (#eq? @error_var "err"))
)

;; 3. Panic statements (similar to exceptions)
(
  (call_expression
    function: (identifier) @function_name
    arguments: (argument_list
      (_) @panic_msg) @_)
  (#eq? @function_name "panic") @reference.exception
)

;; 4. Custom error type definition
(
  (type_declaration
    (type_spec
      name: (type_identifier) @name
      type: (interface_type
        (interface_method_receiver_list
          (method_spec
            name: (field_identifier) @method
            (#eq? @method "Error")))))) @definition.exception
)

;; 5. Defer error handling
(
  (defer_statement
    (call_expression
      function: (identifier) @function_name
      (#match? @function_name "recover|Close|Release")) @reference.exception
    (#set! is_defer true))
)
