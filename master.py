from pandas import read_excel
import pandas as pd
import numpy
import CloseContactList as cc
import graphviz

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QInputDialog, QPushButton, QLineEdit, QMessageBox
# from PyQt5.QtWebEngineWidgets import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import sys
import folium
import io

file_name = 'dataset_final_v2.xlsm'
# file_name1 = 'dataset1.xlsx'

# xl = pd.ExcelFile(file_name)
# res = len(xl.sheet_names)

xls = pd.ExcelFile(file_name)
sheet = xls.sheet_names
df = read_excel(file_name, sheet_name= 'SafeEntry')

# To store the positive cases (key: positive case's NRIC, value: CloseContactList)
positive_cases_dict = {}
positive_cases_keys = []
caseArr = []
digraphEdges = [] # Edges of each positive case
app =  QApplication(sys.argv)
graphWindow = QMainWindow()
# positive_cases_keys = ['positive_case_1', 'positive_case_2']

# class MyError(Exception):
#     pass

def closeWindow():
    print("Button 1 clicked")
    graphWindow.close()

def showCloseContacts(app, graphWindow):
    graphWindow.setWindowTitle("DiGraph")

    graphWindow.central_widget = QWidget()               
    graphWindow.setCentralWidget(graphWindow.central_widget)  

    lay = QVBoxLayout(graphWindow.central_widget)

    shnLabel = QtWidgets.QLabel("SHN has been issued to close contacts")
    
    graphPicLabel = QtWidgets.QLabel(graphWindow)
    pixmap = QPixmap('digraph.png')
    graphPicLabel.setPixmap(pixmap)
    graphWindow.resize(pixmap.width(), pixmap.height())

    msg = QMessageBox(graphWindow)
    msg.setIcon(QMessageBox.Information)

    msg.setText("Would you like to add more positive cases?")
    msg.setWindowTitle("MessageBox demo")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    # msg.buttonClicked.connect(msgbtn)

    lay.addWidget(shnLabel)
    lay.addWidget(graphPicLabel)
    lay.addWidget(msg)

    graphWindow.show()

    retval = msg.exec_()

    if retval == QMessageBox.Yes:
        return 'y'
    elif retval == QMessageBox.No:
        return 'n'

def creategraph(): 
    d = graphviz.Digraph()
    d.attr(size='10,10')

    for i in digraphEdges:
        for j in i:
            d.edge(j[0],j[1])

    d.render('digraph', format='png', view=False)

def close_contacts(n):
    temp = df[df["NRIC"]==n]
    # if temp == None:
    #     raise MyError('NRIC not found in database')
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


    # key = n # Replace with positive case's NRIC.
    # positive_cases_dict[key] = cc.CloseContactList()
    positive_cases_dict[n] = cc.CloseContactList()

        # Sample data to insert as close contacts for each positive case in the dict.
        # df_temp = read_excel(file_name, sheet_name = 'Cases')

    for i in caseArr:
        data = pd.read_excel(file_name, sheet_name=i.data["nric"])
        op = data.drop_duplicates(subset=["NRIC"],keep="last", inplace=True)
        # bt = pd.DataFrame(op, columns= ['BT-Strength(%)'])
        # bluetooth = bt["BT-Strength(%)"].to_numpy()
        # ct = pd.DataFrame(op, columns= ['Connection Time(s)'])
        # time = ct["Connection Time(s)"].to_numpy()

        # lst = op.values.tolist()
        # lst = numpy.array(lst)
        # namelst = lst[:1]

        blueTooth = data[(data["BT-Strength(%)"] >= 90) & (data["Connection Time(s)"] > 300)]
        timePlace = df[(df["Check-in-date"]==i.data["checkInDate"]) & (df["Location"]==i.data["location"]) & (df["NRIC"]!=i.data["nric"])]
        # for j in timePlace.values:
            # for k in blueTooth.values:
                # if k[1] == j[1]:
        
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
                    positive_cases_dict[i.data["nric"]].insert(newCase)
    
    for i in positive_cases_keys:
        print("Close Contacts:")
        positive_cases_dict[i].printList(i)
        # digraphEdges.append(positive_cases_dict[i].printList(i))

    digraphEdges.append(positive_cases_dict[n].edges(n))
    creategraph()

    # showCloseContacts(app, graphWindow)

