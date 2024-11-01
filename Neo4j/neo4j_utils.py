from Neo4j.neo4jDB_connection import Neo4jConnection

from config import NEO4J_URL,NEO4J_PASSWORD,NEO4J_USERNAME

neo4j_conn = Neo4jConnection(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD)

fix_plural = """
    MATCH (:NTag {id: "q9LzwSSI"})-[:VALUE]->(n:Value)
    WHERE n.value CONTAINS $query
    SET n.value = REPLACE(n.value, $query, $replace)
    RETURN n
"""

tag_values_query = """
    MATCH (:NTag {id: $id})-[:VALUE]->(n:Value)
    OPTIONAL MATCH (n)-[:TAGGED_WITH]-(e)
    WITH n.value AS value, n.id AS id, COLLECT({id: e.id, label: LABELS(e)[0]}) AS events
    RETURN { value: value, id: id, events: events } AS nodeInfo
"""

neo4j_conn.connect()

def check_is_value_exist(key_id, value_id):
    query= "MATCH (:Key { id: $key_id })-[:VALUE]->(n:Value { id : $value_id }) RETURN n"
    parameters = {"key_id": key_id, "value_id" : value_id }
    res = neo4j_conn.query(query, parameters)
    return res

def set_value(key_id, value_id, corrected_val):
    query="""
    MATCH (:Key {id: $key_id})-[:VALUE]->(n:Value {id : $value_id})
    SET n.value = $val
    return n
    """
    parameters = {"key_id": key_id, "value_id" : value_id, "val":corrected_val }
    res = neo4j_conn.query(query, parameters)
    return res


def delete_unused_tag_val():
    query = """
    MATCH (n:NTag:Value)
    where not (n)-[:TAGGED_WITH]->()
    detach delete n
    """
    neo4j_conn.query(query)

def get_tag_key(labels):
    query = f"MATCH (n:{(':').join(labels)}) RETURN n.id as id"
    res = neo4j_conn.query(query)
    return res

def get_tag_values(id):
    parameters = {"id": id}
    res = neo4j_conn.query(tag_values_query, parameters)
    return res


def search_tag_values(id, name):
    parameters = {"id": id, "name": name}
    query = """MATCH (:NTag:Key {id: $id})-[:VALUE]->(n:NTag:Value {value: $name}) return n"""
    res = neo4j_conn.query(query, parameters)
    return res