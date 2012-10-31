#! /usr/bin/env python
#
# irc chatbot program implementation in Python
# using NLTK built-in chatbots (Eliza,Zen) as example
# modified from original example using ircbot.py by Joel Rosdahl
# must have the python-irclib-0.4.8 installed
# Foaad Khosmood


# usage example: python testbot.py irc.mibbit.net "#mychannel" nickName1 
"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
ircbot.py.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""
#import irc bot
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import time #mainly for the sleep() function

class TestBot(SingleServerIRCBot):
    def __init__(self, linkbot, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

        self.linkbot = linkbot

    def send_message(self, msg):
        self.connection.privmsg(self.channel, msg)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        self.linkbot.on_join()

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments()[0])

    #Determines if this message is directed at us or not
    def on_pubmsg(self, c, e):
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
#        else: (Message is not for us)
        return

#processes commands
    def do_command(self, e, cmd):
        nick = nm_to_n(e.source())
        c = self.connection
#run through all known commands, add more here if needed
        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            c.privmsg(self.channel,"WOW. How rude. PEACE!")
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        else:
#none of the commands match, pass the text to the response function defined above
#but first sleep a little
            time.sleep(3)
            self.linkbot.on_message(nick, cmd)
