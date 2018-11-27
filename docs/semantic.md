`non_terminal` {
  type = null
  val = null
  error = null
  inh = null
}
in functions the value type is an structure:
`function_type` {
  return = null
  args = null
}


push_element(dest, element): adds one olement to a list
push_elements(dest, element_list): adds all the elements from one element_list to the other


add_id(id_name, type, value): add the id_name with its type and value to the table.
assign(id, value): updates the value of an entry in the table.
exists(id_name): checks if an id_name alraedy exists.
type(id_name): returns the type of the variable id_name.

compare_types(type1, type2): 
  returns 1 if the types are equal, 
  returns -1 if the types have the same base type, ej: float and int have the base type number
  returns 0 if the types are incompatible 

to_type(type, value): converts value to type

evaluate(token_list): evaluate an operation and return its result
evaluateBool(`any_lex`,<COMP_OPERATORS>.lexval,`any_lex`) : returns the boolean value of the comparation 

check_elements_types(list): check that all the elements of a list have the same type, returns boolean
list_type(type): returns a list with the types of the elements in the list

`nfd_list_instructions`.execute() : ejecuta las instrucciones que esten dentro de la lista

control_instructions-nonterminals {
  `if`
  `elif`
  `if_1`
  `elif_1`
  `while`
}        

control_instructions-nonterminals.val{
                            0: no se ejecutó
                            1: se ejecutó
                          }
                  
hasBooleanValue(`any_lex`) : determina si su valor es Booleano  (llamadas a funcion , variables, int, string) o de otro tipo


## Free Context Grammar
1. `program`→ `list_instructions` {
                                  `program`.val = `list_instructions`.val 
                                  }   

### Variables
2. `def_decl_call` → <TYPE> `def_decl_call_1` {  # Type definition/declaration
                                                `def_decl_call`.type = <TYPE>.lexval # NOTE: this two lines are not necessary, because we don't use `def_decl_call` any more
                                                `def_decl_call`.val = `def_decl_call_1`.val
                                                `def_decl_call_1`.inh = <TYPE>.lexval
                                              }
3. `def_decl_call` → <NAME> `def_decl_call_2` {# Assignment  or call
                                                if (!exists(<NAME>.lexval)):
                                                  <error> "No existe una variable/función con el nombre <NAME>.lexval" 
                                                  <return>
                                                if (`def_decl_call_2`.type is not an object of the class Function_type):
                                                  if (compare_types(`def_decl_call_2`.type, type(<NAME>.lexval)) == 0):
                                                    <error> "El valor `def_decl_call_2`.val no se puede convertir a type(<NAME>.lexval)"
                                                    <return>
                                                  if (compare_types(`def_decl_call_2`.type, type(<NAME>.lexval)) == -1):
                                                    to_type(type(<NAME>.lexval), `def_decl_call_2`.val)
                                                  assign(<NAME>.lexval, `def_decl_call_2`.val)
                                                else: # function call
                                                  # The .type of a function is an object of the type Function_type
                                                  if len(type(<NAME>.lexval).args) != len(`def_decl_call_2`.type):
                                                    <error> "La cantidad de parámetros usados no concuerda con la cantidad de parametros requeridos por la función <NAME>.lexval"
                                                  for i in range(len(`def_decl_call_2`.type))
                                                    if (compare_types(`def_decl_call_2`.type[i], type(<NAME>.lexval).args[i]) == 0):
                                                      <error> "Los tipos `def_decl_call_2`.type[i] y type(<NAME>.lexval).args[i] no concuerdan."
                                                      <return>
                                              }

4. `def_decl_call_1` →  <NAME> `def_decl_call_1_1` {
                                                     if(exists(<NAME>.lexval)):
                                                       <error> "Ya existe una variable/función con el nombre <NAME>.lexval" 
                                                     if (`def_decl_call_1_1`.val == null):
                                                       add_id(<NAME>.lexval, `def_decl_call_1`.inh)
                                                       <return>
                                                     if (compare_types(`def_decl_call_1_1`.type, `def_decl_call_1`.inh) == 0):
                                                       <error> "El valor `def_decl_call_1_1`.val no se puede convertir a `def_decl_call_1`.inh"
                                                       <return>
                                                     if (compare_types(`def_decl_call_1_1`.type, `def_decl_call_1`.inh) == -1):
                                                       to_type(`def_decl_call_1`.inh, `def_decl_call_1_1`.val)
                                                     add_id(<NAME>.lexval, `def_decl_call_1`.inh)
                                                     assign(<NAME>.lexval, `def_decl_call_1_1`.val)
                                                   }
