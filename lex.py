from enum import Enum
import re
import pprint
import sys  
import os

class Token:
    def __init__(self, token_type, value='', lineN=0):
        self.token_type = token_type
        self.value = value
        self.lineN = lineN

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
    'elif',
    'func',
    'return',
}
reserved_words.update(types)
reserved_words.update(bool_operators_words)

assign_operators = {
    '='
}

funtion_operators = {
    ':'
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

lines = [] #lista de tuplas

def main():  
   filepath = sys.argv[1]

   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

   bag_of_words = {}
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
           line = line[:len(line)-1] + ' ' + line[len(line)-1:] #to separate the \n
           lines.append((line,cnt))           
           #print("line {} : {}".format(cnt, line))
           cnt += 1
           
   for l in lines:
    #print l
    print (l[0].split(" "))
   
if __name__ == '__main__':  
   main()


