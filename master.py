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
from folium.features import DivIcon
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
    graphWindow.setWindowTitle("Close Contact Visualization")

    graphWindow.central_widget = QWidget()               
    graphWindow.setCentralWidget(graphWindow.central_widget)  

    lay = QVBoxLayout(graphWindow.central_widget)

    shnLabel = QtWidgets.QLabel("SHN has been issued to "+nric+"'s close contacts.\nContinue adding new positive cases?")
    shnLabel.setAlignment(QtCore.Qt.AlignCenter)
    graphPicLabel = QtWidgets.QLabel(graphWindow)
    pixmap = QPixmap('digraph.png')
    graphPicLabel.setPixmap(pixmap)
    graphWindow.resize(pixmap.width(), pixmap.height())

    msg = QMessageBox(graphWindow)
    msg.setText("<p align='left'>SHN has been issued to "+nric+"'s close contacts. Continue adding new positive cases?<br>")
    msg.setStyleSheet("width: "+str(pixmap.width()/2.5)+";")
    msg.setMinimumWidth(pixmap.width())
    # msg.setGeometry(0, 0, pixmap.width(), pixmap.height())

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    lay.addWidget(graphPicLabel, alignment=QtCore.Qt.AlignCenter)
    # lay.addWidget(shnLabel)
    lay.addWidget(msg, alignment=QtCore.Qt.AlignCenter)

    graphWindow.show()

    retval = msg.exec_()

    if retval == QMessageBox.Yes:
        return 'y'
    elif retval == QMessageBox.No:
        return 'n'

def createGraph(): 
    d = graphviz.Digraph()
    d.attr(size='10,10')

    for i in digraphEdges:
        for j in i:
            d.edge(j[0],j[1])

    d.render('digraph', format='png', view=False)

def findCloseContacts(n):
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
    createGraph()

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
    else: 
        sys.exit()

def submit(self):
    str = self.line_edit.text()
    # check str before doing anything with it!
    print(str)

def clear(self):
    print ("cleared")
    self.line_edit.setText("")

def newcase(app, newCaseWindow):
    newCaseWindow.central_widget = QWidget()         
    newCaseWindow.setCentralWidget(newCaseWindow.central_widget)  

    dialog = QInputDialog(newCaseWindow)
    dialog.resize(QtCore.QSize(600, 300))
    dialog.setWindowTitle("CSC1008 TraceTogether")
    dialog.setLabelText("Start contact tracing...\n\nEnter new positive case:")
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
            findCloseContacts(positivecase) #print close contacts of this case
                
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
            showWarning('The target is already positive. Continue adding other cases?')

win = QMainWindow()

def window():
    win.setWindowTitle("Close Contact Visualization")

    win.central_widget = QWidget()               
    win.setCentralWidget(win.central_widget)  

    lay = QVBoxLayout(win.central_widget)

    graphPicLabel = QtWidgets.QLabel(win)
    pixmap = QPixmap('digraph.png')
    graphPicLabel.setPixmap(pixmap)
    win.resize(pixmap.width(), pixmap.height())

    endedLabel = QtWidgets.QLabel("Pending results of swab tests for close contacts.")
    endedLabel.setAlignment(QtCore.Qt.AlignCenter)

    button4 = QPushButton(win)
    button4.setText("Show map")
    button4.adjustSize()
    button4.clicked.connect(show_map)

    win.resize(pixmap.width(),pixmap.height())

    lay.addWidget(endedLabel)
    lay.addWidget(graphPicLabel)
    lay.addWidget(button4, alignment=QtCore.Qt.AlignRight)
    win.show()

    sys.exit(app.exec_())

map_window = QMainWindow()

def show_map():
    win.close()
    map_window.setWindowTitle("Clusters")

    map_window.central_widget = QWidget()               
    map_window.setCentralWidget(map_window.central_widget)   

    m = folium.Map(
        location=[1.3521, 103.8198],
        zoom_start=11,
        tiles='https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=sk.eyJ1IjoiZXpyYXllb3NodWEiLCJhIjoiY2tuN2I2Z2luMG1jdjJwcDltc2MyNndtaCJ9.iE8ZBMYNmhbNT4PbBMLZdw', 
        attr='Mapbox Control Room'
    )

    # p1 = [1.2864, 103.8253]
    lat = []
    lon = []
    count = 0
    for i in positive_cases_keys:
        temp = df[df["NRIC"]==i]
        temp = temp.drop_duplicates(subset=["NRIC","Location"],keep='last')
        for j in temp.values:
            count = count + 1
            lat.append(j[6])
            lon.append(j[7])

    for i in range(len(lat)):
        p1 = [lat[i],lon[i]]
        folium.Marker(p1, icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(7,20),
            html='<div style="font-size: 15pt; color :black">2</div>',
        )).add_to(m)
        m.add_child(folium.CircleMarker(p1, radius=5+count))

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QWebEngineView(map_window)
    w.setHtml(data.getvalue().decode())

    w.resize(640, 480)
    w.move(0,0)
    w.show()
    map_window.resize(640,480)
    map_window.show()

def main():
    newcase(app, newCaseWindow)
    window()

if __name__ == "__main__":
    main()
