"""
Wiki parser
@version lab 3
"""
import nltk
import os
import calendar
from nltk import pos_tag, word_tokenize
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk.tree import Tree
from state import State
from HTMLParser import HTMLParser
from datetime import datetime

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
      grammar = "NP: {((?:(?:<NN[P]?[S]?>)+)(?:(?:<DT>|<IN>)*(?:<NN[P]?[S]?>)+)*)}"
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
      #prefix = "\"http://en.wikipedia.org/w/api.php?format=dump&action=query&prop=revisions&rvprop=content&titles="
      prefix = "\"http://en.wikipedia.org/wiki/"

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
         #clean_wiki = re.compile("^\|[^\n]*|^:[^\n]*|^;[^\n]*|^\*[^\n]*|<ref[^>]*>[^<]*</ref>|</?ref[^/>]*/?>|\[\[File:[^\]]*\]]|\[\[[^\|\]]*\||\[\[|\]\]|<[^/>]*/>|<!--[^-]*-->|{{[^}\n]*}};?|}}|{{[^\n]*|'''|&nbsp;|</?nowiki>", re.M)
         #input_text = re.sub(clean_wiki, "", input_text)
         #input_text = re.sub(r'(?:.|\n)*\["\*"\]=>\n\W*string\(\d+\)\W*"', "", input_text, 1)
         #print input_text[:5000]
         #input_text = input_text.split('\n')
         #input_text = [line for line in input_text if len(line) > 250]
         input_text = re.findall(r"<p>(.*?)<\/p>", input_text)
         if len(input_text) == 0:
            return "I don't know anything about " + " ".join(context['name'])
         input_text = nltk.util.clean_html(input_text[0])
         input_text = re.sub(r'\[(?:\s*\d+\s*|\s*[cC]itation [nN]eeded\s*)\]', "", input_text)
         input_text = re.sub(r' +', " ", input_text)
         input_text = re.sub(r' (-|,|\.|\))', r"\g<1>", input_text)
         input_text = re.sub(r'(-|\() ', r"\g<1>", input_text)
         input_text = re.sub(r'&\S+;', "", input_text)

         pst = nltk.tokenize.punkt.PunktSentenceTokenizer().tokenize(input_text)
         
         length = 0
         final_string = ""
         for sent in pst:
            print sent
            length += len(sent)
            if length < 512:
               final_string += " " + sent

         os.system("rm wiki.tmp") 

         return final_string
      else: #is birthday
         dob = re.findall(r'<span class="bday">([\d-]+)</span>', input_text)
         os.system("rm wiki.tmp") 
         if len(dob) < 1:
            return "I'm not sure when " + " ".join(context['name']) + " was born..."
         else:
            date = datetime.strptime(dob[0], "%Y-%m-%d")
            dob = calendar.month_name[date.month] + " " + str(date.day) + ", " + str(date.year)

            return " ".join(context['name']) + " was born on " + dob
      
