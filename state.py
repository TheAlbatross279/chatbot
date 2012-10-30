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
      return "You forgot to fill out your respond method."

   @staticmethod
   def nextStates():
      return tuple([State])

class StateCollection:
   def __init__(self, states, workers=cpu_count()):
      self.states = states
      self.p = Pool(processes=workers)
      self.validStates = {}

   def validateState(self, state, validStates):
      for e in validStates:
         if issubclass(state, e):
            return True

      return False

   def forceState(self, state, context={'_nick': ""}):
      self.validStates[context['_nick']] = state.nextStates()

      #self.sendMessage(context['_nick'], state.respond(context))

   def query(self, nick, msg):
      msg = pos_tag(word_tokenize(msg))

      validStates = [w for w in self.states if self.validateState(w, self.validStates.get(nick, self.states))]

      confidence = self.p.map(stateTest, [(msg, state) for state in validStates])

      print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      if conf == 0.0:
         self.validStates = State
         return "I have no idea what is going on"

      self.validStates[nick] = state.nextStates()

      context['_nick'] = nick
      return state.respond(context)
