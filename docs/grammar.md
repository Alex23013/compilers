## Free Context Grammar
1. `program`→ `list_instructions`   

### Variables
2. `def_decl_call` → <TYPE> `def_decl_call_1`
3.               | <NAME> `def_decl_call_2`

4. `def_decl_call_1` →  <NAME> `def_decl_call_1_1`
5.                 |  [] <NAME>  `def_decl_call_1_2`

6. `def_decl_call_1_1` → = `any_lex`
7.                   | E

8. `def_decl_call_1_2` → = { `list_any_lex` } # curly brackets instead brackets
9.                   | E


10. `def_decl_call_2` → = `def_decl_call_2_1`
11.                  | <ASSIGN_ESP_OPERATORS> `any_lex`
12.                 | `func_call_1`

13. `def_decl_call_2_1` → `any_lex`
14.                    | [ `list_any_lex` ]


15. `list_var_decl` → <TYPE> <NAME> `list_var_decl_1`

16. `list_var_decl_1` → , `list_var_decl`
17.                  | E

### Function:
18. `func_def_decl` → func <NAME> ( `list_var_decl` ) : `func_def_decl_1`

19. `func_def_decl_1` → void { `nfd_list_instructions` }
20.                  | <TYPE> `func_def_decl_2`

21. `func_def_decl_2` → { `nfd_list_instructions` return `any_lex` }
22.                   | E

23. `func_call_1` → ( `list_any_lex` )

### Control
24. `control_instructions` → `if` 
25.                        | `while`

26. `if` → if (`bool_operation`) { `nfd_list_instructions` } `elif` `if_1`

27. `if_1` → else { `nfd_list_instructions`}
28.       | E

29. `elif` → elif (`bool_operation`) { `nfd_list_instructions` } `elif_1`
30.       | E

31. `elif_1` → `elif`
32.         | E

33. `while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values:
34. `list_instructions` → `instructions` `list_instructions_1`

35. `list_instructions_1` → `list_instructions` 
36.                       | E

37. `instructions`→ `nfd_instructions`
38.               | `func_def_decl`

39. `nfd_list_instructions` → `nfd_instructions` `nfd_list_instructions_1`

40. `nfd_list_instructions_1` → `nfd_list_instructions` 
41.                          | E

42. `nfd_instructions`→ `control_instructions`
43.                   | `def_decl_call`

44. `list_any_lex` → `any_lex` `list_any_lex_1`
45.                | E

46. `list_any_lex_1` → , `list_any_lex`
47.                  | E

48. `any_lex` → <STRING>
49.           | `operation`


### Operation
50. `operation` -> `operand` `operation_1`
51. `operation_1` -> <ARITHM_OPERATORS> `operand` `operation_1`
52.               | E
53. `operand` -> `value`
54.           |  - `value`

### Bool_Operation
55. `bool_operation` -> `comp_operation` `bool_operation_1`
56. `bool_operation_1` -> <BOOL_OPERATORS> `comp_operation` `bool_operation_1`
57.                    | E

58. `comp_operation` -> `any_lex` `comp_operation_1`
59.                  |  ! `any_lex`
60.                  | not `any_lex`

61. `comp_operation_1` -> <COMP_OPERATORS> `any_lex`
62.                    | E

### Callable Values
63. `value` → <NAME> `value_1`
64.         | <NUMBER>


65. `value_1` →`func_call_1`
66.           | E

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
