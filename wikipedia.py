"""
Gustafo-bot Wikipedia extension
@version lab 3
"""
import os
import re 
import nltk 

class wikipedia(object) :
    
    def __init__(self, plain_text):
        self.plain_text = plain_text

    def get_text(self):
        prefix = "http://en.wikipedia.org/wiki/"

        page = "John Adams"
        
        self.plain_text = re.sub("[ ]", "_", page)

        link = prefix + self.plain_text

        os.system("wget " + link)
        
        file = open(self.plain_text)
        input_text = file.read()

        file.close()
        os.system("rm " + self.plain_text)
        #print input_text

        parsed_text = re.findall(r"<p>(.*?)<\/p>", input_text)
        
        first_par =  parsed_text[0]
    
        clean_first = nltk.util.clean_html(first_par)
        clean_fist = re.sub("\(.*?(\(.*?\)).*?\)", "", clean_first)

        pst = nltk.tokenize.punkt.PunktSentenceTokenizer().tokenize(clean_first)

        final_string = " ".join(pst[:2])

        return final_string

    
    






