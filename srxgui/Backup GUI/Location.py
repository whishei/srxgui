#The Location Widget. Controls the point to begin spectroscopy

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from MainScreen_Helper import set_motors

Ui_MainWindow, QtBaseClass = uic.loadUiType('Location.ui')

class Location(QtBaseClass, Ui_MainWindow):

    def __init__(self, parent = None):
        super(QtBaseClass, self).__init__()
        self.setupUi(self)
        if self.location.isChecked():           #the motor is in the correct location
            self.x_motor.setDisabled(True)
            self.y_motor.setDisabled(True)
            self.z_motor.setDisabled(True)
        else:                                   #the motor must be moved
            self.x_motor.setDisabled(False)
            self.y_motor.setDisabled(False)
            self.z_motor.setDisabled(False)

    def motor(self):
        'Gets the coordinates for the point to move the motor to'
        x_motor = float(self.x_motor.text())
        y_motor = float(self.y_motor.text())
        z_motor = float(self.z_motor.text())
        set_motors(x_motor, y_motor, z_motor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Location()
    w.show()
    sys.exit(app.exec_())