5. `def_decl_call_1` →  [] <NAME>  `def_decl_call_1_2` {
                                                         if(exists(<NAME>.lexval)):
                                                           <error> "Ya existe una variable/función ocn el nombre <NAME>.lexval" 
                                                         if (`def_decl_call_1_2`.val == null):
                                                           add_id(<NAME>.lexval, `def_decl_call_1`.inh)
                                                           <return>
                                                         if (compare_types(`def_decl_call_1_2`.type, `def_decl_call_1`.inh) == 0):
                                                           <error> "El valor `def_decl_call_1_2`.val no se puede convertir a `def_decl_call_1`.inh"
                                                           <return>
                                                         if (compare_types(`def_decl_call_1_2`.type, `def_decl_call_1`.inh) == -1):
                                                           to_type(`def_decl_call_1`.inh, `def_decl_call_1_2`.val)
                                                         add_id(<NAME>.lexval, `def_decl_call_1`.inh)
                                                         assign(<NAME>.lexval, `def_decl_call_1_2`.val)
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
                                                      `def_decl_call_1_2`.type = list_type(`list_any_lex`.val)[0] # This must be the type of the first element, because all the elements have the same type
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
                                                          # TODO: send the value of def_decl_call_2, the operator and the right side tokens to evaluate().
                                                          # it requieres that def_decl_call_2 pass it value with .inh
                                                         }
12. `def_decl_call_2` → `func_call_1` {
                                        `def_decl_call_2`.type = `function_call_1`.type
                                      }

13. `def_decl_call_2_1` → `any_lex` {
                                      `def_decl_call_2_1`.val = `any_lex`.val
                                      `def_decl_call_2_1`.type = `any_lex`.type
                                    }
14. `def_decl_call_2_1` → '{' `list_any_lex` '}' {
                                                   if(check_elements_types(`list_any_lex`.val)):
                                                     `def_decl_call_2_1`.val = `list_any_lex`.val
                                                     `def_decl_call_2_1`.type = list_type(`list_any_lex`.val)[0]
                                                   else:
                                                     <error> "Los elementos de la lista deben ser del mismo tipo."
                                                 }

15. `list_var_decl` → <TYPE> <NAME> `list_var_decl_1` {
                                                        push_element(`list_var_decl`.type, <TYPE>.lexval)
                                                        push_elements(`list_var_decl`.type, `list_var_decl_1`.type)
                                                      }

16. `list_var_decl_1` → , `list_var_decl` {
                                            push_elements(`list_var_decl_1`.type, `list_var_decl`.type)
                                          }
17. `list_var_decl_1` → E {
                           `list_var_decl_1`.type = empty_list
                          }

### Function:
18. `func_def_decl` → func <NAME> ( `list_var_decl` ) : `func_def_decl_1` {
                                                                            if(exists(<NAME>.lexval)):
                                                                              <error> "Ya existe una variable/función con el nombre <NAME>.lexval" 
                                                                              <return>
                                                                            add_id(<NAME>.lexval, Function_type(`func_def_decl_1`.type, `list_var_decl`.type))
                                                                          }

19. `func_def_decl_1` → void '{' `nfd_list_instructions` '}' {
                                                               `func_def_decl_1`.type = void
                                                             }
20. `func_def_decl_1` → <TYPE> `func_def_decl_2` {
                                                   `func_def_decl_1`.type = <TYPE>.lexval
                                                   `func_def_decl_2`.inh = <TYPE>.lexval
                                                 }

21. `func_def_decl_2` → '{' `nfd_list_instructions` return `any_lex` '}' {
                                                                           if (`any_lex`.type != `func_def_decl_2`.inh):
                                                                             <error> "El tipo del valor retornado no concuerda con el tipo de retorno declarado"
                                                                             <return>
                                                                         }
22. `func_def_decl_2` → E {
                            <continue>
                          }

23. `func_call_1` → ( `list_any_lex` ) {
                                         `func_call_1`.type = list_type(`list_any_lex`.val)
                                       }

### Control
24. `control_instructions` → `if` {
                                    `control_instructions`.val = `if`.val
                                    <revisar>
                                  }