# for i in sheet:
#     if i == 'SafeEntry':
#         pass
#     else:
#         positive_cases_keys.append(i)
# app =  QApplication(sys.argv)
warningWindow = QMainWindow()

def showWarning(text):
    msgBox = QMessageBox(warningWindow)
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle('Oops!')
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    #    msgBox.buttonClicked.connect(msgButtonClick)
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('OK clicked')
        newcase(app, newCaseWindow)

newCaseWindow = QMainWindow()

def newcase(app, newCaseWindow):
    newCaseWindow.central_widget = QWidget()               
    newCaseWindow.setCentralWidget(newCaseWindow.central_widget)  

    positivecase, okPressed = QInputDialog.getText(newCaseWindow, "CSC1008 TraceTogether","Enter new positive case:", QLineEdit.Normal, "")
    if okPressed and positivecase != '':
        print(positivecase)
    else:
        sys.exit()

    if positivecase is not None:
        #check here if positivecase is in dataset, if not return error msg
        #try:
            #check if inputted case has already tested positive
            if positivecase not in positive_cases_keys:
                positive_cases_keys.append(positivecase) #add case to positive case list
                close_contacts(positivecase) #print close contacts of this case
                    
                print("Positive Cases: ")
                print(', '.join(positive_cases_keys)) #print all positive cases

                cont = showCloseContacts(app, graphWindow)

                if cont == 'y':
                    closeWindow()
                    newcase(app, newCaseWindow) #recursive call to continue adding new cases 
                elif cont == 'n':
                    closeWindow()
                    exit
                else:
                    showWarning('Please click Yes or No only.')

            else:
                showWarning("Target is already positive.")
        # except:
        #     print("NRIC does not exist.")
        #     newcase()

newcase(app, newCaseWindow)


# For iterating through positive cases and assigning close contacts to each.
# Once filtered by Hady's contactTrace() function which returns close contact array.

        
# digraphEdges = [] # Edges of each positive case

# Print positive case's CloseContactList by key

# for i in positive_cases_keys:
#     print("Close Contacts:")
#     digraphEdges.append(positive_cases_dict[i].printList(i))


# def creategraph(): 
#     d = graphviz.Digraph()
#     d.attr(size='10,10')

#     for i in digraphEdges:
#         for j in i:
#             d.edge(j[0],j[1])

#     d.render('digraph', format='png', view=False) 

# creategraph()

# graphWindow = QMainWindow()

# def showCloseContacts(app, graphWindow):
#     graphWindow.setWindowTitle("DiGraph")
    
#     graphWindow.central_widget = QWidget()               
#     graphWindow.setCentralWidget(graphWindow.central_widget)  

#     lay = QVBoxLayout(graphWindow.central_widget)

#     shnLabel = QtWidgets.QLabel("SHN has been issued to close contacts")
    
#     graphPicLabel = QtWidgets.QLabel(graphWindow)
#     pixmap = QPixmap('digraph.png')
#     graphPicLabel.setPixmap(pixmap)
#     graphWindow.resize(pixmap.width(), pixmap.height())

#     lay.addWidget(shnLabel)
#     lay.addWidget(graphPicLabel)

#     addMoreOptionBtn = QPushButton(graphWindow)
#     addMoreOptionBtn.setText("Okay")
#     addMoreOptionBtn.adjustSize()
#     # addMoreOptionBtn.move(10,150)
#     addMoreOptionBtn.clicked.connect(showAddMoreWindow)

#     lay.addWidget(addMoreOptionBtn, alignment=QtCore.Qt.AlignRight)
#     graphWindow.show()

#     sys.exit(app.exec_())

# def showAddMoreWindow():
#     print("Button 1 clicked")
#     graphWindow.close()

# showCloseContacts(app, graphWindow)

