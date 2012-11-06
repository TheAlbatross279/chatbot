from gossip import Gossip

class RespondGossip(Gossip):
    @staticmethod
    def recognize(msg):
        tell_me_gossip = ["gossip"]

        for idx, w in enumerate(tell_me_gossip):
            if msg[idx][0].lower() == w:
                return (1.0, {})

        return (0.0, {})


State.register(RespondGossip)
