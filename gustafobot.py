from bot import Bot
from ircadapter import TestBot
from state.state import State
from state.outreach import InitialOutreach
from state.solicitresponse import SolicitResponse
from state.giveupstate import GiveUpState
from state.factfinding import FindGossip
from state.solicituser import SolicitUser
from threading import Timer
import random
import time

class GustafoBot(Bot):
   CHAT = 0
   TIMEOUT = 30.0

   def __init__(self, channel, nickname, server, port):
      Bot.__init__(self) 

      self.idle = {}
      self.resumeState = {}

      self.adapter = TestBot(self, channel, nickname, server, port)
      self.adapter.start()

   def forget(self):
      for timer in self.idle.values():
         timer.cancel()

      self.idle = {}
      self.resumeState = {}
      State.forget()

      self.on_join()

   def die(self):
      State.die()
      for timer in self.idle.values():
         timer.cancel()

   def send_message(self, nick, msg):
      to_send = nick + ": " + msg

      self.adapter.send_message(to_send)

   def on_join(self):
      self.idle[GustafoBot.CHAT] = Timer(GustafoBot.TIMEOUT, self.on_chat_inactive)
      self.idle[GustafoBot.CHAT].start()

   def on_chat_inactive(self):
      users = self.adapter.get_users()
      users.remove(self.adapter.nickname)

      if "foaad" in users:
         user = "foaad"
      elif len(users) > 0:
         random.shuffle(users)
         user = users[0]
      else:
         self.idle[GustafoBot.CHAT] = Timer(GustafoBot.TIMEOUT, self.on_chat_inactive)

      res = State.forceState(InitialOutreach, {'_nick': user})
      if res is not None:
         self.send_message(user, res)

      self.idle[user] = Timer(GustafoBot.TIMEOUT, self.on_user_inactive, [user])
      self.idle[user].start()

   def on_user_inactive(self, nick):
      if State.userState[nick] is not SolicitResponse:
         self.resumeState[nick] = State.userState[nick]
         res = State.forceState(SolicitResponse, {'_nick': nick})
         #res = State.forceState(SolicitUser,{'_nick': nick})
         self.idle[nick] = Timer(GustafoBot.TIMEOUT, self.on_user_inactive, [nick])
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
         if State.userState[user] is SolicitResponse:
            State.userState[user] = self.resumeState[user]

      it = time.time()
      res = State.query(user, msg)
      rt = time.time()

      if rt - it < 3.0:
         print "Sleep:", 3.0 - (rt - it)
         time.sleep(3.0 - (rt - it))

      if res is not None:
         self.send_message(user, res)

      print user

      self.idle[user] = Timer(GustafoBot.TIMEOUT, self.on_user_inactive, [user])
      self.idle[user].start()

   def on_chat(self, t, f, msg):
      knowers = self.adapter.get_users()
<<<<<<< HEAD
=======
      #knowers.remove("Gustafo-bot")
>>>>>>> 08306e541d046fdf3cf143aad1513211f9836d86
      knowers.remove(self.adapter.nickname)
      context = {'author': f,
                 'recipient': t,
                 'msg': msg,
                 'knowers': knowers}

      State.forceState(FindGossip, context)
