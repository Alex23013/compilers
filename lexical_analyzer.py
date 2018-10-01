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
    r'(?:0x[0-9a-f]+|0o[0-7]+|0b[01]+)|(?:\d*\.)?\d+', re.I)
    # TODO: generalizar lo que está dentro de [] y verificar que solo
    # tenga los valores apropiados luego de reconocerlo como "número"
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


if __name__ == '__main__':
    main()


# ver si los strings van a aceptar caracteres de escape:
# ", ', \
# ver que pasa si no se retorna nada