def window():
    app =  QApplication(sys.argv)
    m = folium.Map(
        location=[1.2864, 103.8253], tiles='Stamen Toner', zoom_start=15
    )
    m = folium.Map(
        location=[1.3521, 103.8198],
        zoom_start=11,
        tiles='https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=sk.eyJ1IjoiZXpyYXllb3NodWEiLCJhIjoiY2tuN2I2Z2luMG1jdjJwcDltc2MyNndtaCJ9.iE8ZBMYNmhbNT4PbBMLZdw', 
        attr='Mapbox Control Room'
    )

    markers = [
        {
            "latlng": [1.2864, 103.8253],
            "markercolor": "blue",
            "radius": 15,
            "count": 10,
            "popup": "message here"
        },
        {
            "latlng": [1.2815, 103.8448],
            "markercolor": "blue",
            "radius": 15,
            "count": 15,
            "popup": "message peeps"
        }
    ]

    # for i in markers: 
    #     folium.Marker(i["latlng"], icon=DivIcon(
    #         icon_size=(150,36),
    #         icon_anchor=(7,20),
    #         html='<div style="font-size: 18pt; color : black">%s</div>' % i["count"],
    #     )).add_to(m)
    #     m.add_child(folium.CircleMarker(i["latlng"], radius=i["radius"]))

    
    p1 = [1.2864, 103.8253]
    m.add_child(folium.CircleMarker(
                            p1,
                            radius = 15,
                            popup="sdfdsds m",
                            fill=True, # Set fill to True
                            fill_color='#999999',
                            color = 'grey',
                            fill_opacity=0.7
    ))
    # folium.Marker(p1, icon=DivIcon(
    #         icon_size=(150,36),
    #         icon_anchor=(7,20),
    #         html='<div style="vertical-align: middle; font-size: 15pt; color :black">8</div>',
    #         )).add_to(m)
    # folium.Marker(p1, icon=DivIcon(
    #         icon_size=(150,36),
    #         icon_anchor=(7,20),
    #         html='<div style="vertical-align: middle; font-size: 15pt; color :black">8</div>',
    #         )).add_to(m)
    # m.add_child(folium.CircleMarker(p1, radius=20))

    # p2 = [1.2815, 103.8448]
    # folium.Marker(p2, icon=DivIcon(
    #         icon_size=(150,36),
    #         icon_anchor=(7,20),
    #         html='<div style="font-size: 15pt; color :black">2</div>',
    #         )).add_to(m)
    # m.add_child(folium.CircleMarker(p2, radius=15))

    win = QMainWindow()
    win.setWindowTitle("CSC1008 Group 5")

    win.central_widget = QWidget()               
    win.setCentralWidget(win.central_widget)   

    button1 = QPushButton(win)
    button1.setText("Show close contact list")
    button1.adjustSize()
    button1.move(64,32)
    # button1.clicked.connect(button1_clicked)


    button2 = QPushButton(win)
    button2.setText("Show cluster")
    button2.adjustSize()
    button2.move(64,64)
    button2.clicked.connect(button2_clicked)

    button3 = QPushButton(win)
    button3.setText("Show safe entry records")
    button3.adjustSize()
    button3.move(64,100)
    button3.clicked.connect(button3_clicked)

    button4 = QPushButton(win)
    button4.setText("Quit")
    button4.adjustSize()
    button4.move(64,132)
    button4.clicked.connect(button4_clicked)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QWebEngineView(win)
    w.setHtml(data.getvalue().decode())
    pixmap = QPixmap('digraph.png')
    # pixmap = pixmap.scaledToWidth(400)
    label1 = QtWidgets.QLabel(win)
    label1.setPixmap(pixmap)
    # label1.setScaledContents(True)
    label1.move(750,50)
    label1.resize(500,500)

    w.resize(640, 480)
    w.move(100,200)
    w.show()
    win.resize(1000,1000)

    win.showFullScreen()
    win.show()


    sys.exit(app.exec_())



    # absolutePath = Path('/dataset.xlsx').resolve()
    # os.system(f'start excel.exe "{absolutePath}"')

def button2_clicked():
    print("Button 2 clicked")  

def button3_clicked():
    print("Button 3 clicked")

def button4_clicked():
    print("Button 4 clicked")  

window()


# print(digraphEdges)

# print(blueTooth)