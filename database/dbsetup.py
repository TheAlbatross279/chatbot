import sqlite3 

class Database(object):
    def __init__(self):
        self.connection = sqlite3.connect('gossip.db')
        self.c = self.connection.cursor()

    def add_row(self, values):
        prefix = "INSERT INTO facts VALUES (" 
        suffix = ")"
        #build query
        query = prefix + "'"+ '\', \''.join(values) +"'"+ suffix
        self.c.execute(query)
        #(commit) the changes
        self.connection.commit()

    def close_conn(self):
        self.connection.close()
     
    def query(self, query):
        self.c.execute(query)
        results = []
        for row in self.c:
            results.append(row)

        return results
    def drop_tables(self):
        self.c.execute("DROP TABLE facts")
        self.c.execute('''CREATE TABLE facts
             (author text, msg text, recipient text, knowers text)''')

