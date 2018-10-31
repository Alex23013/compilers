import reserved_definitions as defs
import re
import sys
import os


class Token:
    def __init__(self, token_type, value='', lineN=0):
        self.token_type = token_type
        self.value = value
        self.lineN = lineN

    def __repr__(self):
        return f"Token({self.token_type.name})"

    def __str__(self):
        return f"Token: ({self.token_type.name}, {self.value}, {self.lineN})"


pattern_comment = re.compile(r'//.*')

patter_number = re.compile(
    r'(?:0x[\da-f]+|0o[\d]+|0b[\d]+)|(?:\d+\.)?\d+', re.I)
pattern_bin = re.compile(r'0b[01]+', re.I)
pattern_oct = re.compile(r'0o[0-7]+', re.I)

pattern_valid_name = re.compile(r'[a-z_]\w*', re.I)

pattern_split = re.compile(r'(\W+)')


def tokenize(str_list, lineN):
    '''
    In: String list, line number
    Out: Token list
    '''
    tokens = []
    inString = False
    strTmp = []
    for idx, item in enumerate(str_list):
        if inString:
            if len(item) != 1 and not item.isalnum():
                for charIdx, char in enumerate(item):
                    str_list.insert(idx + 1 + charIdx, char)
                continue
            if item == '"':
                inString = False
                tokens.append(
                    Token(defs.Token_type.STRING, ''.join(strTmp), lineN))
            else:
                strTmp.append(item)
            continue

        item = item.strip()
        if not item:
            continue
        token_type = defs.check_reserved(item)

        if token_type:
            if token_type == defs.Token_type.COMMENT:
                break
            tokens.append(Token(token_type, item, lineN))
        elif item == '"':
            inString = True
            strTmp = []
        elif patter_number.fullmatch(item):
            if item[1] == 'o' and not pattern_oct.fullmatch(item):
                tokens.append(Token(defs.Token_type.ERROR,
                                    f"Invalid octal number {item}", lineN))
                continue
            if item[1] == 'b' and not pattern_bin.fullmatch(item):
                tokens.append(Token(defs.Token_type.ERROR,
                                    f"Invalid binary number {item}", lineN))
                continue
            tokens.append(Token(defs.Token_type.NUMBER, item, lineN))
        elif pattern_valid_name.fullmatch(item):
            tokens.append(Token(defs.Token_type.NAME, item, lineN))
        elif len(item) != 1:  # Special case: '")', '("', '= "', ...
            for charIdx, char in enumerate(item):
                str_list.insert(idx + 1 + charIdx, char)
        else:
            tokens.append(Token(defs.Token_type.ERROR,
                                f"Invalid character {item}", lineN))

    if inString:
        tokens.append(Token(defs.Token_type.ERROR,
                            "Wrong number of quotes", lineN))
    return tokens

terminals = {
    'TYPE': 0,
    'NAME': 1,
    '[': 2,
    ']': 3,
    'ASSIGN_OPERATOR': 4,
    'ASSIGN_ESP_OPERATORS': 5,
    'COMMA': 6,
    'func': 7,
    '(': 8,
    ')': 9,
    'FUNCTION_OPERATOR': 10,
    'void': 11,
    '{': 12,
    '}': 13,
    'return': 14,
    'if': 15,
    'else': 16,
    'elif': 17,
    'while': 18,
    'STRING': 19,
    'ARITHMETIC_OPERATOR': 20,##ARITHM_OPERATORS
    '-': 21,
    'BOOL_OPERATORS': 22,
    '!': 23,
    'not': 24,
    'COMPARATION_OPERATOR': 25, ##COMP_OPERATORS
    'NUMBER': 26,
    '$': 27,
}
non_terminals = {
    'program': 0,
    'def_decl_call': 1,
    'def_decl_call_1': 2,
    'def_decl_call_1_1': 3,
    'def_decl_call_1_2': 4,
    'def_decl_call_2': 5,
    'def_decl_call_2_1': 6,
    'list_var_decl': 7,
    'list_var_decl_1': 8,
    'func_def_decl': 9,
    'func_def_decl_1': 10,
    'func_def_decl_2': 11,
    'func_call_1': 12,
    'control_instructions': 13,
    'if': 14,
    'if_1': 15,
    'elif': 16,
    'elif_1': 17,
    'while': 18,
    'list_instructions': 19,
    'list_instructions_1': 20,
    'instructions': 21,
    'nfd_list_instructions': 22,
    'nfd_list_instructions_1': 23,
    'nfd_instructions': 24,
    'list_any_lex': 25,
    'list_any_lex_1': 26,
    'any_lex': 27,
    'operation': 28,
    'operation_1': 29,
    'operand': 30,
    'bool_operation': 31,
    'bool_operation_1': 32,
    'comp_operation': 33,
    'comp_operation_1': 34,
    'value': 35,
    'value_1': 36,
}

