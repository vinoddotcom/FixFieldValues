import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager
from helper import updateEvent, readEvent, updateCoreTag
from neo4j import GraphDatabase

# Database configuration
url = "bolt://localhost:7687"
username = "neo4j"
password = "login@123"

# Loading JSON data from files
with open("location_map.json", 'r') as f:
    location_map = json.load(f)

with open("new_location_id_map.json", 'r') as f:
    unique_map = json.load(f)

with open("myData.json", 'r') as f:
    my_data = json.load(f)

#  Process the response to check for specific nameId keys
def process_response(response):
    tags = response.get("tags", [])
    yJhhcHi6_valueIds = []
    ZhWcSTMm_valueIds = set()  # Use a set for quick look-up

    # Collect all valueIds for both nameIds
    for tag in tags:
        if tag["nameId"] == "yJhhcHi6":
            yJhhcHi6_valueIds.append(tag["valueId"])
        elif tag["nameId"] == "ZhWcSTMm":
            ZhWcSTMm_valueIds.add(tag["valueId"])

    return yJhhcHi6_valueIds, ZhWcSTMm_valueIds

# Get the key from unique_map
def get_key_from_unique_map(value_id):
    string_value = location_map.get(value_id, None)
    if not string_value: return None
    return unique_map.get(string_value, None).get("valueId", None)


def find_valueIds_to_update(response):
    yJhhcHi6_valueIds, ZhWcSTMm_valueIds = process_response(response)
    valueIds_to_update = []
    for value_id in yJhhcHi6_valueIds:
        corresponding_id = get_key_from_unique_map(value_id)
        if not corresponding_id : raise ValueError(f"No corresponding key found in unique_map for valueId {value_id}")
        if corresponding_id and corresponding_id not in ZhWcSTMm_valueIds:
            valueIds_to_update.append(corresponding_id)

    return list(set(valueIds_to_update))


