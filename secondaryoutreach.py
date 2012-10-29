from state import State
import random

class SecondaryOutreach(State):
    @staticmethod
    def recognize(msg):
        pass
    @staticmethod
    def respond(context):
        
        #randomly choose how are your/
        inquiries = [ "How are you?", 
                      "How's it going?",
                      "How are things?",
                      "How's it hanging?",
                      "What are you up to?", 
                      "What's up?",
                      "Sup?",
                      "What's crackin?" ]

        rand_ndx = random.rand(0, len(inquiries))

        return inquiries[rand_ndx]


 print respond("any random nonsense will do")
