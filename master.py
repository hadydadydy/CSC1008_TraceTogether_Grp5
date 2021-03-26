from pandas import read_excel

my_sheet = 'SafeEntry' # change it to your sheet name, you can find your sheet name at the bottom left of your excel file
file_name = 'dataset.xlsx' # change it to the name of your excel file

df = read_excel(file_name, sheet_name = my_sheet)

class Case:
    def __init__(self, nric, location, checkInDate, checkInTime, checkOutTime):
        self.nric = nric
        self.location = location
        self.checkInDate = checkInDate
        self.checkInTime = checkInTime
        self.checkOutTime = checkOutTime

print(len(df["NRIC"])) # shows headers with top 5 rows


