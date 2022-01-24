# import wora.file
import sys
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import regex as re

nlp = English()
tokenizer = Tokenizer(nlp.vocab)

def parse(cont: str):
    tokens = {}
    # keyword: string
    i = 0
    while i < len(cont):
        x = cont[i]
        if x == '[':
            print(cont[i+1])
        if x == ']':
            print(cont[i])
            # tokens.append(cont[i:]: cont[)
        i += 1


def read_file(fname: str) -> str:
    file = open(fname, 'r')
    res = file.read()
    file.close()
    return res

def get_tokens(fp: str):
    '''Create list of word tokens from file'''
    my_doc = nlp(read_file(fp))

    token_list = []
    for token in my_doc:
        token_list.append(token.text)
    return token_list
tokens: list = get_tokens(sys.argv[1])
print(tokens)
print(parse(tokens))
