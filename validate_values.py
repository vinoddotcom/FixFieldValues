import re
import datetime
import openpyxl
from Neo4j.neo4j_utils import get_tag_values, check_exist

text_keys = ["3PvVhPBF","74X1HhtR","8lw29cmS","Bv2ZOMzp","Fcm0skbv","HXKXXgut","LMGjNRLB","LyLh6cz8","5GH9iXBb","MI8XYecF","MgHVVPYR","OwIM1KAN","ScNU9SmO","Sd1YZBDu","UnAo4ITS","VIPwQsKv","eEPkh9p7","h4i4xwcE","iJg6EsMk","ilZxrAUM","jw58ZOFp","nWIiWAv7","pBL58aed","q9LzwSSI","sK04P6qT","3CMVAjGP","4pEkYi6u","koB6smr5"]
link = ["gaZ53yRq", "TjYfVePb", "2UU2evzg", "LTSBsmlP", "hUzgT599"]
date = ["Fx8qspPX","5pb8RPB8","QncoLeTV","jAP1LfPz","w3krZ0Dx","t60hXQOX","EFaWKQJy","4WHqv7GA","PRJ6dHSW","IRjAgSmX","snXVSiKo","SzeeR4ci","5HiKjeRR","NMO4Ob7r","lDMkaMHN","BacdiitI","XEjrQYHU","N7sHYMBr","TaKS8r6f","qJb5DHRo","Sr4NfLwH","GjZLY0ru","eQ9Oa0jj","18mYoBSp","iZFmRVDI","5gSUXZbt","Jp91fNOw","lOJzoh3X","atnz22UZ","3tobG0Ll","6jULpVIC","8KPwwUM7","UKQNGp7G","MlWsZKAO","g0nD0Eci","3XF4Jwmp","knqaRa5m","okluikCa","DT8oT2db","OlgUCTED","phBCmCLS","9gUxVMHP","QZBQoY1q","HUv2egrv","K3is8qpk","m2NkMsQW","C7eU8wmq","57wNbySh"]
number = ["3t4Jn4gc","JUVYiZ11","5bTHsTg6","fgoGRSvp","eXiPSdCT", 'zJ71l6ue']


def check_string(s: str) -> bool:
    # Check if the string is a URL
    url_pattern = re.compile(r'(https?://|www\.)')
    if url_pattern.search(s):
        return False
    
    # Check if the string is a whole number
    if s.isdigit():
        return False
    
    # Check if the string starts with a special character except '('
    if re.match(r'^[^a-zA-Z0-9(]', s):
        return False
    
    # Check if the string ends with a special character except ')'
    if re.match(r'.*[^a-zA-Z0-9)]$', s):
        return False
    
    # Check if the length of the string is greater than 3
    if len(s) < 3:
        return False

    return True

def is_valid_timestamp(timestamp):
    try:
        # Convert the timestamp to a datetime object
        date_time = datetime.datetime.fromtimestamp(timestamp)
        
        # Check if the date is within a reasonable range
        if datetime.datetime(1970, 1, 1) <= date_time <= datetime.datetime.now():
            return True
        else:
            return False
    except (ValueError, OverflowError):
        return False

def is_link(value):
    # Regular expression to match URLs
    regex = re.compile(
        r'^(https?:\/\/)?'  # http:// or https://
        r'([\da-z\.-]+)\.'  # domain name and extension
        r'([a-z\.]{2,6})'  # domain extension
        r'([\/\w \.-]*)*\/?$'  # resource path
    )
    
    # Check if the value matches the regex
    if re.match(regex, value):
        return True
    return False


def is_number(s: str) -> bool:
    pattern = r'^-?\d+(\.\d+)?$'
    return re.match(pattern, s) is not None

def sanitize_sheet_title(title):
    invalid_chars = r'/\*?[]:'
    for char in invalid_chars:
        title = title.replace(char, '')
    return title

workbook = openpyxl.Workbook()
workbook.remove(workbook.active)

for text_key in text_keys:
    tag_key =  check_exist(text_key, ["Key","Text"])
    key_name = tag_key[0].get("n", {})["name"]
    title = sanitize_sheet_title(f"{key_name}--{text_key}")
    sheet = workbook.create_sheet(title=title)
    tag_values = [res.get("nodeInfo", None) for res in get_tag_values(text_key)]
    sheet.append(["Tag ID", "Value ID","Value", "Corrected Value", "Status", "Connected Events Count"])
    for row_index, row_data in enumerate(tag_values, start=2):  # Start from row 2
            sheet.append([text_key, row_data["id"], row_data["value"], "", "Pass" if check_string(row_data["value"]) else "Fail", len(row_data["events"])])

workbook.save("text_key_value_sheet_data.xlsx")