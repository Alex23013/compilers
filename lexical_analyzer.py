import reserved_definitions as defs
import re


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
    r'(?:0x[0-9a-f]+|0o[0-7]+|0b[01]+)|(?:\d*\.)?\d+', re.I)
pattern_valid_name = re.compile(r'[a-z_]\w*', re.I)


def tokenize(str_list, lineN):
    '''
    In: String list, line number
    Out: Token list
    '''
    tokens = []
    inString = False
    strTmp = []
    for item in str_list:
        if inString:
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
        elif patter_number.fullmatch(item):
            tokens.append(Token(defs.Token_type.NUMBER, item, lineN))
        elif pattern_valid_name.fullmatch(item):
            tokens.append(Token(defs.Token_type.NAME, item, lineN))

    if inString:
        tokens.append(Token(defs.Token_type.ERROR,
                            "Wrong number of quotes", lineN))
    return tokens



# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver que pasa si no se retorna nada
