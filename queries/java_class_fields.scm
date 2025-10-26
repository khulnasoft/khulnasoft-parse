;; Captures field declarations in Java classes
(class_declaration
    (class_body
        (field_declaration) @field
    )
)

;; Captures constructor declarations in Java classes
(class_declaration
    (class_body
        ([
            (constructor_declaration)
        ]) @definition.constructor
    )
)

;; Captures field declarations in Java records (as parameters)
(record_declaration
    (formal_parameters
        (formal_parameter) @field
    )
)

;; Captures constructor declarations in Java records
(record_declaration
    (class_body
        ([
            (constructor_declaration)
            (compact_constructor_declaration)
        ]) @definition.constructor
    )
)
