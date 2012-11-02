from state import State
from inquiry import InquiryState
from secondaryoutreach import SecondaryOutreach

class OutreachState(State):
   def recognize(self, msg):
      greeting_words = ['hi', 'hello', 'hey', 'hola', 'yo']

      for (w, tag) in msg:
         if w.lower() in greeting_words:
            return (1, {})

      return (0, {})

   def respond(self, context):
      return "Hello, " + context['_nick'] + "."

class InitialOutreach(OutreachState):
   def nextStates(self):
      return tuple([SecondaryOutreach])

InitialOutreach()

class OutreachResponse(OutreachState):
   def nextStates(self):
      return tuple([InquiryState])

OutreachResponse(True)
