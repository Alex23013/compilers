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
    'NAME',  # represents a variable and function name

    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'ERROR',
    'COMMENT',  # Tokens of this type are removed in the lexical analyzer
]
Token_type = Enum('Token_type', token_types)

types = [
    'string',
    'int',
    'float',
    'void',
]
bool_operators_words = [
    'and',
    'or',
    'not'
]
control_words = [
    'while',
    'if',
    'else',
    'elif',
    'func',
    'return',
]
assign_operators = [
    '='
]
function_operators = [
    ':'
]
arithm_operators = [
    '+',
    '-',
    '*',
    '/',
    '^',  # right associative
]
composite_operators = [
    '++',
    '--',
    '*=',
    '+=',
    '-=',
]
comp_operators = [
    '==',
    '!=',
    '>',
    '<',
    '>=',
    '=>'
]
bool_operators = [
    '||',
    '&&',
    '!'
]
open_brackets = [
    '(',
    '[',
    '{'
]
close_brackets = [
    ')',
    ']',
    '}'
]
comma_symb = [
    ','
]
comment_symb = [
    '//'
]

all_reserved = {}
all_reserved.update((i, Token_type.TYPE) for i in types)
all_reserved.update((i, Token_type.ASSIGN_OPERATOR) for i in assign_operators)
all_reserved.update((i, Token_type.ARITHMETIC_OPERATOR) for i in arithm_operators)
all_reserved.update((i, Token_type.COMPARATION_OPERATOR) for i in comp_operators)
all_reserved.update((i, Token_type.BOOLEAN_OPERATOR) for i in bool_operators)
all_reserved.update((i, Token_type.BOOLEAN_OPERATOR) for i in bool_operators_words)
all_reserved.update((i, Token_type.FUNCTION_OPERATOR) for i in function_operators)
all_reserved.update((i, Token_type.CONTROL_WORD) for i in control_words)
all_reserved.update((i, Token_type.COMPOSITE_OPERATOR) for i in composite_operators)
all_reserved.update((i, Token_type.OPEN_BRACKET) for i in open_brackets)
all_reserved.update((i, Token_type.CLOSE_BRACKET) for i in close_brackets)
all_reserved.update((i, Token_type.COMMA) for i in comma_symb)
all_reserved.update((i, Token_type.COMMENT) for i in comment_symb)

def check_reserved(item):
    if item in all_reserved:
        return all_reserved[item]
    else:
        return None


