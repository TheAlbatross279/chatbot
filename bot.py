from state import StateCollection
from threading import Timer

class Bot(object):
   def __init__(self, states, inactive_time=20.0):
      self.inactive = Timer(inactive_time, self.on_inactive)
      self.states = StateCollection(states)

   def start(self):
      return None

   def send_message(self, msg):
      return None

   def get_users(self):
      return None

   def on_user_join(self):
      return None

   def on_user_exit(self):
      return None

   def on_message(self):
      return None

   def on_inactive(self):
      return None
