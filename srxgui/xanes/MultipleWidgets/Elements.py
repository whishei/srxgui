import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

Ui_MainWindow, QtBaseClass = uic.loadUiType('elements.ui')

class Elements(QtBaseClass, Ui_MainWindow):

    def __init__(self, parent = None):
        super(QtBaseClass, self).__init__()
        self.setupUi(self)
        f = open("elements.txt", 'r')
        s = f.read()
        self.elements.setText(s)
        f = open("edges.txt", 'r')
        s = f.read()
        self.edges.setText(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Elements()
    w.show()
    sys.exit(app.exec_())
