from state import State
import random
from giveupstate import GiveUpState

class SolicitResponse(State):
    
    @staticmethod
    def respond(context):
        solicitations = ["Hello?",
                         "You should really put an away message up...",
                         "Are you there?",
                         "AYT?",
                         "Hey, " + context['_nick'] + ", you there?" ]

        rand_nsx = random.randint(0, len(solicitations))

        return solicitations[rand_ndx]

    @staticmethod
    def nextState():
        return tuple([GiveUpState])
