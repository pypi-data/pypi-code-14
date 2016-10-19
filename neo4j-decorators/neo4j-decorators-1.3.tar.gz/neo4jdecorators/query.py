from pandas import DataFrame
from neo4jdecorators.db import Neo4j

# decorator to inject transaction into a class method
def Transactional(method):
    def openTransaction(self=None, tx=None):
        # call method with transaction
        transaction = tx or Neo4j.graph().begin()
        result = None

        try:
            result = method(self=self, tx = transaction)
            
            transaction.commit()
        except:
            transaction.rollback()
            raise

        return result

    return openTransaction 

# decorator to run query over a given or injected transaction
def Query(statement, asTable=False):
    def neo4jQuery(method):
        def startTxAndQuery(self, tx=None, parameters=None):
            if tx is None:
                tx = Neo4j.graph()

            result = tx.run(statement, parameters=parameters)

            if asTable:
                result = DataFrame(result.data())

            return method(self, result=result)

        return startTxAndQuery

    return neo4jQuery
