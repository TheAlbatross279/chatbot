from state import *

class Bot(object):
   def __init__(self):
      pass

   def send_message(self, nick, msg):
      pass

   def get_users(self):
      pass

   def on_join(self):
      pass

   def on_user_join(self, user, timestamp):
      res = state.State.userJoin(user, timestamp)

      if res is not None:
         self.send_message(user, res)

   def on_user_exit(self, user, timestamp):
      res = state.State.userExit(user, timestamp)

      if res is not None:
         self.send_message(user, res)

   def on_message(self, user, timestamp, msg):
      res = state.State.query(user, msg)

      if res is not None:
         self.send_message(user, res)
