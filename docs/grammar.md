## Free Context Grammar
`program`→ `list_instructions`   

### Variables
`var_decl` → <TYPE> <NAME>
`var_def` → <TYPE> <NAME> = `any_lex`
          | <NAME> = `any_lex`
          | <NAME> <ASSIGN_ESP_OPERATORS> `any_lex`

`list_var_decl` → `var_decl`
                | `var_decl`, `list_var_decl`
                | E

### Array:
`array_decl_def` → <TYPE> [] <NAME>
                 | <TYPE> [] <NAME> = [ `list_any_lex` ]
                 | <NAME> = [ `list_any_lex` ]

### Function:
`function_def` → func <NAME> ( `list_var_decl` ) : void { `nfd_list_instructions` }
               | func <NAME> ( `list_var_decl` ) : <TYPE> { `nfd_list_instructions` return `any_lex` }
`function_call` → <NAME> ( `list_any_lex` )
`function_decl` → func <NAME> ( `list_var_decl` ) : <TYPE>

### Control
`control_instructions` → `if` | `while`

`if` → if (`bool_operation`) { `nfd_list_instructions` } `elif`
     | if (`bool_operation`) { `nfd_list_instructions` } `elif` else { `nfd_list_instructions`}
`elif` → elif (`bool_operation`) { `nfd_list_instructions` }
       | elif (`bool_operation`) { `nfd_list_instructions` } `elif`
       | E

`while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values:
`list_instructions` → `instructions`
                    | `instructions` `list_instructions`

`instructions`→ `control_instructions`
              | `var_decl`
              | `var_def`
              | `function_def`
              | `function_decl`
              | `function_call`
              | `array_decl_def`

`nfd_list_instructions` → `nfd_instructions`
                        | `nfd_instructions` `nfd_list_instructions`

`nfd_instructions`→ `control_instructions`
                  | `var_decl`
                  | `var_def`
                  | `function_call`
                  | `array_decl_def`

`list_any_lex` → `any_lex`
               | `any_lex` , `list_any_lex`
               | E

`any_lex` → <NAME>
          | <NUMBER>
          | <STRING>
          | `operation`
          | `function_call`

`operation` → `value` <ARITHM_OPERATORS> `value`
            | - `value`

`bool_operation` → ! `bool_operation` `bool_operation_P`
                 | not `bool_operation` `bool_operation_P`
                 | `any_lex` `bool_operation_P`

`bool_operation_P` → <COMP_OPERATORS> `bool_operation` `bool_operation_P`
                   | <COMP_OPERATORS> `bool_operation` `bool_operation_P`
                   | E

`value` → <NAME>
        | <NUMBER>
        | `function_call`

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
