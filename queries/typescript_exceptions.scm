;; TypeScript Exception/Error Handling Queries
;; Captures try-catch-finally blocks and error handling

;; 0. Try-catch blocks
(
  (try_statement
    body: (statement_block) @body
    ((catch_clause
      (parameter) @error_param
      body: (statement_block) @catch_body) @reference.exception)+) @definition.exception_handler
  (#set! handler_type "try_catch")
)

;; 1. Try-finally blocks
(
  (try_statement
    body: (statement_block) @body
    (finally_clause
      body: (statement_block) @finally_body) @definition.exception_handler)
  (#set! handler_type "try_finally")
)

;; 2. Throw statements
(
  (throw_statement
    (new_expression
      constructor: (identifier) @exception_type
      arguments: (arguments) @constructor_args) @_) @reference.exception
)

;; 3. Simple throw
(
  (throw_statement
    (identifier) @exception_name) @reference.exception
)

;; 4. Custom error class definition
(
  (class_declaration
    name: (type_identifier) @name
    superclass: (expression
      (identifier) @parent
      (#match? @parent "Error|Exception$"))) @definition.exception
)

;; 5. Error interface/type
(
  (interface_declaration
    name: (type_identifier) @name
    (#match? @name "Error|Exception$")) @definition.exception
)
