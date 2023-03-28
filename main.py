import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QLabel, QMessageBox

pyQTfileName = "test_ui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(pyQTfileName)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.menu_button.clicked.connect(lambda: self.toggle_menu(250, True))
        self.Btn_1.clicked.connect(lambda: self.navigate_to_view_all('Display All Vulnerabilities with \n Description and CVE link, May be add\n CVSS score too'))
        self.Btn_2.clicked.connect(lambda: self.navigate_to_check('Check for Vulnerabilities'))
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

    def navigate_to_check(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_3)
        self.page_3_label.setText(msg)

    def navigate_to_fix(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_4)
        self.page_4_label.setText(msg)

    def navigate_to_add_new(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_5)
        self.page_5_label.setText(msg)

    def fix_vulnerability(self):
        msgbox = QMessageBox();
        msg =''
        if self.radioButton_1.isChecked():
            msg = self.radioButton_1.text()
        elif self.radioButton_2.isChecked():
            msg = self.radioButton_2.text()
        elif self.radioButton_3.isChecked():
            msg = self.radioButton_3.text()
        elif self.radioButton_4.isChecked():
            msg = self.radioButton_4.text()
        elif self.radioButton_5.isChecked():
            msg = self.radioButton_5.text()
        msgbox.setText('Attempted to fix '+msg)
        msgbox.exec_()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())