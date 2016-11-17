__author__ = "Kiran Vemuri"
__email__ = "kkvemuri@uh.edu"
__status__ = "Development"
__maintainer__ = "Kiran Vemuri"

from cassandra.cluster import Cluster
from cassandra.query import dict_factory


class Cassandra:
    """
    Class to facilitate requests to the cassandra cluster
    """
    def __init__(self, seed_nodes):
        """
        :param seed_nodes(list(strings)): list of IP addresses of the seed nodes
        """
        self.seed_nodes = seed_nodes

    def new_session(self, keyspace=None):
        """
        Establishes a session to the cassandra cluster and Returns session object
        :param keyspace: <str> name of the keyspace you want to connect to
        :return session object
        """
        cluster = Cluster(self.seed_nodes)
        session = cluster.connect(keyspace)
        return session

    def fetch_keyspaces(self):
        """
        Returns a list of keyspaces
        :return list of keyspace names
        """
        keyspace_query = self.new_session().execute("select keyspace_name from system.schema_keyspaces")
        keyspace_list = [row.keyspace_name for row in keyspace_query]
        return keyspace_list

    def run_query(self, in_query, keyspace=None):
        """
        :param in_query: <str> query to be executed on the cluster
        :param keyspace: <str> name of the keyspace to run the query on
        :return a list of rows from the query results
        """
        cql_session = self.new_session(keyspace)
        cql_session.row_factory = dict_factory
        user_query = cql_session.execute(in_query)
        return [row for row in user_query]
