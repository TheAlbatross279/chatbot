"""
Wiki parser
@version lab 3
"""
import nltk
import os
from nltk import pos_tag, word_tokenize
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk.tree import Tree
from state import State

class WikiState(State):
   
   @staticmethod
   def recognize(cmd):
      #split
      #input_text = word_tokenize(cmd) 
      #birthday_keywords = ['born', 'birthdate', 'birthday', 'birth']
      isBirthday = False
      #for word in input_text:
      #   if word in birthday_keywords:
      #      birthday_lookup(postag(input_text));
      #      isBirthday = True
      #      break

      name = None
      if not isBirthday:
         #tagged_words = pos_tag(input_text)
         grammar = "NP: {((?:(?:<DT>)?(?:<NN[P]?[S]?>)+)(?:(?:<DT>|<IN>)*(?:<NN[P]?[S]?>)+)*)}"
         cp = RegexpParser(grammar)
         result = cp.parse(cmd)

         for e in result:
            if isinstance(e, Tree):
               if e.node == 'NP':
                  name = [w[0] for w in e]
     
      if name == None:
         return (0, {})
      
      return (0.9, {'name': name})

   @staticmethod
   def respond(context):
      prefix = "http://en.wikipedia.org/wiki/"

      page = '_'.join(context["name"])

#      page = re.sub("[ ]", "_", page)

      link = prefix + page 

      os.system("wget " + link + " -O wiki.tmp")

      file = open('wiki.tmp')
      input_text = file.read()

      file.close()
      #print input_text

      parsed_text = re.findall(r"<p>(.*?)<\/p>", input_text)

      if len(parsed_text) == 0:
         return "I don't know anything about " + ' '.join(context['name'])

      first_par =  parsed_text[0]

      clean_first = nltk.util.clean_html(first_par)
      clean_fist = re.sub("\(.*?(\(.*?\)).*?\)", "", clean_first)

      pst = nltk.tokenize.punkt.PunktSentenceTokenizer().tokenize(clean_first)
   
      final_string = " ".join(pst[:2])

      os.system("rm wiki.tmp") 

      return final_string

