import openpyxl

sheet_name = "FieldAreaSubject--h4i4xwcE"
file_name = "text_key_value_sheet_data_v1.xlsx"

def read_sheet(filename, sheet_identifier):
    # Load the workbook
    workbook = openpyxl.load_workbook(filename)
    
    # Get the sheet
    if isinstance(sheet_identifier, int):
        sheet = workbook.worksheets[sheet_identifier]
    else:
        sheet = workbook[sheet_identifier]
    
    # Read data from the sheet
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(list(row))  # Ensure each row is a list
    
    return data

# Example usage
data = read_sheet(file_name, sheet_name)
print(data)
