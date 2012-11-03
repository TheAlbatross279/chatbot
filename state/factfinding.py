from state import State

class FindGossip(State):

    @staticmethod
    def respond(context):
        f = fact(context['author'], context['msg'], context['recipient'], context['knowers'])
        tuple = f.to_list()

        db = Database()
        db.add_row(context['tuple'])
        db.close()
        
