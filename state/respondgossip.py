from gossip import Gossip
from state import State

class RespondGossip(Gossip):
    @staticmethod
    def recognize(msg):
        tell_me_gossip = ["gossip", "secret"]
        keywords = [, "tell", "me", "do", "you", "know"]
        count = 0
        isGossip = False

        #determine if specific query
        isSpecific = False
        subject = None

        #TODO NEED LIST OF USERS
        users = []

        for idx, w in enumerate(msg):
            if w in keywords:
                count+=1
            elif w in tell_me_gossip:
                isGossip = True
            elif w in users:
                isSpecific = True
                subject = w

        #confidence is high that it's gossip
        if isGossip:
            confidence = 1
        #we're a little less confident it's gossip
        elif count/len(keywords) >= .10:
            confidence = count/len(keywords)
            
        
        return (confidence, {'specific': isSpecific, 
                             'subject': subject}


State.register(RespondGossip, True)
