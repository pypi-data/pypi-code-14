from py2neo import Graph

class Neo4j():
    connection = None
    settings = {
        'host': '',
        'username': '',
        'password': ''
    }

    @staticmethod
    def initialize(host, username, password):
        Neo4j.settings['host'] = host
        Neo4j.settings['username'] = username
        Neo4j.settings['password'] = password

    @staticmethod
    def graph(): 
        if Neo4j.connection is None:
            print("Opening Database Connection")
            Neo4j.connection = Graph(
                host=Neo4j.settings['host'], 
                user=Neo4j.settings['username'], 
                password=Neo4j.settings['password']
            )

        return Neo4j.connection