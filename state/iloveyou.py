from state import State

class ILoveYouState(State):
    @staticmethod
    def recognize(msg):
        iloveyou = "i love you"
        if msg.lower() == iloveyou

        return (1.0, {'msg':"I love you too"})

    @staticmethod
    def respond(context):
        return context['msg'] + ", " + context['name'] + "!" 

ILoveYouState(True)
