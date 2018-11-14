`non_terminal` {
  type = null
  val = null
  error = null
  inh = null
  syn = null
}


push_element(dest, element): adds one olement to a list
push_elements(dest, element_list): adds all the elements from one element_list to the other

assign(id, value)

add_id(id_name, type): add the id_name with its type to the table.
exists(id_name): checks if an id_name alraedy exists.

compare_types(type1, type2): 
  returns 1 if the types are equal, 
  returns -1 if the types have the same base type, ej: float and int have the base type number
  returns 0 if the types are incompatible 

to_type(type, value): converts value to type

evaluate(token_list): evaluate an operation and return its result


check_elements_types(list): check that all the elements of a list have the same type, returns boolean

## Free Context Grammar
1. `program`→ `list_instructions`   

### Variables
2. `def_decl_call` → <TYPE> `def_decl_call_1` {  # Type definition/declaration
                                                `def_decl_call`.type = <TYPE>.lexval
                                                `def_decl_call`.val = `def_decl_call_1`.val
                                                `def_decl_call_1`.inh = <TYPE>.lexval <revisar>
                                              }
3. `def_decl_call` → <NAME> `def_decl_call_2` {# Assignment 
                                                  
}

4. `def_decl_call_1` →  <NAME> `def_decl_call_1_1` {
                                                     if (`def_decl_call_1_1`.val == null):
                                                       add_id(<NAME>.valex, `def_decl_call_1`.type)
                                                       <return>
                                                     if (compare_types(`def_decl_call_1_1`.type, `def_decl_call_1`.inh) == 0):
                                                       <error> "El valor `def_decl_call_1_1`.val no se puede convertir a `def_decl_call_1`.inh"
                                                       <return>
                                                     if (compare_types(`def_decl_call_1_1`.type, `def_decl_call_1`.inh) == -1):
                                                       to_type(`def_decl_call_1`.type, `def_decl_call_1_1`.val)
                                                     add_id(<NAME>.valex, `def_decl_call_1`.type)
                                                     assign(<NAME>.valex, `def_decl_call_1_1`.val)
                                                   }
5. `def_decl_call_1` →  [] <NAME>  `def_decl_call_1_2` {
                                                         if (`def_decl_call_1_2`.val == null):
                                                           add_id(<NAME>.valex, `def_decl_call_1`.type)
                                                           <return>
                                                         if (compare_types(`def_decl_call_1_2`.type, `def_decl_call_1`.inh) == 0):
                                                           <error> "El valor `def_decl_call_1_2`.val no se puede convertir a `def_decl_call_1`.inh"
                                                           <return>
                                                         if (compare_types(`def_decl_call_1_2`.type, `def_decl_call_1`.inh) == -1):
                                                           to_type(`def_decl_call_1`.type, `def_decl_call_1_2`.val)
                                                         add_id(<NAME>.valex, `def_decl_call_1`.type)
                                                         assign(<NAME>.valex, `def_decl_call_1_2`.val)
                                                       }

6. `def_decl_call_1_1` → = `any_lex` {
                                       `def_decl_call_1_1`.val = `any_lex`.val
                                       `def_decl_call_1_1`.type = `any_lex`.type
                                     }
7. `def_decl_call_1_1` → E { 
                             <continue>
                           }

8. `def_decl_call_1_2` → = '{' `list_any_lex` '}' {
                                                    if(check_elements_types(`list_any_lex`.val)):
                                                      `def_decl_call_1_2`.val = `list_any_lex`.val
                                                    else:
                                                      <error> "Los elementos de la lista deben ser del mismo tipo."
                                                  }
9. `def_decl_call_1_2` → E {
                             <continue>
                           }


10. `def_decl_call_2` → = `def_decl_call_2_1` {
                                                `def_decl_call_2`.val = `def_decl_call_2_1`.val
                                                `def_decl_call_2`.type = `def_decl_call_2_1`.type
                                              }
11. `def_decl_call_2` → <ASSIGN_ESP_OPERATORS> `any_lex` {
                                                           
                                                         }
12. `def_decl_call_2` → `func_call_1`

13. `def_decl_call_2_1` → `any_lex`
14. `def_decl_call_2_1` → { `list_any_lex` }


15. `list_var_decl` → <TYPE> <NAME> `list_var_decl_1`

16. `list_var_decl_1` → , `list_var_decl`
17. `list_var_decl_1` → E

