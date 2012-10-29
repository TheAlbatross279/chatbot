from multiprocessing import Pool, cpu_count
from nltk import pos_tag, word_tokenize

def stateTest((msg, state)):
   return (state.recognize(msg), state)

class State:
   @staticmethod
   def recognize(msg):
      return (0, {})

   @staticmethod
   def respond(context):
      return None

class StateCollection:
   def __init__(self, states, workers=cpu_count()):
      self.states = states
      self.p = Pool(processes=workers)

   def query(self, nick, msg):
      msg = pos_tag(word_tokenize(msg))
      confidence = self.p.map(stateTest, [(msg, state) for state in self.states])

      print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      if conf == 0.0:
         return "I have no idea what is going on"

      context['_nick'] = nick
      return state.respond(context)
