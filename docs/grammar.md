## Free Context Grammar
`program`→ `list_instructions`   
`type` → int | float | void | string  

### Variables
`var_decl` → `type` <NAME>
`var_def` → `type` <NAME> = `any_lex`
          | <NAME> = `any_lex`  
          | <NAME> `assign_esp_operators` `any_lex`

`list_var_decl` → `var_decl` 
                | `var_decl`, `list_var_decl` 
                | E

### Array:
`array_decl_def` → `type` [] <NAME> 
                 | `type` [] <NAME> = [ `list_any_lex` ]
                 | <NAME> = [ `list_any_lex` ]

### Function:
`function_def` → func <NAME> ( `list_var_decl` ) : `type` { `list_instructions` return `any_lex` }   
               | func <NAME> ( `list_var_decl` ) : void { `list_instructions` }   
`function_call` → <NAME> ( `list_any_lex` )   
`function_decl` → <NAME> ( `list_var_decl` ) : `type`  

### Control
`control_instructions` → `if` | `while`   

`if` → if (`bool_operation`) { `list_instructions` } `elif`
     | if (`bool_operation`) { `list_instructions` } `elif` else { `list_instructions`}
`elif` → elif (`bool_operation`) { `list_instructions` } 
       | elif (`bool_operation`) { `list_instructions` } `elif` 
       | E  

`while` → while (`bool_operation`) {`list_instructions`}

### Values:
`list_instructions` → `instructions` 
                    | `instructions` `list_instructions` 

`instructions`→ `control_instructions` 
              | `var_decl`
              | `var_def` 
              | `function_def` 
              | `array_decl_def`  

`list_any_lex` → `any_lex` 
               | `any_lex` , `list_any_lex` 
               | E   

`any_lex` → <NAME> 
          | <NUMBER>
          | <STRING> 
          | `operation` 
          | `function_call`  

`operation` → `value` `arithm_operators` `value` 
            | - `value`

`bool_operation` → `bool_operation` `comp_operators` `bool_operation`
                 | `bool_operation` `bool_operators` `bool_operation`
                 | ! `bool_operation`
                 | not `bool_operation`
                 | `any_lex`

`value` → <NAME> 
        | <NUMBER> 
        | `function_call`

### Operators:
`arithm_operators` → + | - | * | / | ^   
`assign_esp_operators` → += | -= | *= | /= 
`comp_operators` → == | != | < | > | <= | >= 
`bool_operators` → && | || | and | or

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.