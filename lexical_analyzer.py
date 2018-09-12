from enum import Enum
import re

STATEMENT_DEF_DECL = 'DEF_DECL'
STATEMENT_ASSIGNMENT = 'ASSIGNMENT'
STATEMENT_ERROR = 'ERROR'

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
        return f"Token({self.token_type})"

    def __str__(self):
        return f"Token<{self.token_type}, {self.value}, {self.lineN}>"

class Matcher:
    pattern_comment = re.compile(r'//.*')

    # After this you have to check the right side of the declaration.
    pattern_var_def_decl = re.compile(r'(\w+(?:\[\])?)\s+(\w+)(?:\s*=\s*(\S.*))?(?:\s*//.*)?', re.I)
    # (\S.*) match any_lex
    # (?:\s*//.*)? match comments

    # You have to check the right site of the assignment too.
    pattern_assingment = re.compile(r'([a-z_]\w*)\s*=\s*(\S.*)(?:\s*//.*)?', re.I)

    repattern_number = re.compile(r'(?:0x[0-9a-f]+|0o[0-7]+|0b[01]+)|(?:\d*\.)?\d+', re.I)

    repattern_variale = re.compile(r'[a-z_]\w*', re.I)



    @staticmethod
    def match(line):
        line = line.strip()
        match = Matcher.pattern_comment.fullmatch(line)
        if (match):
            return 
        
        match = Matcher.pattern_var_def_decl.fullmatch(line)
        if (match):
            return (STATEMENT_DEF_DECL, match.groups)
        
        match = Matcher.pattern_assingment.match(line)
        if (match):
            return (STATEMENT_ASSIGNMENT, match.groups)

        return (STATEMENT_ERROR, line)

    @staticmethod
    def rematch(relexeme):
        relexeme = relexeme.strip()

        if relexeme[0] == '"':  # Is a string
            if relexeme[-1] == '"':
                return (RELEX_STR, relexeme[1:-1])
            else:
                return (RELEX_ERROR, "Incorrect number of quotes")

        if Matcher.repattern_number.fullmatch(relexeme): 
            return (RELEX_NUM, relexeme)

        if Matcher.repattern_variale.fullmatch(relexeme): 
            return (RELEX_VAR, relexeme)
        
        # TODO: match other relex...
        ###return (RELEX_ANY_LEX, relexeme)

class Tokenizer:
    @staticmethod
    def def_decl(lexeme_tuple, lineN):
        if len(lexeme_tuple) != 3:
            raise ValueError(f"Define and declaration need 3 lexemes. LINE: {lineN}")

        tokens = []
        tokens.append(Token(Token_type.TYPE, lexeme_tuple[0], lineN))
        tokens.append(Token(Token_type.VARIABLE, lexeme_tuple[1], lineN))
        if lexeme_tuple[2]: # definition
            tokens.append(Token(Token_type.ASSIGN_OPERATOR, '=', lineN))

            any_lex = Matcher.rematch(lexeme_tuple[3])
            tokens.extend(Tokenizer.retokenize(any_lex, lineN))

        return tokens
            
 
    @staticmethod 
    def assignment(lexeme_tuple, lineN):
        if len(lexeme_tuple) != 3:
            raise ValueError(f"Assignment need 2 lexemes. LINE: {lineN}")
        tokens = []
        tokens.append(Token(Token_type.VARIABLE, lexeme_tuple[0], lineN))
        tokens.append(Token(Token_type.ASSIGN_OPERATOR, '=', lineN))

        any_lex = Matcher.rematch(lexeme_tuple[3])
        tokens.extend(Tokenizer.retokenize(any_lex, lineN))

    @staticmethod
    def stmnt_error(line_content, lineN):
        return [Token(Token_type.ERROR, f"Match_Error in <{line_content}>", lineN)]

    statement_types = {
        STATEMENT_DEF_DECL: def_decl, # type var; type var = val
        STATEMENT_ASSIGNMENT: assignment,
        STATEMENT_ERROR: stmnt_error,
    }


    @staticmethod
    def tokenize(lexeme_tuple, statement_type, lineN):
        pass

    @staticmethod 
    def retokenize(any_lex, lineN):
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
