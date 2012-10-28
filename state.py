from multiprocessing import Pool, cpu_count

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
      self.p = Pool(processes=1)

   def query(self, msg):
      confidence = self.p.map(stateTest, [(msg, state) for state in self.states])

      ((_, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      return state.respond(context)
