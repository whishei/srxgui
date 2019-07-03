import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import uic

form, base = uic.loadUiType('MainWindow.ui')

class MainWidget(base,form):

    def __init__(self):
        super(base, self).__init__()
        self.setupUi(self)
        self.submit.clicked.connect(self.changepage2)
        self.userdataform.clicked.connect(self.changepage1)

    def changepage2(self):
        self.stackedWidget.setCurrentIndex(1)

    def changepage1(self):
        self.stackedWidget.setCurrentIndex(0)

    def setdefault(self):
        if self.default_2.isChecked() == True:
            self.prop_num.setText('304923')
            self.prop_title.setText('Routine Setup and Testing for Beamline 5-ID')
            self.PI_lname.setText('Kiss')
            self.saf_num.setText('304072')
            self.cycle.setText('2019_cycle2')
        if self.default_2.isChecked() == False:
            self.prop_num.setText('')
            self.prop_title.setText('')
            self.PI_lname.setText('')
            self.saf_num.setText('')
            self.cycle.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())