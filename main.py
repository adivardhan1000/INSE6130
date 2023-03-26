import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QLabel

pyQTfileName = "test_ui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(pyQTfileName)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.menu_button.clicked.connect(lambda: self.toggle_menu(250, True))
        self.Btn_1.clicked.connect(lambda: self.view_all('Display All Vulnerabilities'))
        self.Btn_2.clicked.connect(lambda: self.check('Check for Vulnerabilities'))
        self.Btn_3.clicked.connect(lambda: self.fix('Fix Any Vulnerability'))
        self.Btn_4.clicked.connect(lambda: self.add_new('Add New Vulnerability'))

    ## support from https://github.com/Wanderson-Magalhaes/Toggle_Burguer_Menu_Python_PySide2/blob/master/ui_functions.py
    def toggle_menu(self,maxWidth, enable):
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

    def view_all(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_2)
        self.page_2_label.setText(msg)

    def check(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_3)
        self.page_3_label.setText(msg)

    def fix(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_4)
        self.page_4_label.setText(msg)

    def add_new(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_5)
        self.page_5_label.setText(msg)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())