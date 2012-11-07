from gossip import Gossip
from state import State

class RespondGossip(Gossip):
    @staticmethod
    def recognize(msg):
        tell_me_gossip = ["gossip", "secret"]
        keywords = ["tell", "me", "do", "you", "know"]
        count = 0
        isGossip = False

        #determine if specific query
        isSpecific = False
        subject = None

        #TODO NEED LIST OF USERS
        users = []

        for (ndx, m) in enumerate(msg):
            if m[0] in keywords:
                count+=1
            elif m[0] in tell_me_gossip:
                isGossip = True
            elif m[0] in users:
                isSpecific = True
                subject = m[0]

        confidence = 0.0
        #confidence is high that it's gossip
        if isGossip:
            confidence = 1
        #we're a little less confident it's gossip
        elif count/len(keywords) >= .10:
            confidence = count/len(keywords)
            
        return (confidence, {'specific': isSpecific, 
                             'subject': subject})


State.register(RespondGossip, True)
