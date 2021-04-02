from pandas import read_excel
import pandas as pd
import PositiveCase as pc

file_name = 'dataset1.xlsx'

xls = pd.ExcelFile(file_name)
sheet = xls.sheet_names
zeroList = []

patientZero = []

for i in sheet:
    if i == 'Cases':
        pass
    else:
        zeroList.append(i)

df = read_excel(file_name, sheet_name = 'Cases')

for i in zeroList:
    temp = df[df["NRIC"]==i]
    for j in temp.values:
        newCase = pc.PositiveCase(j[0],j[1],j[2],j[3],j[4],j[5])
        # data = {
        #     "name": j[0],
        #     "nric": j[1],
        #     "location": j[2],
        #     "checkInDate": j[3],
        #     "checkInTime": j[4],
        #     "checkOutTime": j[5]
        # }
        # print(data)
        # newCase = pc.PositiveCase(data)
        # patientZero.append(newCase)

timePlace = df[(df["Check-in-date"]==newCase.checkInDate) & (df["Location"]=='Jewel Changi Airport') & (df["NRIC"]!=newCase.nric)]
print(timePlace)