#The Metadata Collection Widget.

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import json

form, base = uic.loadUiType('Metadata.ui')

class Metadata(base,form):

    def __init__(self, parent = None):
        super(Metadata, self).__init__()
        self.setupUi(self)
        self.cycle.setText('2019_cycle2')
        self.save_metadata.clicked.connect(self.Saving)
        #Loads in the last saved set of data
        with open('testingjson.txt', 'r') as file:
            data = json.load(file)
            self.prop_num.setText(data['Metadata']['Proposition Number'])
            self.prop_title.setText(data['Metadata']['Proposition Title'])
            self.PI_lname.setText(data['Metadata']['PI Last Name'])
            self.saf_num.setText(data['Metadata']['SAF Number'])

    def setdefault(self):
        # Sets the defaults for the beamline
        if self.default_2.isChecked() == True:
            self.prop_num.setText('304923')
            self.prop_title.setText('Routine Setup and Testing for Beamline 5-ID')
            self.PI_lname.setText('Kiss')
            self.saf_num.setText('304072')

        if self.default_2.isChecked() == False:
            self.prop_num.setText('')
            self.prop_title.setText('')
            self.PI_lname.setText('')
            self.saf_num.setText('')

    def Saving(self):
        #Updates the .json file with the new metadata
        with open('testingjson.txt', 'r') as file:
            data = json.load(file)
            data['Metadata']['Proposition Title'] = self.prop_title.text()
            data['Metadata']['Proposition Number'] = self.prop_num.text()
            data['Metadata']['PI Last Name'] = self.PI_lname.text()
            data['Metadata']['SAF Number'] = self.saf_num.text()

        with open('testingjson.txt', 'w') as file:
            json.dump(data, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Metadata()
    w.show()
    sys.exit(app.exec_())


