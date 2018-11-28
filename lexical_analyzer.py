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

pattern_split = re.compile(r'([^\w.]+)')


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
            if len(item) > 1 and item[1] == 'o' and not pattern_oct.fullmatch(item):
                tokens.append(Token(defs.Token_type.ERROR,
                                    f"Invalid octal number {item}", lineN))
                continue
            if len(item) > 1  and item[1] == 'b' and not pattern_bin.fullmatch(item):
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

table = [
#0                    5					 10 				  15			     20 			     25
[ 0,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1], #r0
[ 1,  2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
[-1,  3,  4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
[ 6,  6, -1, -1,  5, -1, -1,  6, -1, -1, -1, -1, -1,  6,  6,  6, -1, -1,  6, -1, -1, -1, -1, -1, -1, -1, -1,  6], 
[ 8,  8, -1, -1,  7, -1, -1,  8, -1, -1, -1, -1, -1,  8,  8,  8, -1, -1,  8, -1, -1, -1, -1, -1, -1, -1, -1,  8], #r4
[-1, -1, -1, -1,  9, 10, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
[-1, 12, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, 12, -1, -1, -1, -1, 12, -1], 
[14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
[-1, -1, -1, -1, -1, -1, 15, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
[-1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #r9
[19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
[21, 21, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, 20, -1, -1, 21, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, 21], 
[-1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #r14
[27, 27, -1, -1, -1, -1, -1, 27, -1, -1, -1, -1, -1, 27, 27, 27, 26, -1, 27, -1, -1, -1, -1, -1, -1, -1, -1, 27],
[29, 29, -1, -1, -1, -1, -1, 29, -1, -1, -1, -1, -1, 29, 29, 29, 29, 28, 29, -1, -1, -1, -1, -1, -1, -1, -1, 29],
[31, 31, -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, 31, 31, 31, 31, 30, 31, -1, -1, -1, -1, -1, -1, -1, -1, 31],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[33, 33, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1], #r19
[34, 34, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, 35],
[36, 36, -1, -1, -1, -1, -1, 37, -1, -1, -1, -1, -1, -1, -1, 36, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[38, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 39, -1, 38, -1, -1, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1],#{22}{13}:39
[39, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 40, 40, 39, -1, -1, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[42, 42, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1], #r24
[-1, 43, -1, 44, -1, -1, -1, -1, -1, 44, -1, -1, -1, 44, -1, -1, -1, -1, -1, 43, -1, 43, -1, -1, -1, -1, 43, -1], #{25}{13}:44
[-1, -1, -1, 46, -1, -1, 45, -1, -1, 46, -1, -1, -1, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #{26}{13}:47
[-1, 48, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 47, -1, 48, -1, -1, -1, -1, 48, -1],
[-1, 49, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 49, -1, -1, -1, -1, 49, -1],
[51, 51, -1, 51, -1, -1, 51, 51, -1, 51, -1, -1, -1, 51, 51, 51, -1, -1, 51, -1, 50, -1, 51, -1, -1, 51, -1, 51], #r29
[-1, 52, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, 52, -1],
[-1, 54, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 54, -1, 54, -1, 54, 54, -1, 54, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, 56, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1],
[-1, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 57, -1, 57, -1, 58, 59, -1, 57, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, 61, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 61, -1, -1, 60, -1, -1], #r34
[-1, 62, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 63, -1],
[65, 65, -1, 65, -1, -1, 65, 65, 64, 65, -1, -1, -1, 65, 65, 65, -1, -1, 65, -1, 65, -1, 65, -1, -1, 65, -1,  6]
]


terminals = {
'TYPE' : 0,
'NAME' : 1,
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
'ARITHMETIC_OPERATOR': 20,
'-': 21,
'<BOOL_OP>': 22,
'!': 23,
'not': 24,
'COMPARATION_OPERATOR': 25,
'NUMBER': 26,
'$' : 27
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




rules = { #inverted rules and 'ASSIGN_OPERATOR' instead of '='
    1 : ['list_instructions'],
    2 : ['def_decl_call_1' , 'TYPE'],
    3 : ['def_decl_call_2' , 'NAME'],
    4 : ['def_decl_call_1_1' , ],
	5 : ['def_decl_call_1_2' , 'NAME' , 'CLOSE_BRACKET' , 'OPEN_BRACKET'], ##  
    6 : ['any_lex' , 'ASSIGN_OPERATOR'],
    7 : [ ],
	8 : ['CLOSE_BRACKET', 'list_any_lex' , 'OPEN_BRACKET' , 'ASSIGN_OPERATOR'],   ##
	9 : [ ],
	10: ['def_decl_call_2_1' , 'ASSIGN_OPERATOR' ],
    11: ['any_lex' , 'ASSIGN_ESP_OPERATORS'], 
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
	39: ['nfd_list_instructions_1', 'nfd_instructions'],
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
######################Reglas semanticas implementadas##############################
def program() :
    print("program start")

def def_decl_call(temp_line_list,args_size):
    print(args_size,"] input:", temp_line_list[0].token_type.name)
    if temp_line_list[0].token_type.name == "TYPE" :
        def_decl_call_1(temp_line_list,args_size-1)
    else:
        print ("error en la linea", temp_line_list[0].lineN)
        print("No se puede asignar una variable que no existe")
        #implemented_rules(4,temp_line_list,args_size-1)

def def_decl_call_1(temp_line_list, args_size):
    if temp_line_list[1].token_type.name == "NAME" :
        def_decl_call_1_1(temp_line_list,args_size-1)
        #implemented_rules(6,temp_line_list,args_size-1)

def def_decl_call_1_1 (temp_line_list, args_size):
    if len(temp_line_list) > 3:
        add_id(temp_line_list[1].value, temp_line_list[0].value, any_lex(temp_line_list[3]) ) #  no compruebo si existe porque add_id ya lo hace    
    
def any_lex (data):
    if data.token_type.name == "STRING":
        return data.value
    else :
        return 0

def implemented_rules(number_rule,temp_line_list,args_size ):
    if args_size > 0:
        switcher = {
            1: program,
            2: def_decl_call,
            3: print,
            4: def_decl_call_1,
            6: def_decl_call_1_1,
        }
        if (number_rule != 1):
            switcher[number_rule](temp_line_list,args_size)
        else:
            switcher[number_rule]()
    else:
        return
    
######################Reglas semanticas implementadas##############################

def validate (token_list):  #sintactico
    stack=['$','program']
    temp_line =1 #linea donde comienza el código
    temp_line_list =[]
    for i in token_list:
        in_process = True
        a=45
        while in_process and a <55:
            a=a+1
            if i.token_type.name == 'ERROR':
                print (i.token_type.name, "Invalid number of quotes")
                in_process = False
                break
            ##print("s:",stack)
            if i.token_type.name == 'OPEN_BRACKET' or i.token_type.name == 'CLOSE_BRACKET' or i.token_type.name == 'CONTROL_WORD' or i.token_type.name=='BOOLEAN_OPERATOR':
               term = terminals[i.value] 
            else:
                term = terminals[i.token_type.name]
            #print(i.token_type.name, "term:" ,term) 
            non_term = is_non_terminal(stack[-1])
            #print('nonTermIndex', non_term)
            if non_term != -1:
                nonT=non_terminals[stack[-1]]
                #print(stack[-1],"nonT:",nonT+1)
                tmp = table[nonT][term]
                number_rule = tmp+1
                ##print ("rule:",tmp+1,rules[tmp+1]) #tmp+1 because rules start in 1 on the grammar
                if tmp != -1:
                    stack.pop()
                    stack+=rules[tmp+1]
                else:
                    print("ERROR invalid enter in syntax table with input ", i.value  )
                    return False
            else:
                if i.token_type.name == stack[-1]:
                    if i.lineN==temp_line:#seguimos en la linea
                        temp_line_list.append(i)
                    else:                  #cambiamos de linea
                        print("rule: ", number_rule, "temp_line_list: ",temp_line_list)
                        implemented_rules(number_rule,temp_line_list,len(temp_line_list))
                        temp_line=temp_line+1
                        temp_line_list = []
                        temp_line_list.append(i)
                    stack.pop()
                    print("...................term founded", i.token_type.name," Linea: ", i.lineN)
                    
                    in_process = False
    return True

class Non_terminal:
    def __init__(self, nt_type='', val='', inh=''):
        self.nt_type = nt_type
        self.val = val
        self.inh = inh

    def __repr__(self):
        return f"Non_terminal({self.val})"

    def __str__(self):
        return f"Non_terminal: ({self.nt_type}, {self.val}, {self.inh})"

class function_type:
    def __init__(self, return_func, args):
        self.return_func = return_func
        self.args = args

    def __repr__(self):
        return f"Non_terminal({self.args})"

    def __str__(self):
        return f"Non_terminal: ({self.return_func}, {self.args})"

semantic_table = {}

def exists(id_name):
    return id_name in semantic_table
    

def add_id(id_name, type, value):
    if not exists(id_name):
        tail = [type, value]
        semantic_table[id_name] = tail
    else:
        print("Id exists, did not add")


def assign(id_name, value):
    if exists(id_name):
        temp_tail = semantic_table[id_name]
        temp_tail[1] = value
        semantic_table[id_name] = temp_tail
    else:
        print("Id does not exist")    


def type(id_name):
    return semantic_table[id_name][0]


def compare_types(type1, type2):
    if type1 == type2:
        return 1
    elif (type1 == 'int' and type2 == 'float') or (type2 == 'int' and type1 == 'float'):
        return -1
    elif (type1 == 'string' and type2 != type1) or (type2 == 'string' and type2 != type1):
        return 0

def check_elements_types(list_of_id):
    res = list_of_id[0]
    for i in range(1, len(list_of_id)):
        if type(res) == type(list_of_id[i]):
            res = list_of_id[i]
        else:
            return False
    return True

def list_type(list_of_id):
    res = []
    for i in range(len(list_of_id)):
        res.append(type(list_of_id[i]))
    return res


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
        #semantico
    else:
        print("ERROR during syntax analysis")
    
    print(semantic_table)

if __name__ == '__main__':
    main()


# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver que pasa si no se retorna nada