# ["<TYPE>","<NAME>","[","]","=","<ASSIGN_ESP_OPERATORS>",",","func","(",")",":","void","{","}","return","if","else","elif","while","<STRING>","<ARITHM_OPERATORS>","-","<BOOL_OPERATORS>","!","not","<COMP_OPERATORS>","<NUMBER>","$"],
table = [
[1,1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[2,3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,4,5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[7,7,-1,-1,6,-1,-1,7,-1,-1,-1,-1,-1,7,7,7,-1,-1,7,-1,-1,-1,-1,-1,-1,-1,-1,7],
[9,9,-1,-1,8,-1,-1,9,-1,-1,-1,-1,-1,9,9,9,-1,-1,9,-1,-1,-1,-1,-1,-1,-1,-1,9],
[-1,-1,-1,-1,10,11,-1,-1,12,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,13,14,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,13,-1,13,-1,-1,-1,-1,13,-1],#table{6}{19}:13
[15,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,16,-1,-1,17,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,18,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[20,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,19,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[22,22,-1,-1,-1,-1,-1,22,-1,-1,-1,-1,21,-1,-1,22,-1,-1,22,-1,-1,-1,-1,-1,-1,-1,-1,22],
[-1,-1,-1,-1,-1,-1,-1,-1,23,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,24,-1,-1,25,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,26,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[28,28,-1,-1,-1,-1,-1,28,-1,-1,-1,-1,-1,28,28,28,27,-1,28,-1,-1,-1,-1,-1,-1,-1,-1,28],
[30,30,-1,-1,-1,-1,-1,30,-1,-1,-1,-1,-1,30,30,30,30,29,30,-1,-1,-1,-1,-1,-1,-1,-1,30],
[32,32,-1,-1,-1,-1,-1,32,-1,-1,-1,-1,-1,32,32,32,32,31,32,-1,-1,-1,-1,-1,-1,-1,-1,32],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,33,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[34,34,-1,-1,-1,-1,-1,34,-1,-1,-1,-1,-1,-1,-1,34,-1,-1,34,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[35,35,-1,-1,-1,-1,-1,35,-1,-1,-1,-1,-1,-1,-1,35,-1,-1,35,-1,-1,-1,-1,-1,-1,-1,-1,36],
[37,37,-1,-1,-1,-1,-1,38,-1,-1,-1,-1,-1,-1,-1,37,-1,-1,37,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[39,39,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,39,-1,-1,39,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[40,40,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,41,41,40,-1,-1,40,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[43,43,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,42,-1,-1,42,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,44,-1,45,-1,-1,-1,-1,-1,45,-1,-1,-1,45,-1,-1,-1,-1,-1,44,-1,44,-1,-1,-1,-1,44,-1], #table{25}{13}:45	
[-1,-1,-1,47,-1,-1,46,-1,-1,47,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,49,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,48,48,-1,49,-1,-1,-1,-1,49,-1], #table{27}{19}:48	
[-1,50,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,50,-1,-1,-1,-1,50,-1],
[52,52,-1,52,-1,-1,52,52,-1,52,-1,-1,-1,52,52,52,-1,-1,52,-1,51,-1,52,-1,-1,52,-1,52],
[-1,53,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,54,-1,-1,-1,-1,53,-1],
[-1,55,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,55,-1,55,-1,55,55,-1,55,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,57,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,56,-1,-1,-1,-1,-1],
[-1,58,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,58,-1,58,-1,59,60,-1,58,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,61,-1,-1],
[-1,63,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,64,-1],
[66,66,-1,66,-1,-1,66,66,65,66,-1,-1,-1,66,66,66,-1,-1,66,-1,66,-1,66,-1,-1,66,-1,66]
]



rules = { #inverted rules and 'ASSIGN_OPERATOR' instead of '='
    1 : ['list_instructions'],
    2 : ['def_decl_call_1' , 'TYPE'],
    3 : ['def_decl_call_2' , 'NAME'],
    4 : ['def_decl_call_1_1' , ],
	5 : ['def_decl_call_1_2' , 'NAME' , 'CLOSE_BRACKET' , 'OPEN_BRACKET'], ##  
    6 : ['any_lex' , 'ASSIGN_OPERATOR'],
    7 : [ ],
	8 : ['CLOSE_BRACKET', 'list_any_lex' , 'OPEN_BRACKET' ],   ##
	9 : [ ],
	10: ['def_decl_call_2_1' , 'ASSIGN_OPERATOR' ],
    11: ['any_lex' , 'ASSIGN_ESP_OPERATORS'], ##
	12: ['func_call_1'],
	13: ['any_lex'],
	14: ['CLOSE_BRACKET', 'list_any_lex' , 'OPEN_BRACKET' ], ##
    15: ['list_var_decl_1', 'NAME' , 'TYPE' ],
	16: ['list_var_decl' , 'COMMA'],
	17: [ ],
	18: ['func_def_decl_1' , 'FUNCTION_OPERATOR' , 'CLOSE_BRACKET' , 'list_var_decl' , 'OPEN_BRACKET' , 'NAME' , 'CONTROL_WORD'],
	19: ['CLOSE_BRACKET', 'nfd_list_instructions' , 'OPEN_BRACKET' , 'void' ],
	20: ['func_def_decl_2' , 'TYPE' ],
	21: ['CLOSE_BRACKET', 'list_any_lex' , 'CONTROL_WORD', 'nfd_list_instructions', 'OPEN_BRACKET'  ], ##CONTROL_WORD instead return
	22: [ ],
	23: ['CLOSE_BRACKET', 'list_any_lex' , 'OPEN_BRACKET' ],
	24: ['if' ],
	25: ['while'],
	26: ['if_1' , 'elif' , 'CLOSE_BRACKET' , 'nfd_list_instructions' , 'OPEN_BRACKET' , 'CLOSE_BRACKET' , 'bool_operation' , 'OPEN_BRACKET' , 'CONTROL_WORD'], ##CONTROL_WORD instead return
	27: ['CLOSE_BRACKET' , 'nfd_list_instructions' , 'OPEN_BRACKET' , 'CONTROL_WORD'], 
	28: [ ],
	29: ['elif_1' , 'CLOSE_BRACKET' , 'nfd_list_instructions' , 'OPEN_BRACKET' , 'CLOSE_BRACKET' , 'bool_operation' , 'OPEN_BRACKET', 'CONTROL_WORD' ],##CONTROL_WORD instead elif 
	30: [ ],
	31: ['elif'],
	32: [ ],
	33: ['CLOSE_BRACKET' , 'nfd_list_instructions' , 'OPEN_BRACKET' , 'CLOSE_BRACKET' , 'bool_operation' , 'OPEN_BRACKET' , 'CONTROL_WORD' ], ##CONTROL_WORD instead while
    34: ['list_instructions_1' , 'instructions'],
    35: ['list_instructions'],
    37: ['nfd_instructions'],
	38: ['func_def_decl'],
	39: ['nfd_list_instructions_1' , 'nfd_instructions'],
	40: ['nfd_list_instructions'],
	41: [ ],
	42: ['control_instructions'],
    43: ['def_decl_call'],
	44: ['list_any_lex_1' , 'any_lex' ],
    45: [ ],
	46: ['list_any_lex' , 'COMMA' ],
	47: [ ],
	48: ['STRING'],
    49: ['operation'], 
    50: ['operation_1' , 'operand' ],
    51: ['operation_1' , 'operand' , 'ARITHMETIC_OPERATOR'],
	52: [],
    53: ['value'],
    54: ['value' , 'ARITHMETIC_OPERATOR'],
	55: ['bool_operation_1' , 'comp_operation' ],
	56: ['bool_operation_1' , 'comp_operation' , 'BOOL_OPERATORS'],
	57: [],
	58: ['comp_operation_1' , 'any_lex'],
	59: ['any_lex' , 'BOOLEAN_OPERATOR'],
	60: ['any_lex' , 'BOOLEAN_OPERATOR'],
	61: ['any_lex' , 'COMPARATION_OPERATOR'], ##COMP_OPERATORS
	62: [],
	63: ['value_1' , 'NAME'],
	64: ['NUMBER'],
	65: ['value_1'],
	66: [],
    }

def is_non_terminal(item):
    if item in non_terminals:
        return non_terminals[item]
    else:
        return -1
    
def validate (token_list):
    stack=['$','program']
    for i in token_list:
        in_process = True
        while in_process:
            print("s:",stack)
            if i.token_type.name == 'OPEN_BRACKET' or i.token_type.name == 'CLOSE_BRACKET' or i.token_type.name == 'CONTROL_WORD' or i.token_type.name=='BOOLEAN_OPERATOR':
               term = terminals[i.value] 
            else:
                term = terminals[i.token_type.name]
            print(i.token_type.name, "term:" ,term) 
            non_term = is_non_terminal(stack[-1])
            print('nonTermIndex', non_term)
            if non_term != -1:
                nonT=non_terminals[stack[-1]]
                print(stack[-1],"nonT:",nonT)
                tmp = table[nonT][term]
                print ("rule:",tmp,rules[tmp])
                if tmp != -1:
                    stack.pop()
                    stack+=rules[tmp]
                else:
                    print("ERROR invalid enter")
                    return False
            else:
                if i.token_type.name == stack[-1]:
                    stack.pop()
                    print("...................term founded", i.token_type.name)
                    in_process = False
    return True


def main():
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print(f"File path {filepath} does not exist. Exiting...")
        sys.exit()

    tokens = []
    with open(filepath) as file:
        for lineN, lineVal in enumerate(file):
            res = tokenize(pattern_split.split(lineVal.strip()), lineN + 1)
            print(pattern_split.split(lineVal))
            tokens.extend(res)

    for i in tokens:
        print(i)
    if validate(tokens):
        print("Syntax Done!")
    else:
        print("ERROR during syntax analysis")


if __name__ == '__main__':
    main()


# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver que pasa si no se retorna nada
