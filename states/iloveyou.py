from state import State

class InquiryState(State):
    @staticmethod
    def recognize(msg):
        iloveyou = "i love you"
        if msg.lower() == iloveyou

        return ("I love you too")

    @staticmethod
    def respond(context):
        return context + ", " + context['name'] + "!" 
