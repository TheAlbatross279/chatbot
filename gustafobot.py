from bot import Bot
from ircadapter import TestBot
from state.state import State
from state.outreach import InitialOutreach
from threading import Timer
import random
import time

class GustafoBot(Bot):
   CHAT = 0

   def __init__(self, channel, nickname, server, port):
      Bot.__init__(self) 

      self.idle = {}

      self.adapter = TestBot(self, channel, nickname, server, port)
      self.adapter.start()

   def send_message(self, nick, msg):
      to_send = nick + ": " + msg

      self.adapter.send_message(to_send)

   def on_join(self):
      self.idle[GustafoBot.CHAT] = Timer(10.0, self.on_chat_inactive)
      self.idle[GustafoBot.CHAT].start()

   def on_chat_inactive(self):
      users = self.adapter.get_users()

      random.shuffle(users)

      #The following line is not probable with the singleton pattern.
      #States have no reason to be initialized, they should simply register
      # with the main State class using a static method.
      #This will allow multithreading to be added back into the code :)
      #State.forceState(InitialOutreach, {'_nick': users[0]})

   def on_user_inactive(self):
      pass

   def on_message(self, user, timestamp, msg):
      self.idle[GustafoBot.CHAT].cancel()

      it = time.time()
      res = State.query(user, msg)
      rt = time.time()

      if rt - it < 3.0:
         print "Sleep:", 3.0 - (rt - it)
         time.sleep(3.0 - (rt - it))

      if res is not None:
         self.send_message(user, res)
