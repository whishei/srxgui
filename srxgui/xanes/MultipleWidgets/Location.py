import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from MainScreen_Helper import *
import json
from ophyd import (PseudoPositioner, PseudoSingle, EpicsMotor)
from ophyd import (Component as Cpt, Device)
from ophyd.pseudopos import (pseudo_position_argument, real_position_argument)
from ophyd.sim import SynSignal, SynAxis
from ophyd.positioner import SoftPositioner

Ui_MainWindow, QtBaseClass = uic.loadUiType('Location.ui')

class Location(QtBaseClass, Ui_MainWindow):

    def __init__(self, parent = None):
        super(QtBaseClass, self).__init__()
        self.setupUi(self)
        if self.location.isChecked():
            self.x_motor.setDisabled(True)
            self.y_motor.setDisabled(True)
            self.z_motor.setDisabled(True)
        else:
            self.x_motor.setDisabled(False)
            self.y_motor.setDisabled(False)
            self.z_motor.setDisabled(False)
            # with open('testingjson.txt') as f:
            #     data = json.load(f)
            #     # global x_motor, y_motor, z_motor, hf_stage
            #     # hf_stage = HFSampleStage(name='hf_stage')
            #     # x_motor = hf_stage.x #data['beamline']['Sample Stages']['Coarse X']
            #     # y_motor = hf_stage.y #data['beamline']['Sample Stages']['Coarse Y']
            #     # z_motor = hf_stage.z #data['beamline']['Sample Stages']['Coarse Z']

    def motor(self):
        x_motor = float(self.x_motor.text())
        y_motor = float(self.y_motor.text())
        z_motor = float(self.z_motor.text())
        set_motors(x_motor, y_motor, z_motor)
        # x_motor.set(float(self.x_motor.text()))
        # print(hf_stage.read())
    #
    # def ymotor(self):
    #     # y_motor.set(float(self.y_motor.text()))
    #     # print(hf_stage.read())
    #
    # def zmotor(self):
    #     # z_motor.set(float(self.z_motor.text()))
    #     # print(hf_stage.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Location()
    w.show()
    sys.exit(app.exec_())
