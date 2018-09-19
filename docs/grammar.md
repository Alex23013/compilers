## Free Context Grammar
`<program>`→ `<list_instructions>`  
`<type>` → int | float | void | string

### Variables
`<var_declaration>` → `<var>` | `<var>` = `<any_lex>`  
`<var>` → `<type>` `<name>` | `<name>`  


### Array:
`<array_declaration>` → `<type>` [] `<name>`  
       | `<type>` [ `<number>` ] `<name>`  
       | `<type>` [] `<name>` `<assign_operators>` { `<list_any_lex>` }   

### Function:
`<function_definition>` → `<type>`  `<name>` ( `<list_any_lex>` ) : `<type>` { `<list_instructions>` return `<list_any_lex>` }  
`<function_call>` → `<name>` ( `<list_any_lex>` )  
`<function_decl>` → `<name>` ( `<list_any_lex>` )  

### Control
`<control_instructions>` → `<if>` | `<elif>` | `<else>` 
`<if>` → if (`<id>` `<comp_operators>` `<id>`){`<list_instructions>`}  
`<elif>` → elif (`<id>` `<comp_operators>` `<id>`){`<list_instructions>`}  
`<else>` → else{ `<list_instructions>` }  

### Values:
`<list_instructions>` → `<instructions>` | `<instructions>``<instructions>` | E  
`<instructions>`→ `<control_instructions>` | `<var_declaration>` | `<function_definition>` | `<array_declaration>`
`<list_any_lex>` → `<any_lex>` | `<list_any_lex>` , `<list_any_lex>` | E  
`<any_lex>` → `<var>` | `<number>` | `<string>` | `<operation>` | `<function_call>` 
`<operation>` → `<id>` `<arithm_operators>` `<id>` | `<var>` `<double_operators>` 

`<id>` → `<var>` | `<number>`   
`<name>` → (`<letter>` | `<name_symbols>`) | (`<letter>` | `<name_symbols>`)(`<word>` | `<number>` | `<name_symbols>`)  
`<string>` → (`<word>` | `<number>` | `<name_symbols>`)
`<word>` → `<letter>` | `<letter><letter>`  
`<number>` → `<digit>` | `<digit><digit>`   

### Operators:
`<arithm_operators>` → + | - | * | / | ^  
`<double_operators>` → ++ | -- | *= | +=  
`<comp_operators>` → == | != | < | > | <= | >=  | `<bool_operators>` | `<bool_operators_words>`
`<bool_operators>` → && | || | !  
`<bool_operators_words>` → and | or | not  

### Terminals:
`<name_symbols>` →  _   
`<letter>` → a | b | ... | z | A | B | ... | Z  
`<digit>` → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9   

