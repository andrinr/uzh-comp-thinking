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

def check_word(word, variables, alphabet, grammar):
    print(word)
    l = list(word)
    if len(l) == 1:
        if l[0] in alphabet:
            return False

    for start, ends in grammar.items():
        for end in ends:
            for i in range(len(l)):
                print(l[i], start, end)
                if l[i] == end and start != l[i]:
                    check_word(start + word[1:], variables, alphabet, grammar)
    

variables = {'S', 'A', 'B', 'C'}
alphabet = {'a', 'b'}

grammar = dict()
grammar['S'] = ['AB', 'BC']
grammar['A'] = ['BA', 'a']
grammar['B'] = ['CC', 'b']
grammar['C'] = ['AB', 'a']

word = 'abbaa'

print(check_word(word, variables, alphabet, grammar))