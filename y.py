import openpyxl
from collections import defaultdict

file_name = "text_key_value_sheet_data-v2.xlsx"

workbook = openpyxl.load_workbook(file_name)


def read_sheet(sheet_identifier):
    if isinstance(sheet_identifier, int):
        sheet = workbook.worksheets[sheet_identifier]
    else:
        sheet = workbook[sheet_identifier]
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(list(row))  # Ensure each row is a list
    
    return data

data = []
unique_words = set()
frequency_dict = defaultdict(list)
word_count = defaultdict(int)

def count_word_frequencies(strings):
    for string in strings:
        if not string: continue
        words = string.split()
        for word in words:
            word_count[word] += 1
    return word_count


def classify_words_by_frequency():
    for word, count in word_count.items():
        frequency_dict[count].append(word)
    return frequency_dict



def save_to_file(frequency_dict):
    print(len(list(frequency_dict)))
    with open("unique_words.txt", 'w') as file:
       for frequency, words in sorted(frequency_dict.items()):
           file.write(f"{frequency} times: {'****'.join(words)}\n\n\n\n\n\n\n\n\n")


sheet_names = workbook.sheetnames

for sheet_name in sheet_names:
    print(sheet_name)
    data = [item[3] for item in  read_sheet(sheet_name)]
    count_word_frequencies(data)

frequency_dict = classify_words_by_frequency()

save_to_file(frequency_dict)