25. `control_instructions` → `while`{
                                    `control_instructions`.val = `while`.val
                                    <revisar>
                                    }


26. `if` → if (`bool_operation`) { `nfd_list_instructions` } `elif` `if_1`{
                                                                            if(`bool_operation`. val == 1){
                                                                              `nfd_list_instructions`.execute()
                                                                              `if`.val = 1
                                                                            }else{
                                                                              if (`elif`. val != 0 ){
                                                                                `if`.val =  `elif`. val        
                                                                              }else{
                                                                                if (`if_1`. val != 0 ){
                                                                                  `if`.val =  `if_1`. val        
                                                                                }else{
                                                                                  `if`.val = 0
                                                                                }  
                                                                              }
                                                                            }
}

27. `if_1` → else { `nfd_list_instructions`} {
                                             `nfd_list_instructions`.execute()  
                                             `if_1`.val = 1
                                            }
28. `if_1` → E {
              `if_1`.val = 0
               }

29. `elif` → elif (`bool_operation`) { `nfd_list_instructions` } `elif_1` {
                                                                           if (`bool_operation`.val ==1){
                                                                            `nfd_list_instructions`.execute()
                                                                            `elif`.val = 1
                                                                           } else{
                                                                              if(`elif_1` != 0 ){
                                                                                `elif`.val = `elif_1`.val
                                                                              } else{
                                                                                `elif`.val = 0
                                                                              }
                                                                           }
                                                                          }

30. `elif` → E {
              `elif`.val = 0
               }

31. `elif_1` → `elif` {
                        `elif_1`.val = `elif`.val
                      }

32. `elif_1` → E {
              ` elif_1`.val = 0
               }

33. `while` → while (`bool_operation`) {`nfd_list_instructions`} {
                                                                    if (`bool_operation`.val ==1){
                                                                      `nfd_list_instructions`.execute()
                                                                      `while`.val = 1
                                                                    } else{
                                                                      `while`.val = 0
                                                                    }
                                                                  }

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

37. `instructions` → `nfd_instructions` {
                                          `instructions`.val = `nfd_instructions`.val  
                                          `instructions`.type = `nfd_instructions`.type  
                                        }
38. `instructions` → `func_def_decl` {
                                       `instructions`.val = `func_def_decl`.val  
                                       `instructions`.type = `func_def_decl`.type  
                                     }

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

42. `nfd_instructions` → `control_instructions` {
                                                  `nfd_instructions`.val = `constrol_instructions`.val  
                                                  `nfd_instructions`.type = `constrol_instructions`.type  
                                                } 
43. `nfd_instructions` → `def_decl_call` {
                                           `nfd_instructions`.val = `def_decl_call`.val  
                                           `nfd_instructions`.type = `def_decl_call`.type  
                                         }

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
50. `operation` → `operand` `operation_1` {
                                            push_element(`operation`.val, `operand`.val)
                                            push_elements(`operation`.val, `operation_1`.val1)
                                            if (evaluate(`operation`.val) returns an error): #in theory evaluate receives an string, so the list of tokens must be converted to a string.
                                              <error> "No se pudo realizar la operación."
                                              <return>
                                            `operation`.val = evaluate(`operation`.val)

                                          }

51. `operation_1` → <ARITHM_OPERATORS> `operand` `operation_1-1` {
                                                                push_element(`operation_1`.val, <ARITHM_OPERATORS>.lexval)
                                                                push_element(`operation_1`.val, `operand`.val)
                                                                push_elements(`operation_1`.val, `operation_1-1`.val1) # NOTE: `operation1-1` if the same as `operation_1`
                                                               }
52. `operation_1` → E {
                        `operation_1`.val = empty_list
                      }

53. `operand` → `value` {
                          if (compare_types(`value`.type, int) == 0):
                            <error> "No se pueden realizar operaciones aritméticas con valores del tipo `value`.type"
                            <return>
                          `operand`.type = `value`.type
                          `operand`.val = `value`.val
                        }
54. `operand` →  - `value` {
                             if (compare_types(`value`.type, int) == 0):
                               <error> "No se pueden realizar operaciones aritméticas con valores del tipo `value`.type"
                               <return>
                             `operand`.type = `value`.type
                             `operand`.val = - `value`.val
                           }

