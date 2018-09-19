from enum import Enum

token_types = [
    # Operators
    'ASSIGN_OPERATOR',
    'ARITHMETIC_OPERATOR',
    'COMPARATION_OPERATOR',
    'BOOLEAN_OPERATOR',
    'FUNCTION_OPERATOR'

    # Reserved words
    'TYPE',
    'CONTROL_STRUCT',
    'FUNCTION_DECLARATION',
    'FUNCTION_CALL',
    'RESERVED_WORD',  # Other reserver words

    # Variables and values
    'VARIABLE',
    'NUMBER',
    'STRING',
    'ARRAY_VALS',  # NOTE: Is this needed?

    'BRACKET',  # Any kind of bracket
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

comma_operators = {
    ','
}

reserved_words = [
    types,
    bool_operators_words,
    control_words,
    assign_operators,
    function_operators,
    arithm_operators,
    composite_operators,
    comp_operators,
    bool_operators,
    open_brackets,
    close_brackets,
    comma_operators,
]
