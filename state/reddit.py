from state import State

class RedditState(State):
   def recognize(self, msg):
      phrase = ("when", "does", "the", "narwhal", "bacon")

      if len(msg) < len(phrase):
         return (0.0, {})

      for idx, w in enumerate(phrase):
         if msg[idx][0].lower() != w:
            return (0.0, {})

      return (1.0, {})

   def respond(self, context):
      return "Midnight."

RedditState(True)
