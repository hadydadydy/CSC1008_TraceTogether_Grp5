from pandas import read_excel
import pandas as pd
import CloseContactList as cc

file_name = 'dataset_final_v2.xlsm'
# file_name1 = 'dataset1.xlsx'

# xl = pd.ExcelFile(file_name)
# res = len(xl.sheet_names)

xls = pd.ExcelFile(file_name)
sheet = xls.sheet_names

# To store the positive cases (key: positive case's NRIC, value: CloseContactList)
positive_cases_dict = {}
positive_cases_keys = []
caseArr = []
# positive_cases_keys = ['positive_case_1', 'positive_case_2']

for i in sheet:
    if i == 'SafeEntry':
        pass
    else:
        positive_cases_keys.append(i)


# For iterating through positive cases and assigning close contacts to each.
# Once filtered by Hady's contactTrace() function which returns close contact array.
df = read_excel(file_name, sheet_name= 'SafeEntry')

for i in positive_cases_keys:
    temp = df[df["NRIC"]==i]
    for j in temp.values:
        data = {
            "name": j[0],
            "nric": j[1],
            "location": j[2],
            "checkInDate": j[3],
            "checkInTime": j[4],
            "checkOutTime": j[5]
        }
        newCase = cc.Case(data)
        caseArr.append(newCase)

for idx in range(len(positive_cases_keys)):
    key = positive_cases_keys[idx] # Replace with positive case's NRIC.
    positive_cases_dict[key] = cc.CloseContactList()

    # Sample data to insert as close contacts for each positive case in the dict.
    # df_temp = read_excel(file_name, sheet_name = 'Cases')
    for i in caseArr:
        op = read_excel(file_name, sheet_name=i.data["nric"])
        blueTooth = op[(op["BT-Strength(%)"] >= 90)]
        timePlace=df[(df["Check-in-date"]==i.data["checkInDate"]) & (df["Location"]==i.data["location"]) & (df["NRIC"]!=i.data["nric"])]
        for j in timePlace.values:
            for k in blueTooth.values:
                if k[1] == j[1]:
                    data = {
                        "name": j[0],
                        "nric": j[1],
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
for i in positive_cases_keys:
    print("Close Contacts:")
    positive_cases_dict[i].printList(i)

# print(blueTooth)