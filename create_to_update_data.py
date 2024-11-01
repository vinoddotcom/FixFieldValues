from Neo4j.neo4j_utils import get_tag_key, get_tag_values
from collections import defaultdict
import json

all_text_field_name_ids = [result.get("id", None) for result in get_tag_key(["Key", "Text"])]

tag_replace_map = {}

# Function to group objects by value and filter groups with two or more objects
def group_and_filter(objects):
    grouped = defaultdict(list)
    for obj in objects:
        grouped[obj['value']].append(obj)
    result = [group for group in grouped.values() if len(group) >= 2]
    return result

def find_greatest_event_count(objects):
    longest_events_obj = None
    max_length = -1
    
    for obj in objects:
        events_length = len(obj['events'])
        if events_length > max_length:
            max_length = events_length
            longest_events_obj = obj
    
    return longest_events_obj

for id in all_text_field_name_ids:
    tag_values = [res.get("nodeInfo", None) for res in get_tag_values(id)]
    duplicate_values = group_and_filter(tag_values)
    for values in duplicate_values:
        longest_events = find_greatest_event_count(values)
        for value in values:
            if not value["id"] == longest_events["id"]:
                if not id in tag_replace_map:
                    tag_replace_map[id] = { value["id"]: { "id": longest_events["id"], "events": value["events"] }}
                else:
                    tag_replace_map[id][value["id"]] = { "id": longest_events["id"], "events": value["events"] }
                print(len(values), value["id"], longest_events["id"], value)



with open("to_update_event.json", 'w') as file:
     json.dump(tag_replace_map, file, ensure_ascii=False)



# query_to_at_end = """ 
# Match (m:Key:Text)-[:VALUE]->(n:Value)
# where not m.id in ["1zWOGWtS", "3kE1juY6", "gaZ53yRq", "TjYfVePb", "2UU2evzg", 'LTSBsmlP', "hUzgT599"] and n.value =~ '.*[^a-zA-Z0-9\\s)]$'
# return n.value, n.id, m.name, m.id
# """
# query_to_at_start = """ 
# Match (m:Key:Text)-[:VALUE]->(n:Value)
# where not m.id in ["1zWOGWtS", "3kE1juY6", "gaZ53yRq", "TjYfVePb", "2UU2evzg", 'LTSBsmlP', "hUzgT599"] and n.value =~ '^[^a-zA-Z0-9\\s(].*'
# return n.value, n.id, m.name, m.id
# """