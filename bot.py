from state import StateCollection
from threading import Timer

class Bot(object):
   def __init__(self, states, inactive_time=20.0):
      self.inactive = {}
      self.inactive['_chat'] = Timer(inactive_time, self.on_inactive)
      self.states = StateCollection(states)

      self.handlers = {'ON_USER_INACTIVE' :[],
                       'ON_INACTIVE'      :[],
                       'ON_MESSAGE'       :[],
                       'ON_USER_EXIT'     :[],
                       'ON_USER_JOIN'     :[]}
                       
      self.context = {}

   def start(self):
      self.inactive['_chat'].cancel()
      self.inactive['_chat'] = Timer(inactive_time, self.on_inactive)

   def send_message(self, msg):
      return None

   def get_users(self):
      return None

   def register_sm(self, sm):
      sm.build(self)

   def register_handler(self, event, fun, args):
      if self.handlers.get(event, None) is not None:
         self.handlers[event] += fun
         return True
      else:
         return False

   def on_user_join(self, user, timestamp):
      for fun in self.handlers['ON_USER_JOIN']:
         fun(user, timestamp)

   def on_user_exit(self, user, timestamp):
      for fun in self.handlers['ON_USER_EXIT']:
         fun(user, timestamp)

   def on_message(self, user, timestamp, msg):
      if self.inactive.get(user, None) is not None:
         self.inactive[user].cancel()
      self.inactive[user] = Timer(inactive_time, self.on_user_inactive, user)

      for fun in self.handlers['ON_MESSAGE']:
         fun(user, timestamp, msg)

   def on_inactive(self):
      for fun in self.handlers['ON_INACTIVE']:
         fun()

   def on_user_inactive(self, user):
      for fun in self.handlers['ON_USER_INACTIVE']:
         fun(user)
