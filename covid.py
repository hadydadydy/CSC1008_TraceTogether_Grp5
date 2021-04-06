import pandas as pd
import numpy
#S9037583J, S9345678C, S7890123G
caselist = []
all_cc = []
dataset = 'dataset_new.xlsx'

#filter tracetogether token info for
#BT strength > 90% and connection time > 5 mins 
def close_contacts(n):
    cc_list = []
    
    sheet = pd.read_excel(dataset, sheet_name=n) #import excel sheet

    bt = pd.DataFrame(sheet, columns= ['BT-Strength']) #import BT-Strength excel column
    bluetooth = bt["BT-Strength"].to_numpy() #convert column data into numpy list

    ct = pd.DataFrame(sheet, columns= ['Connection Time(s)'])#import Connection Time excel column
    time = ct["Connection Time(s)"].to_numpy() #convert column data into numpy list

    lst = sheet.values.tolist() #import all data from excel sheet
    lst = numpy.array(lst) #convert data to numpy list

    namelst = lst[:,1] #list of 1st index of all the rows in lst

    #loop through indexes of bluetooth numpy list
    for idx, val in enumerate(bluetooth):
        if val >= 0.90: #if bluetooth strength more than 90%
            if time[idx] > 300: #if connection time is more than 5 minutes 
                cc_list.append(namelst[idx]) #add name to close contact list

    all_cc.append(cc_list) #add this contact list to total close contacts list

    print(', '.join(cc_list))
    
#adding in a new positive case
def newcase():
    positivecase = input("Enter positive case: ")

    if positivecase is not None:
        #check here if positivecase is in dataset, if not return error msg
        try:
            #check if inputted case has already tested positive
            if positivecase not in caselist:
                caselist.append(positivecase) #add case to positive case list
                print("SHN has ben issued to close contacts:")
                close_contacts(positivecase) #print close contacts of this case
                print("All close contacts:")

                #print each positive case's close contacts
                for i in range(len(all_cc)):
                    strcc = ', '.join(all_cc[i])
                    print(positivecase, "-", strcc) 
                    
                print("Positive Cases: ")
                print(', '.join(caselist)) #print all positive cases

                cont = input("Enter more positive cases? (y/n): ")
                if cont == 'y':
                    newcase() #recursive call to continue adding new cases 
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
