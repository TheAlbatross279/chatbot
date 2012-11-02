from state import State
from secondaryoutreach import SecondaryOutreach

class InitiateState(State):
    def respond(self, context):
        return "Hello, " + context['_nick'] + "."

    def nextState(self):
        return tuple([SecondaryOutreach])

InitiateState()
