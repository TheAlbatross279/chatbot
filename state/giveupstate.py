from state import State
import random

class GiveUpState(State):
    def respond(self, context):
        frustrated_responses = ["Well, fine. Be that way", 
                                "Well... I'll catch you later then!",
                                "G2G! TTYL!"]

        rand_nsx = random.randint(0, len(frustrated_responses))
        
        return inquiries[rand_ndx]

GiveUpState()
