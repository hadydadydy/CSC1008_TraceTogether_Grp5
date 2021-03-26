from pandas import read_excel

my_sheet = 'Dataset 1' # change it to your sheet name, you can find your sheet name at the bottom left of your excel file
file_name = 'dataset.xlsx' # change it to the name of your excel file

df = read_excel(file_name, sheet_name = my_sheet)
print(len(df["Device ID"])) # shows headers with top 5 rows
