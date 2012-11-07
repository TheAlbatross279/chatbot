from state import State
from database.dbsetup import Database
from database.fact import Fact
import random

class Gossip(State):
    @staticmethod
    def respond(context):

        subject = None

        if context['isAffirmative'] == True:
           #if it's a targeted query, get the subject of the gossip
           if context['specific'] == True:
               subject = context['subject']
        
           query = '''SELECT * FROM facts'''
           db = Database()
           results = db.query(query)
 #          db.close_conn()

           prefix = ["Did you know that ",
                     "I heard that ", 
                     "A little birdy told me that "]
        
           #select prefix
           rand_ndx2 = random.randint(0, len(prefix)-1)        

           gossip = []

           #if it's a speicifc query
           if subject != None:
               if State.users != None and subject in State.users:
                   db.close_conn()
                   return "Oh, " + subject + " is just so nice... nothing to say about them!"
               else:
                   specific_results = []
                   for result in results:
                       if subject in result:
                           specific_results.append(result)
                       else: 
                           tokens = result[1].split(" ")
                           for token in tokens:
                               if subject.lower() == token.lower():
                                   specific_results.append(result)
                   rand_ndx = random.randint(0, len(specific_results)-1)            
                   gossip = specific_results[rand_ndx]                
           else: #randomly grab facts
               rand_ndx = random.randint(0, len(results)-1)            
               gossip = results[rand_ndx]            

           response = prefix[rand_ndx2] + gossip[2] + " told "  + \
               gossip[0] + ", \"" + gossip[1] + "\"!"

           #print gossip
           #print response

           if len(gossip) == 0:
               db.close_conn()
               return "Hmmm... well, I don't really know anything right now...."
           else:
               knowers = gossip[3] + "; " + context['_nick']
               update_statement = "UPDATE facts SET knowers = \'" + knowers + \
                                  "\' WHERE author= \'" + gossip[0] + \
                                  "\' AND msg= \'" + gossip[1] + \
                                  "\' AND recipient= \'" + gossip[2] + "\';" 
                                  
               db.update(update_statement)
               db.close_conn()
               return response
        else:
            db.close_conn()
            return "Too bad... I had something really juicy!"

State.register(Gossip, True)
