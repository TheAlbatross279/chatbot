from bot import Bot
from ircadapter import TestBot
from state.state import State
import random
import time

class GustafoBot(Bot):
   def __init__(self, channel, nickname, server, port):
      Bot.__init__(self) 

      self.adapter = TestBot(self, channel, nickname, server, port)
      self.adapter.start()

   def send_message(self, nick, msg):
      to_send = nick + ": " + msg

      self.adapter.send_message(to_send)

   def get_users(self):
      #return self.adapter.channels[0][1].users()
      return ["foaad"]     

   def on_message(self, user, timestamp, msg):
      it = time.time()
      res = State.query(user, msg)
      rt = time.time()

      if rt - it < 3.0:
         print "Sleep:", 3.0 - (rt - it)
         time.sleep(3.0 - (rt - it))

      if res is not None:
         self.send_message(user, res)
