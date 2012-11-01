from bot import Bot
from ircadapter import TestBot
from states.outreach import InitialOutreach
import random

class GustafoBot(Bot):
   def __init__(self, states, channel, nickname, server, port):
      Bot.__init__(self, states) 

      self.adapter = TestBot(self, channel, nickname, server, port)

   def start(self):
      self.adapter.start()

   def send_message(self, nick, msg):
      to_send = nick + ": " + msg

      self.adapter.send_message(to_send)

   def get_users(self):
      #return self.adapter.channels[0][1].users()
      return ["foaad"]      

   def on_join(self):
      self.inactive['_chat'].start()

   def on_message(self, nick, msg):
      self.inactive['_chat'].cancel()
      res = self.states.query(nick, msg)
      if (res) != None:
         self.send_message(nick, res)

   def on_inactive(self):
      users = self.get_users()
      nick = users[random.randint(0, len(users) - 1)]
      res = self.states.forceState(InitialOutreach, {'_nick': nick})
      if (res) != None:
         self.send_message(nick, res)
