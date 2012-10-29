from state import State
from inquiry import InquiryState

class OutreachState(State):
   @staticmethod
   def recognize(msg):
      greeting_words = ['hi', 'hello', 'hey', 'hola', 'yo']

      for (w, tag) in msg:
         if w.lower() in greeting_words:
            return (1, {})

      return (0, {})

   @staticmethod
   def respond(context):
      return "Hello, " + context['_nick'] + "."

   @staticmethod
   def nextStates():
      return tuple([InquiryState])
