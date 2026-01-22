;; Python Decorator/Annotation Queries
;; Captures decorators and class/function annotations

;; 0. Function decorators
(
  (decorated_definition
    (decorator
      "@"
      (identifier) @name) @definition.decorator
    definition: (function_definition
      name: (identifier) @function_name) @definition.function)
  (#set! decorator_target "function")
)

;; 1. Class decorators
(
  (decorated_definition
    (decorator
      "@"
      (identifier) @name) @definition.decorator
    definition: (class_definition
      name: (identifier) @class_name) @definition.class)
  (#set! decorator_target "class")
)

;; 2. Decorator with arguments
(
  (decorated_definition
    (decorator
      "@"
      (attribute
        object: (identifier) @module
        attribute: (identifier) @name)
      arguments: (argument_list) @khulnasoft.parameters) @definition.decorator)
)

;; 3. Property decorator (special case)
(
  (decorated_definition
    (decorator
      "@"
      (identifier) @name
      (#eq? @name "property")
    ) @definition.property)
)
