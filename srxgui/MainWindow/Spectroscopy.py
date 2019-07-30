#Loading the Spectroscopy Tab

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType('Spectroscopy.ui')

class Spectroscopy(QtBaseClass, Ui_MainWindow):

    def __init__(self, parent = None):
        super(QtBaseClass, self).__init__()
        self.setupUi(self)

    ################### Accessing Element Index ##################

    def Index(self):
        if self.stackedWidget.currentIndex() == 1:
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.stackedWidget.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Spectroscopy()
    w.show()