### Bool_Operation
55. `bool_operation` → `comp_operation` `bool_operation_1`{
                                                            if (`bool_operation_1` == 0){
                                                              `bool_operation`.val = `comp_operation`.val
                                                            }else{
                                                              if (`bool_operation_1`.inh.<BOOL_OPERATORS>.lexval == '&&' ){ #<revisar>
                                                                `bool_operation`.val = `comp_operation`.val and `bool_operation_1`.val 
                                                              }else{
                                                                `bool_operation`.val = `comp_operation`.val or `bool_operation_1`.val
                                                              }                                                            
                                                          }
56. `bool_operation_1` → <BOOL_OPERATORS> `comp_operation` `bool_operation_1`{
                                                                             if (`bool_operation_1` == 0){
                                                                                `bool_operation_1`.val = `comp_operation`.val
                                                                              }else{ 
                                                                                if (extractOp(`bool_operation_1`.inh) == '&&' ){
                                                                                  `bool_operation`.val = `comp_operation`.val and `bool_operation_1`.val 
                                                                                }else{
                                                                                  `bool_operation`.val = `comp_operation`.val or `bool_operation_1`.val
                                                                                }
                                                                              } 
                                                                             }
57.                    → E  {
                              `bool_operation_1` = 0
                            }

58. `comp_operation` → `any_lex` `comp_operation_1` {
                                                      if(`comp_operation_1` == 0 ){
                                                        if (`any_lex`.type == string or `any_lex`.type == int ){ #the same for float
                                                          `comp_operation`.val = 1
                                                        }
                                                        else{ # any_lex is operation or function call
                                                          `comp_operation`.val = `any_lex`.val
                                                        }
                                                      }else{
                                                        `comp_operation`.val = `comp_operation_1`.val
                                                      }
                                                    }

59. `comp_operation` →  ! `any_lex` {
                                      if ( hasBooleanValue(`any_lex`) ){
                                        if(`any_lex`.val == 1){
                                          `comp_operation`.val == 0
                                        }else{
                                          `comp_operation`.val == 1
                                        }
                                      }
                                      else{ # any_lex is operation or function call
                                        <error>"No se puede usar la operacion unaria '!' con any_lex.val"
                                      }
                                    }

60. `comp_operation` → not `any_lex` {
                                      if ( hasBooleanValue(`any_lex`) ){
                                        if(`any_lex`.val == 1){
                                          `comp_operation`.val == 0
                                        }else{
                                          `comp_operation`.val == 1
                                        }
                                      }
                                      else{ # any_lex is operation or function call
                                        <error>"No se puede usar la operacion unaria 'not' con any_lex.val"
                                      }
                                     }

61. `comp_operation_1` -> <COMP_OPERATORS> `any_lex` {
                                                     `comp_operation_1`.val = evaluateBool(`comp_operation`.syn,<COMP_OPERATORS>.lexval, `any_lex`) 
                                                      <revisar>
                                                     }

62. `comp_operation_1` → E {
                            `comp_operation_1`.val = 0
                           }

### Callable Values
63. `value` → <NAME> `value_1` {
                                 if (`value_1`.type != null): # function call
                                   if len(type(<NAME>.lexval).args) != len(`value_1`.type):
                                     <error> "La cantidad de parámetros usados no concuerda con la cantidad de parametros requeridos por la función <NAME>.lexval"
                                   for i in range(len(`value_1`.type))
                                     if (compare_types(`value_1`.type[i], type(<NAME>.lexval).args[i]) == 0):
                                       <error> "Los tipos `value_1`.type[i] y type(<NAME>.lexval).args[i] no concuerdan."
                                       <return>
                                   `value`.type = type(<NAME>.lexval).return
                                 else:
                                   `value`.type = type(<NAME>.lexval)
                               }
64. `value` → <NUMBER> {
                         `value`.type = int # It doesn't matter if <NUMBER> is int or float, both are treated in the same way.
                         `value`.val = <NUMBER>.lexval # Is this value needed?
                       }

65. `value_1` → `func_call_1` {
                                `value_1`.type = `func_call_1`.type
                              }
66. `value_1` → E {
                    <continue>
                  }

## Notes
* Upper case names enclosed with '<>' are tokens.
* Numbers, names and strings are already checked in the lexical analyzer and passed as tokens.
* `nfd_instructions` have all the instructions but no function defitions or function declarations
