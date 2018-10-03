## Free Context Grammar
1. `program`→ `list_instructions`   

### Variables
2. `var_decl` → <TYPE> <NAME>
3. `var_def` → <TYPE> <NAME> = `any_lex`
4.           | <NAME> = `any_lex`
5.           | <NAME> <ASSIGN_ESP_OPERATORS> `any_lex`

6. `list_var_decl` → `var_decl`
7.                 | `var_decl`, `list_var_decl`
8.                 | E

### Array:
9. `array_decl_def` → <TYPE> [] <NAME>
10.                 | <TYPE> [] <NAME> = [ `list_any_lex` ]
11.                 | <NAME> = [ `list_any_lex` ]

### Function:
12. `function_def` → func <NAME> ( `list_var_decl` ) : void { `nfd_list_instructions` }
13.                | func <NAME> ( `list_var_decl` ) : <TYPE> { `nfd_list_instructions` return `any_lex` }
14. `function_call` → <NAME> ( `list_any_lex` )
15. `function_decl` → func <NAME> ( `list_var_decl` ) : <TYPE>

### Control
16. `control_instructions` → `if` 
17.                        | `while`

18. `if` → if (`bool_operation`) { `nfd_list_instructions` } `elif`
19.      | if (`bool_operation`) { `nfd_list_instructions` } `elif` else { `nfd_list_instructions`}
20. `elif` → elif (`bool_operation`) { `nfd_list_instructions` }
21.        | elif (`bool_operation`) { `nfd_list_instructions` } `elif`
22.        | E

23. `while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values:
24. `list_instructions` → `instructions`
25.                    | `instructions` `list_instructions`

26. `instructions`→ `control_instructions`
27.               | `var_decl`
28.               | `var_def`
29.               | `function_def`
30.               | `function_decl`
31.               | `function_call`
32.               | `array_decl_def`

33. `nfd_list_instructions` → `nfd_instructions`
34.                         | `nfd_instructions` `nfd_list_instructions`

35. `nfd_instructions`→ `control_instructions`
36.                   | `var_decl`
37.                   | `var_def`
38.                   | `function_call`
39.                   | `array_decl_def`

40. `list_any_lex` → `any_lex`
41.                | `any_lex` , `list_any_lex`
42.                | E

43. `any_lex` → <NAME>
44.           | <NUMBER>
45.           | <STRING>
46.           | `operation`
47.           | `function_call`

48. `operation` → `value` <ARITHM_OPERATORS> `value`
49.             | - `value`

50. `bool_operation` → ! `bool_operation` `bool_operation_P`
51.                  | not `bool_operation` `bool_operation_P`
52.                  | `any_lex` `bool_operation_P`

53. `bool_operation_P` → <COMP_OPERATORS> `bool_operation` `bool_operation_P`
54.                    | <COMP_OPERATORS> `bool_operation` `bool_operation_P`
55.                    | E

56. `value` → <NAME>
57.         | <NUMBER>
58.         | `function_call`

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
