## Free Context Grammar
`program` → `list_instructions`   

### Variables
`def_decl` → <TYPE> `def_decl_P` 
`def_decl_P` → <NAME> `def_decl_P_var`
             | [] <NAME> `def_decl_P_arr`
`def_decl_P_var` → = `any_lex`
                 | E
`def_decl_P_arr` → = [ `list_any_lex` ]
                 | E

`assign` → <NAME> `assign_P` 
`assign_P` → = `assign_P1`
           | <ASSIGN_ESP_OPERATORS> `any_lex`
`assign_P1` → `any_lex`
            | [ `list_any_lex` ]

`list_var_decl` → <TYPE> <NAME> `list_var_decl_P`
                | E
`list_var_decl_P` → , `list_var_decl` 
                  | E

### Function:
`func_def_decl` → func <NAME> ( `list_var_decl` ) : `func_def_decl_P`
`func_def_decl_P` → void { `nfd_list_instructions` } 
                  | <TYPE> `func_def_decl_P1`
`func_def_decl_P1` → { `nfd_list_instructions` return `any_lex` }
                   | E

`function_call` → <NAME> ( `list_any_lex` )

### Control
`control_instructions` → `if` 
                       | `while`

`if` → if (`bool_operation`) { `nfd_list_instructions` } `elif` `if_P`
`if_P` →  else { `nfd_list_instructions`} 
       | E
`elif` → elif (`bool_operation`) { `nfd_list_instructions` } `elif_P`
       | E
`elif_P` → `elif`
         | E

`while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values:
`list_instructions` → `instructions` `list_instructions_P`
`list_instructions_P` → `list_instructions`
                      | E

`instructions`→ `control_instructions`
              | `def_decl`
              | `assign`
              | `func_def_decl`
              | `function_call`

`nfd_list_instructions` → `nfd_instructions` `nfd_list_instructions_P`
`nfd_list_instructions_P` → , `nfd_instruction_list_P`
                          | E 

`nfd_instructions`→ `control_instructions`
                  | `def_decl`
                  | `assign` 
                  | `function_call`

`list_any_lex` → `any_lex` `list_any_lex_P`
               | E
`list_any_lex_P` → , `list_any_lex`
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
                   | <BOOL_OPERATORS> `bool_operation` `bool_operation_P`
                   | E

`value` → <NAME>
        | <NUMBER>
        | `function_call`

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
