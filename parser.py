"""
Wiki parser
@version lab 3
"""
import nltk
from nltk import pos_tag
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *

class parser(object):

    def __init__(self, cmd):
        #split
        input_text = cmd.split(" ")
        birthday_keywords = ['born', 'birthdate', 'birthday', 'birth']
        isBirthday = False
        for word in input_text:
            if word in birthday_keywords:
                birthday_lookup(postag(input_text));
                isBirthday = True
                break

        if not isBirthday:
            tagged_words = pos_tag(input_text)
            grammar = "NP: {((?:(?:<DT>)?(?:<NN[P]?[S]?>)+)(?:(?:<DT>|<IN>)*(?:<NN[P]?[S]?>)+)*)}"
            cp = RegexpParser(grammar)
            result = cp.parse(tagged_words)
            print result

        #POS tagging

        #chunking/custom tagging



    def birthday_lookup(self, input_text):
        pass

    def get_state(self, grammar):
        #state lookup

        return None
