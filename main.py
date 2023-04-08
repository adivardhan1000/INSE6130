import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton, QFileDialog
from PyQt5.QtCore import Qt
import pandas as pd
import json
import os

pyQTfileName = "test_ui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(pyQTfileName)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.radioButtons = []
        self.menu_button.clicked.connect(lambda: self.toggle_menu(250, True))
        self.Btn_1.clicked.connect(lambda: self.navigate_to_view_all('Display All Vulnerabilities'))
        self.Btn_3.clicked.connect(lambda: self.navigate_to_fix('Available Fixes'))
        self.Btn_4.clicked.connect(lambda: self.navigate_to_add_new('Add New Vulnerability'))
        self.Btn_fix.clicked.connect(lambda: self.fix_vulnerability())
    ## support from https://github.com/Wanderson-Magalhaes/Toggle_Burguer_Menu_Python_PySide2/blob/master/ui_functions.py

    def toggle_menu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def navigate_to_view_all(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_2)
        self.page_2_label.setText(msg)

        # Import data
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        cve_row = cve.shape[0]
        cve_col = cve.shape[1]

        # Set table
        self.Table_Cve.setColumnCount(cve_col)
        self.Table_Cve.setRowCount(cve_row)
        self.Table_Cve.setHorizontalHeaderLabels(cve.columns.values)
        self.Table_Cve.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        font = self.Table_Cve.horizontalHeader().font()
        font.setBold(True)
        self.Table_Cve.horizontalHeader().setFont(font)
        # Add data into the table
        for i in range(len(cve)):
            for j in range(len(cve.columns)):
                item = QTableWidgetItem(str(cve.iloc[i, j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.Table_Cve.setItem(i, j, item)

    def navigate_to_fix(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_4)
        self.page_4_label.setText(msg)
        ## create new button if new was added
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        cve_names = cve.loc[:, 'CVE'].tolist()
        print(cve_names)
        self.radioButtons = self.show_all_radio_buttons(cve_names)

    def navigate_to_add_new(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_5)
        self.page_5_label.setText(msg)

        # Button action
        self.btn_browser.clicked.connect(self.File_Add)
        self.btn_cve_add.clicked.connect(self.Cve_Add)


    def File_Add(self):
        # choose a file
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'python files (*.py)')
        # split file path -> only file name
        fnamelist = fname[0].split('/')
        # set button text as file name
        self.btn_browser.setText(fnamelist[len(fnamelist)-1])


    def Cve_Add(self):
        # Get attributes fo new cve
        NewName = self.cve_name.toPlainText()
        NewDesc = self.cve_description.toPlainText()
        NewCVSS = float(self.cve_cvss.toPlainText())
        NewLink = self.cve_link.toPlainText()
        NewScript = self.btn_browser.text()

        # Store as dict
        NewDataDict = dict(CVE=NewName,
                    Description=NewDesc,
                    CVSS=NewCVSS,
                    Link=NewLink,
                    Script=NewScript)

        # update json file
        with open('test_data.json', 'r') as f:
            OldData = json.load(f)
        if len(OldData) > 1:
            OldData.append(NewDataDict)
        else:
            OldData = list(OldData)
        with open('test_data.json', 'w') as f_new:
            json.dump(OldData, f_new)
        self.outstate.setStyleSheet('color: rgb(255,255,255)')
        self.outstate.setPlainText('Success!')

    def fix_vulnerability(self):
        # Import data
        print('calling new function')
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        cve_row = cve.shape[0]
        cve_col = cve.shape[1]
        msgbox = QMessageBox()
        msg = ''
        description = ''
        str_val = ' '
        for i, radioButton in enumerate(self.radioButtons):
            if radioButton.isChecked():
                msg = radioButton.text()
                val = cve.loc[cve['CVE'] == msg, 'Script'].iloc[0]
                description = cve.loc[cve['CVE'] == msg, 'Description'].iloc[0]
                str_val = str(val)
                print(str_val)
                break
        msgbox.setText(description)
        msgbox.setInformativeText("Do you want to proceed with fixing this vulnerability?");
        msgbox.setStandardButtons(msgbox.Ok | msgbox.Cancel);
        msgbox.setWindowTitle('Description')
        ##msgbox.setDefaultButton(msgbox.Ok);
        ret = msgbox.exec_()

        if ret == int(msgbox.Ok):
            print('user clicked ok to execute ' + str_val)
            os.system("python3 "+ str_val) #invoke .py file to fix
        else:
            print('user clicked cancel')

    def show_all_radio_buttons(self, cve_names):
        radio_buttons = []
        for i, name in enumerate(cve_names):
            ay = i*50+50
            button = QRadioButton(name, self.page_4)
            #button.setFixedWidth(190)
            #button.setFixedHeight(60)
            button.setGeometry(QtCore.QRect(0, ay, 190, 50))
            button.setStyleSheet('color: rgb(255,255,255)')
            button.show()
            radio_buttons.append(button)
        return radio_buttons


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
