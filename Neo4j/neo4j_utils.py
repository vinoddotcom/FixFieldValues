from Neo4j.neo4jDB_connection import Neo4jConnection

from config import NEO4J_URL,NEO4J_PASSWORD,NEO4J_USERNAME

neo4j_conn = Neo4jConnection(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD)

fix_plural = """
    MATCH (n:Value)
    WHERE n.value CONTAINS $query
    SET n.value = REPLACE(n.value, $query, $replace)
    RETURN n
"""

def fix_plural_values(queryObj):
    neo4j_conn.connect()
    for key, item in queryObj.items():
        parameters = {"query": key, "replace": item}
        neo4j_conn.query(fix_plural, parameters)
        print(f"fixed {key} to {item}")