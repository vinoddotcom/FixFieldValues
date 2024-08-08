import re
import inflect
import openpyxl
from multiprocessing import Pool, cpu_count
import json

p = inflect.engine()

def preprocess(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^A-Za-z0-9\s]', ' ', text).lower()
    return text







sheet_identifier = "Course name--nWIiWAv7"
file_name = "text_key_value_sheet_data-v3.xlsx"

workbook = openpyxl.load_workbook(file_name)

if isinstance(sheet_identifier, int):
    sheet = workbook.worksheets[sheet_identifier]
else:
    sheet = workbook[sheet_identifier]
    
singularize_data = {}

def singularize(str):
    str_processed = preprocess(str)
    singularize_data[str] = " ".join([p.singular_noun(word) or word for word in str_processed.split()])
    


def read_sheet():
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(list(row))  # Ensure each row is a list
    
    return data

def save_to_json(similar_pairs, filename):
    # Convert the defaultdict to a regular dictionary for JSON serialization
    regular_dict = {key: [{"string": pair[0], "similarity": pair[1]} for pair in value] for key, value in similar_pairs.items()}
    with open(filename, 'w') as json_file:
        json.dump(regular_dict, json_file, indent=4)

all_data = read_sheet()
similar_strings = [item[3] for item in all_data if item[3]]
for strs in similar_strings:
    singularize(strs)
# save_to_json(similar_strings, 'Course name-similar_strings.json')
# for string, similar in similar_strings.items():
#     for similar_string, similarity in similar:
#         print(f"'{string}' is {similarity*100:.2f}% similar to '{similar_string}'")
for item in all_data:
    for item_d in all_data:
        # print(singularize_data[item[3]], singularize_data[item_d[3]])
        if not item[3] or not item_d[3] or item[3] == item_d[3]: continue
        if singularize_data[item[3]] == singularize_data[item_d[3]]:
            print(f"'{item[3]}'", "   -   ", f"'{item_d[3]}'")