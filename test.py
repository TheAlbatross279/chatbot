from state import State, StateCollection
from parser import WikiState

bot = StateCollection([WikiState])

print bot.query("Tell me about John Adams")
