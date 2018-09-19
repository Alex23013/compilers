from enum import Enum

token_types = [
    # Operators
    'ASSIGN_OPERATOR',
    'ARITHMETIC_OPERATOR',
    'COMPARATION_OPERATOR',
    'BOOLEAN_OPERATOR',
    'COMPOSITE_OPERATOR',
    'FUNCTION_OPERATOR',
    'COMMA',

    # Reserved words
    'TYPE',
    'CONTROL_WORD',
    'RESERVED_WORD',  # Other reserver words # NOTE: Is this needed?

    # Variables and values
    'NUMBER',
    'STRING',
    'ARRAY_VALS',  # NOTE: Is this needed?
    'NAME', # represents a variable and function name

    'OPEN_BRACKET', 
    'CLOSE_BRACKET',
    'ERROR',
    'COMMENT', # Tokens of this type are removed in the lexical analyzer
]
Token_type = Enum('Token_type', token_types)

types = {
    'string',
    'int',
    'float',
    'void',
}

bool_operators_words = {
    'and',
    'or',
    'not'
}

control_words = {
    'while',
    'if',
    'else',
    'elif',
    'func',
    'return',
}

assign_operators = {
    '='
}

function_operators = {
    ':'
}

arithm_operators = {
    '+',
    '-',
    '*',
    '/',
    '^',  # right associative
}

composite_operators = {
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

comma_symb = {
    ','
}

comment_symb = {
    '//'
}

def check_reserved(item):
    if item in types:
        return Token_type.TYPE
    if item in assign_operators:
        return Token_type.ASSIGN_OPERATOR
    if item in arithm_operators:
        return Token_type.ARITHMETIC_OPERATOR
    if item in comp_operators:
        return Token_type.COMPARATION_OPERATOR
    if item in bool_operators or item in bool_operators_words:
        return Token_type.BOOLEAN_OPERATOR
    if item in function_operators:
        return Token_type.FUNCTION_OPERATOR
    if item in control_words:
        return Token_type.CONTROL_WORD
    if item in composite_operators:
        return Token_type.COMPOSITE_OPERATOR
    if item in open_brackets:
        return Token_type.OPEN_BRACKET
    if item in close_brackets:
        return Token_type.CLOSE_BRACKET
    if item in comma_symb:
        return Token_type.COMMA
    if item in comment_symb:
        return Token_type.COMMENT
    return None