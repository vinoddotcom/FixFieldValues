import re
from difflib import SequenceMatcher
from collections import defaultdict
import openpyxl
from multiprocessing import Pool, cpu_count
import json

def preprocess(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^A-Za-z0-9\s]', '', text).lower()
    return text

def remove_stopwords(words):
    stopwords = {'and', 'in', 'the', 'is', 'at', 'which', 'on', 'a', 'to', 'of', 'for'}
    return [word for word in words if word not in stopwords]

def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def compare_strings(args):
    i, words1, words_list, threshold = args
    similar_pairs = []
    print(i)
    for j, words2 in enumerate(words_list):
        if i != j and words1 != words2:
            text1 = ' '.join([word for word in words1 if word not in words2])
            text2 = ' '.join([word for word in words2 if word not in words1])
            if text1 and text2:
                similarity = calculate_similarity(text1, text2)
                if similarity >= threshold:
                    similar_pairs.append((i, j, similarity))
    return similar_pairs

def find_similar_strings(strings, threshold=0.95):
    preprocessed_strings = [preprocess(string) for string in strings]
    words_list = [remove_stopwords(string.split()) for string in preprocessed_strings]

    num_cpus = cpu_count()
    with Pool(num_cpus) as pool:
        results = pool.map(compare_strings, [(i, words1, words_list, threshold) for i, words1 in enumerate(words_list)])

    similar_pairs = defaultdict(list)
    for result in results:
        for i, j, similarity in result:
            similar_pairs[strings[i]].append((strings[j], similarity))

    return similar_pairs


sheet_identifier = "FieldAreaSubject--h4i4xwcE"
file_name = "text_key_value_sheet_data-v3.xlsx"

workbook = openpyxl.load_workbook(file_name)

if isinstance(sheet_identifier, int):
    sheet = workbook.worksheets[sheet_identifier]
else:
    sheet = workbook[sheet_identifier]
    

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


similar_strings = find_similar_strings([item[3] for item in read_sheet() if item[3]])
save_to_json(similar_strings, 'FieldAreaSubject-similar_strings-2.json')
for string, similar in similar_strings.items():
    for similar_string, similarity in similar:
        print(f"'{string}' is {similarity*100:.2f}% similar to '{similar_string}'")

# with open("Course name-similar_strings.json", 'r') as json_file:
#     data = json.load(json_file)

# total_seen = {}
# obj = {}

# for key , value in data.items():
#     if key in total_seen: continue
#     seen = set()
#     unique_objects = []
#     for item in value:
#         if item["string"] not in seen:
#             seen.add(item["string"])
#             total_seen[ item["string"]] = 1
#             unique_objects.append(item)
#     obj[key] = unique_objects

#     with open('Course name-similar_strings-1.json', 'w') as json_file:
#         json.dump(obj, json_file, indent=4)