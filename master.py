from pandas import read_excel
import pandas as pd
import numpy
import CloseContactList as cc
import graphviz

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QInputDialog, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import sys
import folium
import io

file_name = 'dataset_final_v2.xlsm'

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
warningWindow = QMainWindow()
newCaseWindow = QMainWindow()

def closeWindow():
    print("Button 1 clicked")
    graphWindow.close()

def showCloseContacts(app, graphWindow, nric):
    graphWindow.setWindowTitle(nric+"'s Close Contacts")

    graphWindow.central_widget = QWidget()               
    graphWindow.setCentralWidget(graphWindow.central_widget)  

    lay = QVBoxLayout(graphWindow.central_widget)

    shnLabel = QtWidgets.QLabel("SHN has been issued to "+nric+"'s close contacts.\nContinue adding new positive cases?")
    
    graphPicLabel = QtWidgets.QLabel(graphWindow)
    pixmap = QPixmap('digraph.png')
    graphPicLabel.setPixmap(pixmap)
    graphWindow.resize(pixmap.width(), pixmap.height())

    msg = QMessageBox(graphWindow)

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    lay.addWidget(graphPicLabel)
    lay.addWidget(shnLabel)
    lay.addWidget(msg, alignment=QtCore.Qt.AlignRight)

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

    positive_cases_dict[n] = cc.CloseContactList()

    for i in caseArr:
        data = pd.read_excel(file_name, sheet_name=i.data["nric"])
        op = data.drop_duplicates(subset=["NRIC"],keep="last", inplace=True)

        blueTooth = data[(data["BT-Strength(%)"] >= 90) & (data["Connection Time(s)"] > 300)]
        timePlace = df[(df["Check-in-date"]==i.data["checkInDate"]) & (df["Location"]==i.data["location"]) & (df["NRIC"]!=i.data["nric"])]
  
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

    digraphEdges.append(positive_cases_dict[n].edges(n))
    creategraph()

def showWarning(text):
    msgBox = QMessageBox(warningWindow)
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle('Oops!')
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('OK clicked')
        newcase(app, newCaseWindow)

def newcase(app, newCaseWindow):
    newCaseWindow.central_widget = QWidget()         
    newCaseWindow.setCentralWidget(newCaseWindow.central_widget)  

    dialog = QInputDialog(newCaseWindow)
    dialog.resize(QtCore.QSize(600, 300))
    dialog.setWindowTitle("CSC1008 TraceTogether")
    dialog.setLabelText("Enter new positive case:")
    dialog.setTextValue("S9573284R")
    dialog.setTextEchoMode(QLineEdit.Normal)
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        positivecase = dialog.textValue()
    else: 
        sys.exit()

    if positivecase is not None:
        #check here if positivecase is in dataset, if not return error msg
        #check if inputted case has already tested positive
        if positivecase not in positive_cases_keys:
            positive_cases_keys.append(positivecase) #add case to positive case list
            close_contacts(positivecase) #print close contacts of this case
                
            print("Positive Cases: ")
            print(', '.join(positive_cases_keys)) #print all positive cases

            cont = showCloseContacts(app, graphWindow, positivecase)

            if cont == 'y':
                closeWindow()
                newcase(app, newCaseWindow) #recursive call to continue adding new cases 
            elif cont == 'n':
                closeWindow()
                exit
            else:
                showWarning('Please click Yes or No only.')

        else:
            showWarning('The target is already positive.')

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

    win = QMainWindow()
    win.setWindowTitle("CSC1008 Group 5")

    win.central_widget = QWidget()               
    win.setCentralWidget(win.central_widget)   

    button1 = QPushButton(win)
    button1.setText("Show close contact list")
    button1.adjustSize()
    button1.move(64,32)

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
    label1 = QtWidgets.QLabel(win)
    label1.setPixmap(pixmap)
    label1.move(750,50)
    label1.resize(500,500)

    w.resize(640, 480)
    w.move(100,200)
    w.show()
    win.resize(1000,1000)

    win.showFullScreen()
    win.show()

    sys.exit(app.exec_())

def button2_clicked():
    print("Button 2 clicked")  

def button3_clicked():
    print("Button 3 clicked")

def button4_clicked():
    print("Button 4 clicked")  

def main():
    newcase(app, newCaseWindow)
    window()

if __name__ == "__main__":
    main()
