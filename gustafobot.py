from bot import Bot
from ircadapter import TestBot
from state.state import State
from state.outreach import InitialOutreach
from state.solicitresponse import SolicitResponse
from state.giveupstate import GiveUpState
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
      users.remove("Gustafo-bot")

      if "foaad" in users:
         user = "foaad"
      else:
         random.shuffle(users)
         user = users[0]

      res = State.forceState(InitialOutreach, {'_nick': users[0]})
      if res is not None:
         self.send_message(users[0], res)

      self.idle[users[0]] = Timer(15.0, self.on_user_inactive, [users[0]])
      self.idle[users[0]].start()

   def on_user_inactive(self, nick):
      if State.userState[nick] is not SolicitResponse:
         res = State.forceState(SolicitResponse, {'_nick': nick})
         self.idle[nick] = Timer(15.0, self.on_user_inactive, [nick])
         self.idle[nick].start()
      else:
         res = State.forceState(GiveUpState, {'_nick': nick})
         del(State.userState[nick])
         if len(State.userState) == 0:
            self.idle[GustafoBot.CHAT] = Timer(10.0, self.on_chat_inactive)
            self.idle[GustafoBot.CHAT].start()
      if res is not None:
         self.send_message(nick, res) 

   def on_message(self, user, timestamp, msg):
      self.idle[GustafoBot.CHAT].cancel()
      if self.idle.get(user, None) is not None:
         self.idle[user].cancel()

      it = time.time()
      res = State.query(user, msg)
      rt = time.time()

      if rt - it < 3.0:
         print "Sleep:", 3.0 - (rt - it)
         time.sleep(3.0 - (rt - it))

      if res is not None:
         self.send_message(user, res)

      print user

      self.idle[user] = Timer(15.0, self.on_user_inactive, [user])
      self.idle[user].start()
