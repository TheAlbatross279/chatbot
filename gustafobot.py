from bot import Bot
from ircadapter import TestBot
from states.outreach import InitialOutreach

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
      return self.adapter.channels[0][1].users()

   def on_join(self):
      self.inactive.start()

   def on_user_join(self):
      return None

   def on_user_exit(self):
      return None

   def on_message(self, nick, msg):
      res = self.states.query(nick, msg)
      if (res) != None:
         self.send_message(nick, res)

   def on_inactive(self):
      res = self.states.forceState(InitialOutreach)
      if (res) != None:
         self.send_message(nick, res)
