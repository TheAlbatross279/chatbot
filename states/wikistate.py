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

   #finds birthday keywords and removes them, setting isbirthday to true
   @staticmethod
   def clear_birthday_words(input_text):
      birthday_keywords = ['born', 'birthdate', 'birthday', 'birth']
      candidates = []
      isBirthday = False
      for (w, pos) in input_text:
         if w not in birthday_keywords:
            candidates.append((w, pos))
         elif not isBirthday:
            isBirthday = True

      return (candidates, isBirthday)
   
   @staticmethod
   def parser_results(candidates):
      name = None
      #tagged_words = pos_tag(input_text)
      grammar = "NP: {((?:(?:<DT>)?(?:<NN[P]?[S]?>)+)(?:(?:<DT>|<IN>)*(?:<NN[P]?[S]?>)+)*)}"
      cp = RegexpParser(grammar)
      result = cp.parse(candidates)

      foundNP = False
      for e in result:
         if isinstance(e, Tree):
            if e.node == 'NP':
               name = [w[0] for w in e]
               foundNP = True
     
      return (name, foundNP)

   @staticmethod
   def recognize(cmd):
      #remove birthday keywords
      (candidates, isBirthday) = WikiState.clear_birthday_words(cmd)
      (name, foundNP) = WikiState.parser_results(candidates)
      
      #if can't find noun phrase, try all results again
      if not foundNP:
         (name, foundNP) = WikiState.parser_results(cmd)

      if name == None:
         return (0, {})
      
      return (0.9, {'name': name, 'isBirthday': isBirthday})
      
   @staticmethod
   def respond(context):
      prefix = "\"http://en.wikipedia.org/w/api.php?format=dump&action=query&prop=revisions&rvprop=content&titles="

      page = '_'.join(context["name"])

      print page
#      page = re.sub("[ ]", "_", page)

      link = prefix + page + "\""
      print link

      os.system("wget -O wiki.tmp " + link)

      wiki_file = open('wiki.tmp')
      input_text = wiki_file.read()
#      print input_text

      wiki_file.close()
      #print input_text

      if not context['isBirthday']:
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
      else: #is birthday
         dob = re.findall(r"DATE OF BIRTH *= *([^<]*\|)", input_text)
         os.system("rm wiki.tmp") 
         if len(dob) < 1:
            return "I'm not sure when " + " ".join(context['name']) + " was born..."
         else:
            return " ".join(context['name']) + " was born on " + dob[0]
      
