## Free Context Grammar
1.  `program` → `list_instructions`   

### Variables
2. `def_decl` → <TYPE> `def_decl_P` 
3. `def_decl_P` → <NAME> `def_decl_P_var`
4.             | [] <NAME> `def_decl_P_arr`
5. `def_decl_P_var` → = `any_lex`
6.                  | E
7. `def_decl_P_arr` → = [ `list_any_lex` ]
8.                  | E

9. `assign` → <NAME> `assign_P` 
10. `assign_P` → = `assign_P1`
11.            | <ASSIGN_ESP_OPERATORS> `any_lex`
12. `assign_P1` → `any_lex`
13.             | [ `list_any_lex` ]

14. `list_var_decl` → <TYPE> <NAME> `list_var_decl_P`
15.                | E
16. `list_var_decl_P` → , `list_var_decl` 
17.                  | E

### Function:
18. `func_def_decl` → func <NAME> ( `list_var_decl` ) : `func_def_decl_P`
19. `func_def_decl_P` → void { `nfd_list_instructions` } 
20.                  | <TYPE> `func_def_decl_P1`
21. `func_def_decl_P1` → { `nfd_list_instructions` return `any_lex` }
22.                    | E

23. `function_call` → <NAME> ( `list_any_lex` )

### Control
24. `control_instructions` → `if` 
25.                       | `while`

26. `if` → if (`bool_operation`) { `nfd_list_instructions` } `elif` `if_P`
27. `if_P` →  else { `nfd_list_instructions`} 
28.       | E
29. `elif` → elif (`bool_operation`) { `nfd_list_instructions` } `elif_P`
30.       | E
31. `elif_P` → `elif`
32.         | E

33. `while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values:
34. `list_instructions` → `instructions` `list_instructions_P`
35. `list_instructions_P` → `list_instructions`
36.                      | E

37. `instructions`→ `control_instructions`
38.              | `def_decl`
39.              | `assign`
40.              | `func_def_decl`
41.              | `function_call`

42. `nfd_list_instructions` → `nfd_instructions` `nfd_list_instructions_P`
43. `nfd_list_instructions_P` → `nfd_list_instructions`
44.                           | E 

45. `nfd_instructions`→ `control_instructions`
46.                  | `def_decl`
47.                  | `assign` 
48.                  | `function_call`

49. `list_any_lex` → `any_lex` `list_any_lex_P`
50.               | E
51. `list_any_lex_P` → , `list_any_lex`
52.                  | E

53. `any_lex` → <NAME>
54.          | <NUMBER>
55.          | <STRING>
56.          | `operation`
57.          | `function_call`

58. `operation` → `value` <ARITHM_OPERATORS> `value`
59.             | - `value`

60. `bool_operation` → ! `bool_operation` `bool_operation_P`
61.                  | not `bool_operation` `bool_operation_P`
62.                 | `any_lex` `bool_operation_P`

63. `bool_operation_P` → <COMP_OPERATORS> `bool_operation` `bool_operation_P`
64.                    | <BOOL_OPERATORS> `bool_operation` `bool_operation_P`
65.                    | E

66. `value` → <NAME>
67.         | <NUMBER>
68.         | `function_call`

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
