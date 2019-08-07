import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QInputDialog
from PyQt5 import uic

form4, base4 = uic.loadUiType('XRF_Editor.ui')

class XRF_Editor(base4, form4):
    def __init__(self, parent = None):
        super(base4, self).__init__()
        self.setupUi(self)
    #     self.Okay.clicked.connect(self.Edits)
    #
    # def Edits(self):
    #     xstart_changes = float(self.xstart.text())
    #     xstop_changes = float(self.xstop.text())
    #     xnum_changes = float(self.xnum.text())
    #     ystart_changes = float(self.ystart.text())
    #     ystop_changes = float(self.ystop.text())
    #     ynum_changes = float(self.ynum.text())
    #     XRF_Editor.close(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = XRF_Editor()
    w.show()
    sys.exit(app.exec_())