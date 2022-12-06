"""
Context Free Grammar Parser

set of non terminal symbols (variables)
set of terminal symbols (alphabet),
set of rules 
start symbol

--- 

example: 

start symbol: S
variables: {S}
alphabet: {a, b, _}
rules: S -> aSa | bSb | _

words in language: aabbaa, bb, aabbaabbaa, ...

---

our grammar (upper case letters are variables, lower case letters are terminals):

S -> AB | BC
A -> BA | a
B -> CC | b
C -> AB | a

words in language: 


"""

import numpy as np
import matplotlib.pyplot as plt

def inverse_grammar(grammar):
    inv_grammar = {}
    for start, ends in grammar.items():
        for end in ends:
            if end not in inv_grammar:
                inv_grammar[end] = [start]
            else:
                inv_grammar[end].append(start)
    return inv_grammar
 

def check_word(word, variables, alphabet, inv_grammar, start_symbol='S', max_length=2):

    if word == start_symbol:
        return True

    for i in range(len(word)):
        for j in range(1,min(max_length + 1, len(word)-i + 1)):
           
            #print(word[i:i+j])
            if word[i:i+j] in inv_grammar:
                for end in inv_grammar[word[i:i+j]]:
                    if check_word(
                        word[:i] + end + word[i+j:], 
                        variables, 
                        alphabet, 
                        grammar, 
                        start_symbol, 
                        max_length):
                        return True

    return False
    

variables = {'S', 'A', 'B', 'C'}
alphabet = {'a', 'b'}

grammar = dict()
grammar['S'] = ['AB', 'BC']
grammar['A'] = ['BA', 'a']
grammar['B'] = ['CC', 'b']
grammar['C'] = ['AB', 'a']

word = 'abaa'

print(check_word(word, variables, alphabet, inverse_grammar(grammar)))