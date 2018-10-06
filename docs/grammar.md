## Free Context Grammar
`program`→ `list_instructions`   

### Variables
`def_decl_call` → <TYPE> `def_decl_call_1`
               | <NAME> `def_decl_call_2`

`def_decl_call_1` →  <NAME> `def_decl_call_1_1`
                 |  [] <NAME>  `def_decl_call_1_2`

`def_decl_call_1_1` → = `any_lex`
                   | E

`def_decl_call_1_2` → = [ `list_any_lex` ] 
                   | E


`def_decl_call_2` → = `def_decl_call_2_1`
                 | <ASSIGN_ESP_OPERATORS> `any_lex`
                 | `func_call_1`

`def_decl_call_2_1` → `any_lex`
                   | [ `list_any_lex` ]


`list_var_decl` → <TYPE> <NAME> `list_var_decl_1`

`list_var_decl_1` → , `list_var_decl`
                  | E

### Function:
`func_def_decl` → func <NAME> ( `list_var_decl` ) : `func_def_decl_1`

`func_def_decl_1` → void { `nfd_list_instructions` }
                  | <TYPE> `func_def_decl_2`

`func_def_decl_2` → { `nfd_list_instructions` return `any_lex` }
                  | E

`func_call_1` → ( `list_any_lex` )

### Control
`control_instructions` → `if` 
                       | `while`

`if` → if (`bool_operation`) { `nfd_list_instructions` } `elif` `if_1`

`if_1` → else { `nfd_list_instructions`}
       | E

`elif` → elif (`bool_operation`) { `nfd_list_instructions` } `elif_1`
       | E

`elif_1` → `elif`
         | E

`while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values:
`list_instructions` → `instructions` `list_instructions_1`

`list_instructions_1` → `list_instructions` 
                      | E

`instructions`→ `nfd_instructions`
              | `func_def_decl`

`nfd_list_instructions` → `nfd_instructions` `nfd_list_instructions_1`

`nfd_list_instructions_1` → `nfd_list_instructions` 
                          | E

`nfd_instructions`→ `control_instructions`
                  | `def_decl_call`

`list_any_lex` → `any_lex` `list_any_lex_1`
               | E

`list_any_lex_1` → , `list_any_lex`
                 | E

`any_lex` → <STRING>
          | `operation`


### Operation
`operation` -> `operand` `operation_1`
`operation_1` -> <ARITHM_OPERATORS> `operand` `operation_1`
              | E
`operand` -> `value`
          |  - `value`

### Bool_Operation
`bool_operation` -> `comp_operation` `bool_operation_1`
`bool_operation_1` -> <BOOL_OPERATORS> `comp_operation` `bool_operation_1`
                   | E

`comp_operation` -> `any_lex` `comp_operation_1`
                 |  ! `any_lex`
                 | not `any_lex`

`comp_operation_1` -> <COMP_OPERATORS> `any_lex`
                   | E

### Callable Values
`value` → <NAME> `value_1`
        | <NUMBER>


`value_1` →`func_call_1`
          | E

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
