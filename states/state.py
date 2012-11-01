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
      pass

   @staticmethod
   def nextStates():
      return tuple([State])

class StateCollection:
   def __init__(self, workers=cpu_count()):
      self.states = []
      self.initial_states = []
      self.p = Pool(processes=workers)
      self.validStates = {}

   def validateState(self, state, validStates):
      for e in validStates:
         if issubclass(state, e):
            return True

      return False

   def forceState(self, state, context={}):
      if context.get('_nick', None) is not None:
         self.validStates[context['_nick']] = state.nextStates()

      return state.respond(context)

   def query(self, nick, msg):
      print msg
      msg_tag = pos_tag(word_tokenize(msg))

      validStates = [w for w in self.states if self.validateState(w, self.validStates.get(nick, self.initial_states))]

      confidence = self.p.map(stateTest, [(msg_tag, state) for state in validStates])

      print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      if conf < 0.1:
         if self.validStates[nick] != tuple([State]):
            self.validStates[nick] = tuple([State])
            return self.query(nick, msg)
         else:
            return "I have no idea what's going on"

      self.validStates[nick] = state.nextStates()

      context['_nick'] = nick
      return state.respond(context)
