;; Python Exception/Error Handling Queries
;; Captures try-except-finally blocks and exception definitions

;; 0. Try-except blocks
(
  (try_statement
    body: (_) @body
    ((except_clause
      (exception_type)? @exception_type
      (identifier)? @exception_name
      body: (_) @handler_body) @reference.exception)+) @definition.exception_handler
  (#set! handler_type "except")
)

;; 1. Try-finally blocks
(
  (try_statement
    body: (_) @body
    (finally_clause
      body: (_) @finally_body) @definition.exception_handler)
  (#set! handler_type "finally")
)

;; 2. Raise statements
(
  (raise_statement
    exception: (identifier) @exception_name) @reference.exception
)

;; 3. Exception as specific type capture
(
  (except_clause
    exception_type: (attribute
      object: (identifier) @module
      attribute: (identifier) @exception_name)) @reference.exception
)

;; 4. Custom exception definitions
(
  (class_definition
    name: (identifier) @name
    superclasses: (argument_list
      (identifier) @parent
      (#match? @parent "Exception|Error$")) @reference.exception
  ) @definition.exception
)
