import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager
from helper import updateEvent, readEvent, updateCoreTag
import tempfile
import shutil

def get_roman_text(str):
    return str

# Loading JSON data from files
with open("to_update_event.json", 'r') as f:
    to_update_event = json.load(f)

# Loading JSON data from files
with open("raw_exams_orgnisation.json", 'r') as f:
    my_data = json.load(f)


def save_logs(new_logs, log_filename):
    existing_logs = {}
    if os.path.exists(log_filename):
        try:
            with open(log_filename, 'r') as f:
                existing_logs = json.load(f)
        except json.JSONDecodeError:
            existing_logs = {}
        except Exception as e:
            raise Exception(f"Error reading log file: {str(e)}")
    
    existing_logs.update(new_logs)
    
    tmp_dir = os.path.dirname(os.path.abspath(log_filename))
    tmp_fd, tmp_filename = tempfile.mkstemp(dir=tmp_dir, text=True)
    
    try:
        with os.fdopen(tmp_fd, 'w') as f:
            json.dump(existing_logs, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        
        shutil.move(tmp_filename, log_filename)
    
    except Exception as e:
        try:
            os.unlink(tmp_filename)
        except:
            pass
        raise Exception(f"Error writing log file: {str(e)}")


# function to get status
def is_all_events_processed(progress_file, ids):
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


def prepare_event_payload(res):
    # if (not "title_roman" in res or not res["title_roman"]) and "title" in res and "hi" in res["title"]:
    #     roman_text = get_roman_text(res["title"]["hi"])
    #     if roman_text:
    #         res["title_roman"] = {"hi": roman_text }
    #     print(roman_text)

    new_tags = []
    for tag in res["tags"]:
        if tag["nameId"] in to_update_event and tag["valueId"] in to_update_event[tag["nameId"]]:
            # print(to_update_event[tag["nameId"]][tag["valueId"]]["id"], """to_update_event[tag["nameId"]]""")
            if to_update_event[tag["nameId"]][tag["valueId"]]["id"]:
                new_tags.append({"nameId": tag["nameId"], "valueId": to_update_event[tag["nameId"]][tag["valueId"]]["id"]})
            else: raise ValueError(f"Can't find corresponding value")
        else: new_tags.append(tag)
    res["tags"] = new_tags
    return res





# Function to process a single event
def process_single_event(eventId, processed_events, lock, progress_file):
    log_messages = []
    # Lock only the critical section where processed_events is accessed
    with lock:
        is_not_processed = not eventId in processed_events or (not processed_events[eventId].get("status", None) == "success")

    if is_not_processed:
        print("Event", eventId)
        response = readEvent(eventId)
        # print(response, "response")
        if response:
            response = {key: value for key, value in response.items() if key not in ["component", "component_id", "created", "createdby", "forumLink", "notifications"]}
            if not isinstance(response.get("tags", []), list):
                response["tags"] = []
            response["eventId"] = eventId
            response = prepare_event_payload(response)
            final_response = updateEvent(response)
            log_entry = {
                "event": eventId,
                "updated_response": final_response,
                "status": "success" if final_response and final_response== "Save" else "failed"
            }
            if not final_response: log_entry["payload"] = response

            with lock:
                processed_events[eventId] = log_entry
                save_logs({eventId: log_entry}, progress_file)
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

    else:
        print("Already Event Proceesd", eventId)

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
        with ProcessPoolExecutor(max_workers=3) as executor:  # Adjust max_workers as needed
            futures = {executor.submit(process_single_event, eventId, processed_events, lock, progress_file): eventId for eventId in chunk}
            for future in as_completed(futures):
                eventId = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f'Event {eventId} generated an exception: {exc}')

    return is_all_events_processed(progress_file, eventIds)



# Function to prepare payload for exam or organisation
def prepare_payload_for_exam_or_organisation(exam_or_organisation, tag_type):
    if not isinstance(exam_or_organisation, dict):
        return None

    tag_id = exam_or_organisation.get("id")
    tags = exam_or_organisation.get("tags")
    core_tags = exam_or_organisation.get("coreTags", [])

    if tag_id is None or tags is None or tag_type not in ["Organisation", "Exam"]:
        return None

    new_tags = []
    for tag in tags:
        if tag["nameId"] in to_update_event and tag["valueId"] in to_update_event[tag["nameId"]]:
            if to_update_event[tag["nameId"]][tag["valueId"]]["id"]:
                new_tags.append({"nameId": tag["nameId"], "valueId": to_update_event[tag["nameId"]][tag["valueId"]]["id"]})
            else: raise ValueError(f"Can't find corresponding value")
        else: new_tags.append(tag)

    payload = {
        "tagId": tag_id,
        "tags": new_tags,
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
                payload = prepare_payload_for_exam_or_organisation(exam_or_organisation, type)
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
            log_messages.append(f"Exam or origination {exam_or_organisation_id} not found in My data")
        
        # Add log messages to the processed_events and save
        if log_messages:
            if exam_or_organisation_id not in processed_exams_or_organizations:
                processed_exams_or_organizations[exam_or_organisation_id] = {}
            if "log" not in processed_exams_or_organizations[exam_or_organisation_id]:
                processed_exams_or_organizations[exam_or_organisation_id]["log"] = []
            processed_exams_or_organizations[exam_or_organisation_id]["log"].extend(log_messages)
            save_logs(processed_exams_or_organizations, progress_file)
    
    return is_all_events_processed(progress_file, exams_or_organizations_ids)

all_events  = {
    "exams":[],
    "events": [],
    "organizations": []
}

for fields_data in to_update_event.values():
    for value_data in fields_data.values():
        for item in value_data["events"]:
            if item.get("label", None) == "Event": all_events["events"].append(item["id"])
            elif item.get("label", None) == "Exam": all_events["exams"].append(item["id"])
            elif item.get("label", None) == "Organisation": all_events["organizations"].append(item["id"])

all_events["events"] = list(set(all_events["events"]))
all_events["exams"] = list(set(all_events["exams"]))
all_events["organizations"] = list(set(all_events["organizations"]))

len_event = len(list(set(all_events["events"])))
len_exams = len(list(set(all_events["exams"])))
len_organizations = len(list(set(all_events["organizations"])))

print(f"events : {len_event}, exams: {len_exams}, organizations: {len_organizations}")

# isProcessed_events = process_events(["f3neA7MZ"])
# isProcessed_exam  = process_exam_and_organisation(all_events["organizations"], "Organisation", "Organisation_progress.json")
# isProcessed_organisation  = process_exam_and_organisation(all_events["exams"], "Exam", "Exams_progress.json")
# print(f"events: {isProcessed_events}")

isProcessed_events = process_events(all_events["events"])
isProcessed_exam  = process_exam_and_organisation(all_events["organizations"], "Organisation", "Organisation_progress.json")
isProcessed_organisation  = process_exam_and_organisation(all_events["exams"], "Exam", "Exams_progress.json")

# print(f"exams: {isProcessed_exam}, organizations: {isProcessed_organisation}")
print(f"events: {isProcessed_events}, exams: {isProcessed_exam}, organizations: {isProcessed_organisation}")