# Save logs to file
def save_logs(logs, progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            existing_logs = json.load(file)
    else:
        existing_logs = {}
    existing_logs.update(logs)
    with open(progress_file, 'w') as file:
            json.dump(existing_logs, file, ensure_ascii=False)

# function to get status
def get_status_success(progress_file, ids):
    with open(progress_file, 'r') as file:
            processed_events = json.load(file)

    for id_value in ids:
        if not (processed_events.get(id_value, {}).get("status") == "success" or processed_events.get(id_value, {}).get("status") == "no_need"):
            return False
    return True

def store_save_logs(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            existing_logs = json.load(file)
    else:
        existing_logs = {}
    with open(f"store_{progress_file}", 'w') as file:
            json.dump(existing_logs, file, ensure_ascii=False)


def preapre_event_payload(res):
    print(res)
    if (not "title_roman" in res or not res["title_roman"]) and "title" in res and "hi" in res["title"]:
        roman_text = get_roman_text(res["title"]["hi"])
        if roman_text:
            res["title_roman"] = {"hi": roman_text }
        print(roman_text)
        
    return res





# Function to process a single event
def process_single_event(eventId, processed_events, lock, progress_file):
    log_messages = []
    # Lock only the critical section where processed_events is accessed
    with lock:
        event_status = not eventId in processed_events or (not processed_events[eventId].get("status", None) == "success")

    if event_status:
        print("Event", eventId)
        response = readEvent(eventId)
        if response:
            valueIds_to_update = find_valueIds_to_update(response)
            if valueIds_to_update:
                response = {key: value for key, value in response.items() if key not in ["component", "component_id", "created", "createdby", "forumLink", "notifications"]}
                if not isinstance(response.get("tags", []), list):
                    response["tags"] = []
                for value in valueIds_to_update:
                    response["tags"].append({"nameId": "ZhWcSTMm", "valueId": value})
                response["eventId"] = eventId
                response = preapre_event_payload(response)
                print(response)
                final_response = None
                final_response = updateEvent(response)
                log_entry = {
                    "event": eventId,
                    "updated_response": final_response,
                    "status": "success" if final_response and final_response== "Save" else "failed"
                }

                if not final_response: log_entry["payload"] = response
                with lock:
                    processed_events[eventId] = log_entry
                    print("Saving log event", eventId)
                    save_logs({eventId: log_entry}, progress_file)
            else:
                log_messages.append(f"Event {eventId} does not contain required nameIds. Or updated already")
                if eventId not in processed_events:
                    processed_events[eventId] = {}
                processed_events[eventId]["status"] = "no_need"
        else:
            log_messages.append(f"Read event API failed for event {eventId}.")
        
        # Add log messages to the processed_events and save
        with lock:
            if log_messages:
                if eventId not in processed_events:
                    processed_events[eventId] = {}
                if "log" not in processed_events[eventId]:
                    processed_events[eventId]["log"] = []
                processed_events[eventId]["log"].extend(log_messages)
                save_logs({eventId: processed_events[eventId]}, progress_file)

    # else:
    #     print("Already Event Proceesd", eventId)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

# Function to process the events using multiprocessing
def process_events(eventIds, progress_file='event_progress.json'):
    if eventIds == []: return True

    # Load existing progress if it exists
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            processed_events = json.load(file)
    else:
        processed_events = {}

    manager = Manager()
    lock = manager.Lock()
    batch_size = 30
    for chunk in chunks(eventIds, batch_size):
        with ProcessPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
            futures = {executor.submit(process_single_event, eventId, processed_events, lock, progress_file): eventId for eventId in chunk}
            for future in as_completed(futures):
                eventId = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f'Event {eventId} generated an exception: {exc}')

    return get_status_success(progress_file, eventIds)



# Function to prepare payload for exam or organisation
def prepare_payload_for_exam_or_organisation(exam_or_organisation, valueIds_to_update, tag_type):
    if not isinstance(exam_or_organisation, dict):
        return None

    tag_id = exam_or_organisation.get("id")
    tags = exam_or_organisation.get("tags")
    core_tags = exam_or_organisation.get("coreTags", [])

    if tag_id is None or tags is None or tag_type not in ["Organisation", "Exam"]:
        return None
    for new_value_id in valueIds_to_update:
        tags.append({"nameId": "ZhWcSTMm", "valueId": new_value_id})

    payload = {
        "tagId": tag_id,
        "tags": tags,
        "coreTags": core_tags,
        "tagType": tag_type
    }
    return payload

    

# Function to process the exam and organisation
def process_exam_and_organisation(exams_or_organizations_ids, type, progress_file):
    # Load existing progress if it exists
    if not progress_file: raise ValueError("Provide progress_file first")
    if exams_or_organizations_ids == []: return True
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            processed_exams_or_organizations = json.load(file)
    else:
        processed_exams_or_organizations = {}

    # Iterate over the exam and organisation
    for exam_or_organisation_id in exams_or_organizations_ids:
        log_messages = []
        if exam_or_organisation_id not in processed_exams_or_organizations or processed_exams_or_organizations[exam_or_organisation_id].get("status") == "failed":
            print(f"{type} {exam_or_organisation_id}")
            exam_or_organisation = my_data.get(type.lower() + "s", {}).get(exam_or_organisation_id, None)
            if exam_or_organisation:
                valueIds_to_update = find_valueIds_to_update(exam_or_organisation)
                if valueIds_to_update:
                    payload = prepare_payload_for_exam_or_organisation(exam_or_organisation, valueIds_to_update, type)
                    if payload:
                        final_response = updateCoreTag(payload)
                        log_entry = {
                            "event": exam_or_organisation_id,
                            "updated_response": final_response,
                            "status": "success" if final_response else "failed"
                        }
                        processed_exams_or_organizations[exam_or_organisation_id] = log_entry
                        save_logs(processed_exams_or_organizations, progress_file)
                    else:
                        log_messages.append(f"Unable to create payload")
                else:
                    log_messages.append(f"Exam or origination {exam_or_organisation_id} does not contain required nameIds. Or updated already")
            else:
                log_messages.append(f"Exam or origination {exam_or_organisation_id} not found in My data")
        
        # Add log messages to the processed_events and save
        if log_messages:
            if exam_or_organisation_id not in processed_exams_or_organizations:
                processed_exams_or_organizations[exam_or_organisation_id] = {}
            if "log" not in processed_exams_or_organizations[exam_or_organisation_id]:
                processed_exams_or_organizations[exam_or_organisation_id]["log"] = []
            processed_exams_or_organizations[exam_or_organisation_id]["log"].extend(log_messages)
            save_logs(processed_exams_or_organizations, progress_file)
    
    return get_status_success(progress_file, exams_or_organizations_ids)


used_location_query = """
    MATCH (n:NTag {id: "yJhhcHi6"})-[:VALUE]->(val)
    MATCH (val)-[:TAGGED_WITH]->(connectedNode)
    RETURN collect(DISTINCT val.id) AS uniqueIds
"""


# Neo4j query
query = """
    MATCH (n:NTag {id: $id})
    OPTIONAL MATCH (n)-[:TAGGED_WITH]->(event:Event)
    WITH n, COALESCE(COLLECT(DISTINCT event.id), []) AS eventids
    OPTIONAL MATCH (n)-[:TAGGED_WITH]->(org:Organisation)
    WITH n, eventids, COALESCE(COLLECT(DISTINCT org.id), []) AS orgIds
    OPTIONAL MATCH (n)-[:TAGGED_WITH]->(exam:Exam)
    WITH n, eventids, orgIds, COALESCE(COLLECT(DISTINCT exam.id), []) AS examIds
    RETURN {events: eventids, organizations: orgIds, exams: examIds} AS res
"""

delete_query = """
    MATCH (node:NTag {id: $id})
    DETACH DELETE node
"""

# Initialize the Neo4j driver
driver = GraphDatabase.driver(url, auth=(username, password))

# Fetch the unique location IDs from the Neo4j database
with driver.session() as session:
    result = session.run(used_location_query)
    used_location_ids = list(result)[0].get("uniqueIds", [])

# used_location_ids = ["0hCaZsxc"]
# used_location_ids = ["0ZLAvymI"]
# used_location_ids = ["2AqnC5z5", "3K9u9JCv"]
# used_location_ids = ["2gQHglsO", "2gFChln2"]
# used_location_ids = ["0N611QmB"]
# used_location_ids = ["4JqEah22"]




def get_event_organizations_exams(id):
    with driver.session() as session:
        res = session.run(query, {"id": id})
        org_exam_event = list(res)[0].get("res", [])
        return org_exam_event

def delete_node(id):
    with driver.session() as session:
        session.run(delete_query, {"id": id})


for item in used_location_ids:
    organizations_exam_event = get_event_organizations_exams(item)
    print(organizations_exam_event)
    isProcessed_events = process_events(list(set(organizations_exam_event.get("events", []))))
    isProcessed_exam  = process_exam_and_organisation(list(set(organizations_exam_event.get("organizations", []))), "Organisation", "Organisation_progress.json")
    isProcessed_organisation  = process_exam_and_organisation(list(set(organizations_exam_event.get("exams", []))), "Exam", "Exams_progress.json")
    print(isProcessed_events, isProcessed_exam, isProcessed_organisation, item)
    if isProcessed_events and isProcessed_exam and isProcessed_organisation:
        delete_node(item)

    store_save_logs('event_progress.json')
    store_save_logs('Exams_progress.json')
    store_save_logs('Organisation_progress.json')

