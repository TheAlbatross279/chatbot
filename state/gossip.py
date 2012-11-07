from state import State
from database.dbsetup import Database
from database.fact import Fact
import random

class Gossip(State):
    @staticmethod
    def respond(context):

        subject = None
        #if it's a targeted query, get the subject of the gossip
        if context['specific'] == True:
            subject = context['subject']
        
        query = '''SELECT * FROM facts'''
        db = Database()
        results = db.query(query)
        
        prefix = ["Did you know that ",
                  "I heard that ", 
                  "A little birdy told me that "]
        
        #select prefix
        rand_ndx2 = random.randint(0, len(prefix)-1)        

        gossip = []
        #if it's a speicifc query
        if subject != None:
            specific_results = [result for result in results if subject in result]
            rand_ndx = random.randint(0, len(specific_results)-1)            
            gossip = specific_results[rand_ndx]            
            
        else: #randomly grab facts
            rand_ndx = random.randint(0, len(results)-1)            
            gossip = results[rand_ndx]            

        response = prefix[rand_ndx2] + gossip[2] + " told " +  gossip[0] + ", \"" + gossip[1] + "\"!"

        print gossip
        print response

        return response
        

State.register(Gossip, True)
