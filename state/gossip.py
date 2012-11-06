from state import State
from database.dbsetup import Database
from database.fact import Fact
import random

class Gossip(State):
    @staticmethod
    def respond(context):
        query = '''SELECT * FROM facts'''
        db = Database()
        results = db.query(query)
        
        prefix = ["Did you know that ",
                  "I heard that ", 
                  "A little birdy told me that "]
        rand_ndx = random.randint(0, len(results)-1)
        rand_ndx2 = random.randint(0, len(prefix)-1)


        gossip = results[rand_ndx]
        print gossip
        response = prefix[rand_ndx2] + gossip[2] + " told " + gossip[0] + ", \"" + gossip[1] + "\"!"
        return response
        

State.register(Gossip, True)
