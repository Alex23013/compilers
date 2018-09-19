from enum import Enum
import re
import pprint

STATEMENT_DEF_DECL = 'DEF_DECL'
STATEMENT_ASSIGNMENT = 'ASSIGNMENT'
STATEMENT_ERROR = 'ERROR'
STATEMENT_CONDITION = 'CONDITION'
STATEMENT_ELSE = 'ELSE'
STATEMENT_ELIF = 'ELIF'
STATEMENT_CLOSED_CURLY = 'CLOSED_CURLY'

RELEX_STR = 'STRING'
RELEX_NUM = 'NUMBER'
RELEX_VAR = 'VAR'
RELEX_OPERATION = 'OPERATION'
RELEX_FUNC_CALL = 'FUNC_CALL'
RELEX_FUNC_DECL = 'FUNC_DECL'
RELEX_ANY_LEX = 'ANY_LEX'
RELEX_ERROR = 'ERROR'

class Token:
    def __init__(self, token_type, value='', lineN=0):
        self.token_type = token_type
        self.value = value
        self.lineN = lineN

    def __repr__(self):
        return f"Token({self.token_type.name})"

    def __str__(self):
        return f"Token: ({self.token_type.name}, {self.value}, {self.lineN})"

# class Matcher:
pattern_comment = re.compile(r'//.*')

pattern_var_def_decl = re.compile(r'([a-z_]\w*(?:\[\])?)\s+([a-z_]\w*)(?:\s*=\s*(\S.*))?(?:\s*//.*)?', re.I)
# (\S.*) match any_lex
# (?:\s*//.*)? match comments
# [a-z_]\w* match typename and var name

pattern_assingment = re.compile(r'([a-z_]\w*)\s*=\s*(\S.*)(?:\s*//.*)?', re.I)

pattern_control = re.compile(r'(if|while)\s*\((\S.*)\)\s*{(?:\s*//.*)?')

patter_condition = re.compile(r'(if|while)\s*\((\S.*)\)\s*{(?:\s*//.*)?')
pattern_elif = re.compile(r'(})?elif\s*\((\S.*)\)\s*{(?:\s*//.*)?')
pattern_else = re.compile(r'(})?else\s*{(?:\s*//.*)?')
pattern_closed_curly_bracket = re.compile(r'}\s*(?:\s*//.*)?')


pattern_function_declaration = re.compile(r'func\s*(\D\w+)\s*\((\S.*)\)\s*:\s*(\w+)\s*{$') 

pattern_function_call = re.compile(r'(\D\w*)\s*\((.*)\)$')

repattern_number = re.compile(r'(?:0x[0-9a-f]+|0o[0-7]+|0b[01]+)|(?:\d*\.)?\d+', re.I)

repattern_variale = re.compile(r'[a-z_]\w*', re.I)

repattern_operation = re.compile(r'(\S.*)\s*([^\s\w]{1,2})\s*(\S.*)', re.I) # NOTE: doesn't support word operators like 'and', 'or'

def match(line):
    line = line.strip()
    match = pattern_comment.fullmatch(line)
    if match:
        return 
    
    match = pattern_var_def_decl.fullmatch(line)
    if match:
        return STATEMENT_DEF_DECL, match.groups()
    
    match = pattern_assingment.match(line)
    if match:
        return STATEMENT_ASSIGNMENT, match.groups()

    match = pattern_condition.fullmatch(line)
    if match:
        return STATEMENT_CONDITION, match.groups()

    match = pattern_else.fullmatch(line)
    if match:
        return STATEMENT_ELSE, match.groups()
    
    match = pattern_elif.fullmatch(line)
    if match:
        return STATEMENT_ELIF, match.groups()

    match = pattern_closed_curly_bracket.fullmatch(line)
    if match:
        return STATEMENT_CLOSED_CURLY, match.groups()

    return STATEMENT_ERROR, line

def rematch(any_lex):
    any_lex = any_lex.strip()

    if any_lex[0] == '"':  # Is a string
        if any_lex[-1] == '"':
            return RELEX_STR, any_lex[1:-1]
        else:
            return RELEX_ERROR, "Incorrect number of quotes"

    if repattern_number.fullmatch(any_lex): 
        return RELEX_NUM, any_lex

    if repattern_variale.fullmatch(any_lex): 
        return RELEX_VAR, any_lex

    match = repattern_operation.fullmatch(any_lex)
    if match:
        return RELEX_OPERATION, match.groups()

    # TODO: match other relex... Function call ...
    return RELEX_ERROR, f"Match_Error in <{any_lex}>"
    
    ###return (RELEX_ANY_LEX, any_lex)
