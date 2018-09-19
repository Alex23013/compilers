# any_lex
Lexeme that needs reevaluation.

All lexemes that are located in a place where can contain operations (e.g. in the left of an assignment operator, 
a parameter in a function call, condition in control structure) are considered an `any_lex`.

Examples:

* `int name = <any_lex>`
* `func_call(<any_lex>, <any_lex>)`
* `var = <any_lex> + <any_lex>`

### Any lex types

An `any_lex` needs to be reevaluated (matcher and tokenizer), after evaluation it can be one of this types:

* **Variable:** a name of a variable.
* **Number:** a number: 123, 0x123e, 0b0101, ...
* **String:** a string.
* **Operation:** needs to be **reevaluated**.
* **Function call:** needs to be **reevaluated**.
* ...

### Evaluation algorithm

Already we have two methods that are used in the lexical analyzer: `match` and `tokenize`.
Another two methods need to be implemented `rematch` and `retokenize`.

* *Mini*regular expresions will going to be used in rematch.

In `tokenize`:

```python
def tokenize(...):
  ...
  relexemes = rematch(<any_lex>, ...)
  retokenize(relexemes, ...)
  ...

def rematch(any_lex, ...)
  if any_lex is STRING:
    return (STRING, any_lex) # (statement_type, lexeme)
  elif any_lex is NUMBER:
    return (NUMBER, any_lex) # (statement_type, lexeme)
  elif any_lex is VARIABLE:
    return (VARIABLE, any_lex) # (statement_type, lexeme)
  else:
    ... other regex to match any_lex ...
    return (STATEMENT_TYPE, <lexem tuple>)

def retokenize(relexemes, ...):
  ...
  if (relexemes[0] == 'ANY_LEX'): # Actually this is a call of the dictionary of (Statement_types : function)
    1. rematch
    2. tokenize
    3. return tokens
  ...

  
```

### Example

`int x = func("str", var) * 33`

1. First match  
   `DEFINITION: <int> <x> <func("str", var) * 33>`

2. Tokenize  
  `(TYPE, int) (VAR, int) (ASSIGNMENT, '=') <func("str", var) * 33>`   
  The last part needs to be rematched

3. Rematch  
   In :  `func("str", var) * 33`  
   Out `OPERATION: <func("str", var)> <*> <33>`

4. Retokenize  
   `<func("str", var)> (OPERATOR, '*') (NUMBER, 33)`    
   the first part needs to be rematched

5. Rematch  
   In :  `func("str", var)`  
   Out `FUNCTION_CALL: <func> <"str"> <var>`  

6. Rematch  
  `(FUNCTION_CALL, func) (BRACKET, '(') (STRING, str) (VAR, var) (BRACKET, ')') `
