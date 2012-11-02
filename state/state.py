from multiprocessing import Pool, cpu_count
from nltk import pos_tag, word_tokenize

def stateTest((msg, state)):
   return (state.recognize(msg), state)

class State:
   states = []
   initial_states = []
#   p = Pool(processes=cpu_count())
   validStates = {}

   def __init__(self, isInitial=False):
      State.states.append(self)
      if isInitial:
         State.initial_states.append(self.__class__)

   @staticmethod
   def validateState(state, validStates):
      for e in validStates:
         if issubclass(state.__class__, e):
            return True

      return False

   @staticmethod
   def forceState(state, context={}):
      if context.get('_nick', None) is not None:
         State.validStates[context['_nick']] = state.nextStates()

      return state.respond(context)

   @staticmethod
   def query(nick, msg):
      print msg

      msg_tag = pos_tag(word_tokenize(msg))

      validStates = [w for w in State.states if State.validateState(w, State.validStates.get(nick, State.initial_states))]

      print validStates

      confidence = map(stateTest, [(msg_tag, state) for state in validStates])

      print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      if conf < 0.1:
         if State.validStates[nick] != tuple([State]):
            State.validStates[nick] = tuple([State])
            return State.query(nick, msg)
         else:
            return "I have no idea what's going on"

      State.validStates[nick] = state.nextStates()

      context['_nick'] = nick
      return state.respond(context)

   @staticmethod
   def userJoin(user, timestamp):
      for state in states:
         state.onUserJoin(user, timestamp)

   @staticmethod
   def userLeave(user, timestamp):
      for state in states:
         state.onUserLeave(user, timestamp)

   def recognize(self, msg):
      return (0, {})

   def respond(self, context):
      pass

   def nextStates(self):
      return tuple([State])

   def onUserJoin(self, user, timestamp):
      pass

   def onUserLeave(self, user, timestamp):
      pass