# class Matcher/

# class Tokenizer:

def def_decl(lexeme_tuple, lineN):
    if len(lexeme_tuple) != 3:
        raise ValueError(f"Define and declaration needs 3 lexemes. LINE: {lineN}")

    tokens = []
    tokens.append(Token(Token_type.TYPE, lexeme_tuple[0], lineN)) # TODO: check type names
    tokens.append(Token(Token_type.VARIABLE, lexeme_tuple[1], lineN))
    if lexeme_tuple[2]: # definition
        tokens.append(Token(Token_type.ASSIGN_OPERATOR, '=', lineN))

        relex_type, relex_tuple = rematch(lexeme_tuple[2])
        retokens = retokenize(relex_type, relex_tuple, lineN)

        if type(retokens) is list:
            tokens.extend(retokens)
        else:
            tokens.append(retokens)

    return tokens
        
def assignment(lexeme_tuple, lineN):
    if len(lexeme_tuple) != 2:
        raise ValueError(f"Assignment needs 2 lexemes. LINE: {lineN}")
    tokens = []
    tokens.append(Token(Token_type.VARIABLE, lexeme_tuple[0], lineN))
    tokens.append(Token(Token_type.ASSIGN_OPERATOR, '=', lineN))

    relex_type, relex_tuple = rematch(lexeme_tuple[1])
    retokens = retokenize(relex_type, relex_tuple, lineN)

    if type(retokens) is list:
        tokens.extend(retokens)
    else:
        tokens.append(retokens)
    
    return tokens

def control(lexeme_tuple, lineN):
    tokens = []
    if lexeme_tuple[0] == '}': # else |elif
        tokens.append(Token(Token_type.BRACKET, lexeme_tuple[0], lineN))
        tokens.append(Token(Token_type.CONTROL_STRUCT, lexeme_tuple[1], lineN))
    else:
        tokens.append(Token(Token_type.CONTROL_STRUCT, lexeme_tuple[0], lineN))
        tokens.append(Token(Token_type.BRACKET, '(', lineN))        
        #tokens.append(rematch(lexeme_tuple[0], lineN))
        tokens.append(Token(Token_type.BRACKET, ')', lineN))

def func_declaration(lexeme_tuple, lineN):
    tokens = []
    tokens.append(Token(Token_type.FUNCTION_DECLARATION, lexeme_tuple[0], lineN))#func
    tokens.append(Token(Token_type.FUNCTION_CALL, lexeme_tuple[1], lineN))#func name
    tokens.append(Token(Token_type.BRACKET, '(', lineN))
    #tokens.append(rematch(lexeme_tuple[2], lineN))
    tokens.append(Token(Token_type.BRACKET, ')', lineN))
    tokens.append(Token(Token_type.FUNCTION_OPERATOR, ':', lineN)) 
    if len(lexeme_tuple) == 4:
        tokens.append(Token(Token_type.TYPE, lexeme_tuple[3], lineN))
    tokens.append(Token(Token_type.BRACKET, '{', lineN))
    
def func_call(lexeme_tuple, lineN):
    tokens = []
    tokens.append(Token(Token_type.FUNCTION_CALL, lexeme_tuple[0], lineN))#func name
    tokens.append(Token(Token_type.BRACKET, '(', lineN))
    #tokens.append(rematch(lexeme_tuple[1], lineN))
    tokens.append(Token(Token_type.BRACKET, ')', lineN))
    

def stmnt_error(line_content, lineN):
    return Token(Token_type.ERROR, f"Match_Error in <{line_content}>", lineN)

def condition(lexeme_tuple, lineN):
    tokens = []
    tokens.append(Token(Token_type.CONTROL_STRUCT, lexeme_tuple[0], lineN))

    relex_type, relex_tuple = rematch(lexeme_tuple[1])
    retokens = retokenize(relex_type, relex_tuple, lineN)

    if type(retokens) is list:
        tokens.extend(retokens)
    else:
        tokens.append(retokens)
    
    return tokens

def condition_else(lexeme_tuple, lineN):
def condition_elif(lexeme_tuple, lineN):
def closed_curly(lexeme_tuple, lineN):



statement_types = {
    STATEMENT_DEF_DECL: def_decl, # type var; type var = val
    STATEMENT_ASSIGNMENT: assignment,
    STATEMENT_ERROR: stmnt_error,
    STATEMENT_CONDITION: condition,
    STATEMENT_ELSE: condition_else,
    STATEMENT_ELIF: condition_elif,
    STATEMENT_CLOSED_CURLY: closed_curly,
}


