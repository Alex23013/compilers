from enum import Enum

class Token_type(Enum):
    # Operators
    ASSIGN_OPERATOR = 'assign_operator'
    ARITHMETIC_OPERATOR = 'arithmetic_operator'
    COMPARATION_OPERATOR = 'comparation_operator'
    BOOLEAN_OPERATOR = 'boolean_operator'
    
    # Reserved words
    TYPE = 'type'
    CONTROL_STRUCT = 'reserver_word'
    RESERVER_WORD = 'reserver_word'
    
    # Variables and values
    VARIABLE = 'variable'
    NUMBER = 'number'
    STRING = 'string' # chars are strings with just one character
    
    BRACKET = 'bracket'
    ERROR = 'error'

class Tokens(Enum):
    # Types
    CHAR = 'char'
    INT = 'int'
    FLOAT = 'float'
    ARRAY = 'array' # ??
    
    # Reserved words
    WHILE = 'while'
    IF = 'if'
    # THEN = 'then'
    ELSE = 'else'
    FUNC = 'func'
    RETURN = 'return'
    
# TODO: split this reserver words.
reserved_words = {
    'char',
    'int',
    'float',
    'void',
    'while',
    'if',
    'else',
    'func',
    'return',
}

assign_operators = {
    '='
}

arithm_operators = {
    '+',
    '-',
    '*',
    '/',
    '^', # asociativo hacia la derecha
}

comp_operators = {
    '==',
    '!=',
    '>',
    '<',
    '>=',
    '=>'
}
 

# TODO: split this, and include the words in the reserved words set.
bool_operators = {
    'or',
    'and',
    'not',
    '||',
    '&&',
    '!'
 }



# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver si los enteros van a poder ser escritos en hexadecimal, octal y/o binario
# Hexadecimal: 0x[0-9A-F]
# Octal: 0o[0-8]
# Binario: 0b[0-1]
# ver qué pasa si no se retorna nada