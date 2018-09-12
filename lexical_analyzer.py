from enum import Enum
import re

class Token:
    def __init__(self, token_type, value='', lineN=0):
        self.token_type = token_type
        self.value = value
        self.lineN = lineN

class Matcher:
    # After this you have to check the right side of the declaration.
    pattern_var_def_decl = re.compile(r'(\w+(?:\[\])?)\s+(\w+)(?:\s*=\s*(".*"|\d+|[\D\w][\w]*))?(?:\s*\\.*)?$')
    # TODO: this is not right, the right part of the '=' can be:
    # variable, number, string
    # operation: a + b, x - y, ...
    # When this part is an operation, it can contains blank spaces, otherwise not.
    

    # You have to check the right site of the assignment too.
    paterm_assingment = re.compile(r'(\w+)\s*=\s*([^\s].*)(?:\s*\\.*)?$')

class Tokenizer:
    def def_decl(self, lexeme_tuple, lineN):
        if len(lexeme_tuple) != 3:
            raise ValueError("Define and declaration need 3 lexemes")

        tokens = []
        tokens.append(Token(Token_type.TYPE, lexeme_tuple[0], lineN))
        tokens.append(Token(Token_type.VARIABLE, lexeme_tuple[1], lineN))
        if lexeme_tuple[2]: # definition
            if lexeme_tuple[2][0] == '"': # Is a string
                if lexeme_tuple[2][-1] == '"':
                    tokens.append(Token(Token_type.STRING, lexeme_tuple[2][1:-1], lineN))
                else:
                    tokens.append(Token(Token_type.ERROR, "Incorrect number of quotes"))
            elif lexeme_tuple[2].isdigit(): # Is a number # TODO: replace this with a regex that accepts binary, octal, hexadecimal
                tokens.append(Token(Token_type.NUMBER, lexeme_tuple[2], lineN))
            else: # Is a variable name
                tokens.append(Token(Token_type.NUMBER, lexeme_tuple[2], lineN))
            
    
    def assignment(self, lexeme_tuple):
        pass
        
    statement_types = {
        'DECLARATION': def_decl, # type var
        'DEFINITION': def_decl,  # type var = val
        'ASSIGNMENT': assignment,
    }


    def tokenize(self, lexeme_tuple, statement_type, lineN):
        pass


token_types = [
    # Operators
    'ASSIGN_OPERATOR',
    'ARITHMETIC_OPERATOR',
    'COMPARATION_OPERATOR',
    'BOOLEAN_OPERATOR',
    
    # Reserved words
    'TYPE',
    'CONTROL_STRUCT',
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
    'func',
    'return',
}
reserved_words.update(types)
reserved_words.update(bool_operators_words)

assign_operators = {
    '='
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






# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver si los enteros van a poder ser escritos en hexadecimal, octal y/o binario
# Hexadecimal: 0x[0-9A-F]
# Octal: 0o[0-8]
# Binario: 0b[0-1]
# ver qué pasa si no se retorna nada
