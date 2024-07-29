from neo4j import GraphDatabase


class Neo4jConnection:
    """
    A class representing a connection to a Neo4j database.

    Attributes:
    - uri: The URI of the Neo4j database.
    - username: The username for authentication.
    - password: The password for authentication.
    """

    def __init__(self, uri, username, password):
        """
        Initialize a Neo4jConnection object with the given URI, username, and password.

        Parameters:
        - uri (str): The URI of the Neo4j database.
        - username (str): The username for authentication.
        - password (str): The password for authentication.
        """
        self._uri = uri
        self._username = username
        self._password = password
        self._driver = None

    def close(self):
        """Close the connection to the Neo4j database."""
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        """Establish a connection to the Neo4j database."""
        self._driver = GraphDatabase.driver(
            self._uri, auth=(self._username, self._password))

    def _execute_query(self, tx, query, parameters=None):
        result = tx.run(query, parameters)
        return [record for record in result]

    def query(self, query, parameters=None):
        """
        Execute a read query with optional parameters.

        Parameters:
        - query (str): The Cypher query to execute.
        - parameters (dict, optional): Parameters to pass to the query.
        """
        with self._driver.session() as session:
            result = session.read_transaction(
                self._execute_query, query, parameters)
            return list(result)

    def get_session(self):
        """Get the active session for the connection."""
        return self._driver.session()