patter_condition = re.compile(r'(if|while)\s*\((\S.*)\)\s*{(?:\s*//.*)?')
pattern_elif = re.compile(r'(})?elif\s*\((\S.*)\)\s*{(?:\s*//.*)?')
pattern_else = re.compile(r'(})?else\s*{(?:\s*//.*)?')
pattern_closed_curly_bracket = re.compile(r'}\s*(?:\s*//.*)?')



def operation(relexeme_tuple, lineN):
    if len(relexeme_tuple) != 3:
        raise ValueError(f"Operation needs 3 lexemes. LINE: {lineN}")
    tokens = []
    relex_type, relex_tuple = rematch(relexeme_tuple[0])
    retokens = retokenize(relex_type, relex_tuple, lineN)

    if type(retokens) is list:
        tokens.extend(retokens)
    else:
        tokens.append(retokens)

    tokens.append(Token(Token_type.ARITHMETIC_OPERATOR, relexeme_tuple[1], lineN)) # TODO: check all operand types

    relex_type, relex_tuple = rematch(relexeme_tuple[2])
    retokens = retokenize(relex_type, relex_tuple, lineN)

    if type(retokens) is list:
        tokens.extend(retokens)
    else:
        tokens.append(retokens)

    return tokens


relex_types = {
    RELEX_STR: lambda lexeme, lineN: Token(Token_type.STRING, lexeme, lineN),
    RELEX_NUM: lambda lexeme, lineN: Token(Token_type.NUMBER, lexeme, lineN),
    RELEX_VAR: lambda lexeme, lineN: Token(Token_type.VARIABLE, lexeme, lineN),
    RELEX_ERROR:  lambda lexeme, lineN: Token(Token_type.ERROR, lexeme, lineN),
    RELEX_OPERATION: operation,
    # RELEX_FUNC_CALL:
    # RELEX_FUNC_DECL:
    # RELEX_ANY_LEX:
}


def tokenize(statement_type, lexeme_tuple, lineN):
    return statement_types[statement_type](lexeme_tuple, lineN)

def retokenize(relex_type, relex_tuple, lineN):
    return relex_types[relex_type](relex_tuple, lineN)

# class Tokenizer/

token_types = [
    # Operators
    'ASSIGN_OPERATOR',
    'ARITHMETIC_OPERATOR',
    'COMPARATION_OPERATOR',
    'BOOLEAN_OPERATOR',
    'FUNCTION_OPERATOR',
    
    # Reserved words
    'TYPE',
    'CONTROL_STRUCT',
    'FUNCTION_DECLARATION',
    'FUNCTION_CALL', 
    'RESERVED_WORD', # Other reserver words
    
    # Variables and values
    'VARIABLE',
    'NUMBER',
    'STRING',
    'ARRAY_VALS', # NOTE: Is this needed?
    
    'BRACKET', # Any kind of bracket
    'ERROR',
]
Token_type = Enum('Token_type', token_types)


types = {
    'char',
    'int',
    'float',
    'void',
}

bool_operators_words = {
    'and',
    'or',
    'not'
}

reserved_words = {
    'while',
    'if',
    'else',
    'elif',
    'func',
    'return',
}
reserved_words.update(types)
reserved_words.update(bool_operators_words)

assign_operators = {
    '='
}

funtion_operators = {
    ':'
}

arithm_operators = {
    '+',
    '-',
    '*',
    '/',
    '^', # right associative 
}

double_operators = {
    '++',
    '--',
    '*=',
    '+=',
    '-=',
}

comp_operators = {
    '==',
    '!=',
    '>',
    '<',
    '>=',
    '=>'
}

bool_operators = {
    '||',
    '&&',
    '!'
}
bool_operators.update(bool_operators_words)

open_brackets = {
    '(',
    '[',
    '{'
}

close_brackets = {
    ')',
    ']',
    '}'
}


if __name__ == '__main__':
    example = "char[] str = 1 + var - x * 123"
    statement_type, lexeme_tuple = match(example)
    tokens = tokenize(statement_type, lexeme_tuple, 1)
    for i in tokens:
        print(i)


# 0x0123fa
# 0x12abc
# 0b101010
# 0o071234
# int name = 123
# char name = "1"
# float name_1 = 0.123
# float _23n = 123.023
# int[] var = []

# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver si los enteros van a poder ser escritos en hexadecimal, octal y/o binario
# Hexadecimal: 0x[0-9A-F]
# Octal: 0o[0-8]
# Binario: 0b[0-1]
# ver que pasa si no se retorna nada
