import pandas as pd
import numpy
#S9037583J, S9345678C, S7890123G
caselist = []
dataset = 'dataset_new.xlsx'

def close_contacts(n):
    #filter tracetogether token info for
    #BT strength > 90% and
    #connection time > 5 mins 
    #and append into a cc_list
    cc_list = []

    sheet = pd.read_excel(dataset, sheet_name=n)
    bt = pd.DataFrame(sheet, columns= ['BT-Strength'])
    bluetooth = bt["BT-Strength"].to_numpy()
    ct = pd.DataFrame(sheet, columns= ['Connection Time(s)'])
    time = ct["Connection Time(s)"].to_numpy()
    lst = sheet.values.tolist()
    lst = numpy.array(lst)
    namelst = lst[:,1]

    for idx, val in enumerate(bluetooth):
        if val >= 0.90:
            if time[idx] > 300:
                cc_list.append(namelst[idx])
    print(', '.join(cc_list))

def newcase():
    positivecase = input("Enter positive case: ")

    if positivecase is not None:
        #check here if positivecase is in dataset, if not return error msg
        try:
            if positivecase not in caselist:
                caselist.append(positivecase)
                print("SHN has ben issued to close contacts:")
                close_contacts(positivecase)
                print("Positive Cases: ")
                print(', '.join(caselist))

                cont = input("Enter more positive cases? (y/n): ")
                if cont == 'y':
                    newcase()
                elif cont == 'n':
                    exit
                else:
                    print("Err: Pls enter y or n only.")
            else:
                print("Target is already positive.")
                newcase()
        except:
            print("NRIC does not exist.")
            newcase()


newcase()