;; C/C++ Exception Handling Queries
;; Captures try-catch blocks and throw statements

;; 0. Try-catch blocks (C++)
(
  (try_statement
    body: (compound_statement) @body
    (catch_clause
      (parameter_declaration
        type: (_) @exception_type
        declarator: (identifier)? @exception_var)
      body: (compound_statement) @catch_body) @reference.exception+) @definition.exception_handler
  (#set! handler_type "try_catch")
)

;; 1. Throw statements
(
  (throw_statement
    argument: (new_expression
      type: (type_identifier) @exception_type
      arguments: (argument_list) @constructor_args) @_) @reference.exception
)

;; 2. Simple throw
(
  (throw_statement
    argument: (identifier) @exception_name) @reference.exception
)

;; 3. Rethrow (throw without argument)
(
  (throw_statement) @reference.exception
  (#set! is_rethrow true)
)

;; 4. noexcept specifier (C++11)
(
  (function_definition
    (storage_class_specifier)? @_
    (function_declarator
      declarator: (identifier) @function_name
      parameters: (_) @parameters
      (noexcept_specifier)? @noexcept) @definition.function
  (#set! no_except true)
)

;; 5. Exception specification (deprecated)
(
  (exception_specification
    (type_identifier) @exception_type)+ @definition.exception_handler
)

;; 6. Custom exception class
(
  (class_specifier
    name: (type_identifier) @name
    (base_class_clause
      (base_class
        (type_identifier) @parent
        (#match? @parent "exception|Exception|std::exception")))? @_
  ) @definition.exception
)
