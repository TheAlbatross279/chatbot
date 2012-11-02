from bot import Bot
from ircadapter import TestBot
import random

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
