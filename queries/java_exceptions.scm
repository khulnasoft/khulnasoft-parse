;; Java Exception Handling Queries
;; Captures try-catch-finally blocks and exception throwing

;; 0. Try-catch blocks
(
  (try_statement
    body: (block) @body
    ((catch_clause
      (catch_formal_parameter
        type: (type_identifier) @exception_type
        name: (identifier) @exception_var)
      body: (block) @catch_body) @reference.exception)+) @definition.exception_handler
  (#set! handler_type "try_catch")
)

;; 1. Try-finally blocks
(
  (try_statement
    body: (block) @body
    (finally_clause
      body: (block) @finally_body) @definition.exception_handler)
  (#set! handler_type "try_finally")
)

;; 2. Try with resources
(
  (try_with_resources_statement
    (resource_specification
      (resource
        (variable_declarator
          name: (identifier) @resource_name
          value: (_) @resource_init) @resource_var
      )+
    ) @resources
    body: (block) @body) @definition.exception_handler
  (#set! handler_type "try_resource")
)

;; 3. Throw statements
(
  (throw_statement
    (object_creation_expression
      type: (type_identifier) @exception_type
      arguments: (argument_list) @constructor_args) @_) @reference.exception
)

;; 4. Simple throw
(
  (throw_statement
    (identifier) @exception_name) @reference.exception
)

;; 5. Method throws declaration
(
  (method_declaration
    name: (identifier) @name
    parameters: (formal_parameters) @khulnasoft.parameters
    throws: (throws
      (type_identifier) @exception_type)+ @exceptions) @definition.method
  (#set! declares_throws true)
)

;; 6. Constructor throws declaration
(
  (constructor_declaration
    name: (identifier) @constructor_name
    parameters: (formal_parameters) @khulnasoft.parameters
    throws: (throws
      (type_identifier) @exception_type)+) @definition.constructor
  (#set! declares_throws true)
)

;; 7. Custom exception class
(
  (class_declaration
    name: (identifier) @name
    superclass: (superclass
      (type_identifier) @parent
      (#match? @parent "Exception|Error|Throwable$"))) @definition.exception
)

;; 8. Exception interface
(
  (interface_declaration
    name: (identifier) @name
    (#match? @name "Exception|Error|Throwable$")) @definition.exception
)