### Function:
18. `func_def_decl` → func <NAME> ( `list_var_decl` ) : `func_def_decl_1`

19. `func_def_decl_1` → void { `nfd_list_instructions` }
20. `func_def_decl_1` → <TYPE> `func_def_decl_2`

21. `func_def_decl_2` → { `nfd_list_instructions` return `any_lex` }
22. `func_def_decl_2`  → E

23. `func_call_1` → ( `list_any_lex` )

### Control
24. `control_instructions` → `if` 
25. `control_instructions` → `while`

26. `if` → if (`bool_operation`) { `nfd_list_instructions` } `elif` `if_1`

27. `if_1` → else { `nfd_list_instructions`}
28. `if_1` → E

29. `elif` → elif (`bool_operation`) { `nfd_list_instructions` } `elif_1`
30. `elif` → E

31. `elif_1` → `elif`
32. `elif_1` → E

33. `while` → while (`bool_operation`) {`nfd_list_instructions`}

### Values: 

34. `list_instructions` → `instructions` `list_instructions_1` {
                                                                 # `instructions` es todo el token(no terminal), `list_instructions`.val es una lista
                                                                 push_element(`list_instructions`.val, `instructions`) 
                                                                 push_elements(`list_instructions`.val, `list_instuctions_1`.val)
                                                               }

35. `list_instructions_1` → `list_instructions`  {
                                                   push_elements(`list_instructions_1`.val, `list_instructions`.val)
                                                   # `list_instructions_1`.val = `list_instructions`.val
                                                 }
36. `list_instructions_1` → E {
                                `list_instructions_1`.val = empty_list
                              }

37. `instructions` → `nfd_instructions`
38. `instructions` → `func_def_decl`

39. `nfd_list_instructions` → `nfd_instructions` `nfd_list_instructions_1` {
                                                                             push_element(`nfd_list_instructions`.val, `nfd_instructions`) 
                                                                             push_elements(`nfd_list_instructions`.val, `nfd_list_instructions_1`.val)
                                                                           }

40. `nfd_list_instructions_1` → `nfd_list_instructions` {
                                                          push_elements(`nfd_list_instructions_1`.val, `nfd_list_instructions`.val)
                                                        }
41. `nfd_list_instructions_1` → E {
                                    `nfd_list_instructions_1` = empty_list  
                                  }

42. `nfd_instructions` → `control_instructions`
43. `nfd_instructions` → `def_decl_call`

44. `list_any_lex` → `any_lex` `list_any_lex_1` {
                                                  push_element(`list_any_lex`.val, `any_lex`)
                                                  push_elements(`list_any_lex`.val, `list_any_lex_1`.val)
                                                }
45. `list_any_lex` → E {
                        `list_any_lex`.val = empty_list
                       }

46. `list_any_lex_1` → , `list_any_lex` {
                                          if `list_any_lex`.val == empty_list:
                                            <error> "No se especificó valor luego de ','"
                                          else:
                                            push_elements(`list_any_lex_1`.val, `list_any_lex`.val)
                                            # `list_any_lex_1`.val = `list_any_lex`.val
                                        }
47. `list_any_lex_1`→ E {
                          `list_any_lex`.val = empty_list
                        }

48. `any_lex` → <STRING> {
                           `any_lex`.type = string
                           `any_lex`.val = <STRING>.lexval
                         }
49. `any_lex` → `operation` {
                              `any_lex`.type = `operation`.type
                              `any_lex`.val = `operation`.val  <revisar>
                            }

### Operation
50. `operation` -> `operand` `operation_1`
51. `operation_1` -> <ARITHM_OPERATORS> `operand` `operation_1`
52.               → E
53. `operand` -> `value`
54.           →  - `value`

### Bool_Operation
55. `bool_operation` -> `comp_operation` `bool_operation_1`
56. `bool_operation_1` -> <BOOL_OPERATORS> `comp_operation` `bool_operation_1`
57.                    → E

58. `comp_operation` -> `any_lex` `comp_operation_1`
59.                  →  ! `any_lex`
60.                  → not `any_lex`

61. `comp_operation_1` -> <COMP_OPERATORS> `any_lex`
62.                    → E

### Callable Values
63. `value` → <NAME> `value_1`
64.         → <NUMBER>


65. `value_1` →`func_call_1`
66.           → E

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
