from state import State
from databse.dbsetup import Database
from database.fact import Fact
import random

class Gossip(State):
    @staticmethod
    def respond(context):
        query = '''SELECT * FROM facts'''
        db = Database()
        results = db.query(query)
        
        rand_ndx = random.randint(0, len(results)-1)
        
        gossip = results[rand_ndx]
        
        return gossip
        

State.register(Gossip)
