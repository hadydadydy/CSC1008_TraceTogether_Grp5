from pandas import read_excel
import pandas as pd
import PositiveCase as pc

file_name = 'dataset1.xlsx'

xls = pd.ExcelFile(file_name)
sheet = xls.sheet_names
zeroList = []
caseArr = []
patientZero = []
closeContacts = []

for i in sheet:
    if i == 'Cases':
        pass
    else:
        zeroList.append(i)

positive_cases_dict = {}

df = read_excel(file_name, sheet_name = 'Cases')

for i in zeroList:
    temp = df[df["NRIC"]==i]
    for j in temp.values:
        # print(j)
        # newCase=pc.PositiveCase(j[0],j[1],j[2],j[3],j[4],j[5])
        # print(newCase)
        data = {
            "name": j[0],
            "nric": j[1],
            "location": j[2],
            "checkInDate": j[3],
            "checkInTime": j[4],
            "checkOutTime": j[5]
        }
        # print(data)
        newCase = pc.PositiveCase(data)
        caseArr.append(newCase)
        # patientZero.append(newCase)
# for i in caseArr:
#     print(i.checkInDate)
totalCC=[]
for i in caseArr:
    timePlace=df[(df["Check-in-date"]==i.data["checkInDate"]) & (df["Location"]==i.data["location"]) & (df["NRIC"]!=i.data["nric"])]
    totalCC.append(timePlace)
    tempCC = timePlace['NRIC'].tolist()
    # for j in tempCC:
        # closeContacts=[[j for j in tempCC] for k in range(len(zeroList))]
    # print(closeContacts)
    # print(timePlace)

    for idx in range(len(zeroList)):
        key = zeroList[idx]
        positive_cases_dict[key] = pc.CCList()
        for j in tempCC:
            positive_cases_dict[key].insert(j)

results = pd.concat(totalCC)
for i in zeroList:
    print(positive_cases_dict[i].printList())