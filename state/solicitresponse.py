from state import State
import random
from giveupstate import GiveUpState

class SolicitResponse(State):
    def respond(self, context):
        solicitations = ["Hello?",
                         "You should really put an away message up...",
                         "Are you there?",
                         "AYT?",
                         "Hey, " + context['_nick'] + ", you there?" ]

        rand_nsx = random.randint(0, len(solicitations))

        return solicitations[rand_ndx]

    def nextState(self):
        return tuple([GiveUpState])

SolicitResponse()
