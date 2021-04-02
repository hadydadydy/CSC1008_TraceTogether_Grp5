from pandas import read_excel
import pandas as pd
import CloseContactList as cc

file_name = 'dataset.xlsx'
file_name1 = 'dataset1.xlsx'

# xl = pd.ExcelFile(file_name)
# res = len(xl.sheet_names)

# To store the positive cases (key: positive case's NRIC, value: CloseContactList)
positive_cases_dict = {}
positive_cases_keys = ['positive_case_1', 'positive_case_2']

# For iterating through positive cases and assigning close contacts to each.
# Once filtered by Hady's contactTrace() function which returns close contact array.
for idx in range(len(positive_cases_keys)):
    key = positive_cases_keys[idx] # Replace with positive case's NRIC.
    positive_cases_dict[key] = cc.CloseContactList()

    # Sample data to insert as close contacts for each positive case in the dict.
    df_temp = read_excel(file_name, sheet_name = str(idx+1))
    for j in df_temp.values:
        data = {
            "nric": j[0],
            "name": j[1],
            "location": j[2],
            "checkInDate": j[3],
            "checkInTime": j[4],
            "checkOutTime": j[5]
        }
        # Create new case using data
        newCase = cc.Case(data)
        
        # Insert new case into positive case's CloseContactList by key
        positive_cases_dict[key].insert(newCase)
        
# Print positive case's CloseContactList by key
print(positive_cases_dict['positive_case_2'].printList())