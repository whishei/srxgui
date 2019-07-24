import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
from PyQt5 import uic
from MainScreen_Helper import *
import datetime
import warnings

#Ui_MainWindow, QtBaseClass = uic.loadUiType('MainScreen.ui')
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


        #self.start_scan.clicked.connect(self.CalculateTime)
    #     self.plot_layover.stateChanged.connect(self.Plot1)
    #     self.plot_layover_2.stateChanged.connect(self.Plot2)
    #     self.plot_layover_3.stateChanged.connect(self.Plot3)
    #     ax1 = self.results.figure.add_subplot(111)
    #     ax2 = self.results_2.figure.add_subplot(111)
    #     ax3 = self.results_3.figure.add_subplot(111)
    #     setAxs(ax1, ax2, ax3)
    #
    # ################### Accessing Element Index ##################
    #
    # def Index(self):
    #     if self.stackedWidget.currentIndex() == 1:
    #         self.stackedWidget.setCurrentIndex(0)
    #     else:
    #         self.stackedWidget.setCurrentIndex(1)
    #
    # ######################## Graph Widgets #######################
    #
    # def rawgraph(self):
    #     self.stackedWidget_2.setCurrentIndex(1)
    #
    # def normalizedgraph(self):
    #     self.stackedWidget_2.setCurrentIndex(0)
    #
    # def countgraph(self):
    #     self.stackedWidget_2.setCurrentIndex(2)
    #
    # ###########################################################################################
    #
    # def Plot1(self):
    #     if self.plot_layover.isChecked():
    #         self.plot_layover_2.setChecked(True)
    #         self.plot_layover_3.setChecked(True)
    #         ax1 = self.results.figure.add_subplot(111)
    #         ax2 = self.results_2.figure.add_subplot(111)
    #         ax3 = self.results_3.figure.add_subplot(111)
    #         setAxs(ax1, ax2, ax3)
    #     else:
    #         self.plot_layover_2.setChecked(False)
    #         self.plot_layover.setChecked(False)
    #         self.plot_layover_3.setChecked(False)
    #         ax1 = self.results.figure.clf()
    #         ax2 = self.results_2.figure.clf()
    #         ax3 = self.results_3.figure.clf()
    #         ax1 = self.results.figure.add_subplot(111)
    #         ax2 = self.results_2.figure.add_subplot(111)
    #         ax3 = self.results_3.figure.add_subplot(111)
    #         setAxs(ax1, ax2, ax3)
    #
    # def Plot2(self):
    #     if self.plot_layover_2.isChecked():
    #         self.plot_layover.setChecked(True)
    #         self.plot_layover_3.setChecked(True)
    #         ax1 = self.results.figure.add_subplot(111)
    #         ax2 = self.results_2.figure.add_subplot(111)
    #         ax3 = self.results_3.figure.add_subplot(111)
    #         setAxs(ax1, ax2, ax3)
    #     else:
    #         self.plot_layover_2.setChecked(False)
    #         self.plot_layover.setChecked(False)
    #         self.plot_layover_3.setChecked(False)
    #         ax1 = self.results.figure.clf()
    #         ax2 = self.results_2.figure.clf()
    #         ax3 = self.results_3.figure.clf()
    #         ax1 = self.results.figure.add_subplot(111)
    #         ax2 = self.results_2.figure.add_subplot(111)
    #         ax3 = self.results_3.figure.add_subplot(111)
    #         setAxs(ax1, ax2, ax3)
    #
    # def Plot3(self):
    #     if self.plot_layover_3.isChecked():
    #         self.plot_layover_2.setChecked(True)
    #         self.plot_layover.setChecked(True)
    #         ax1 = self.results.figure.add_subplot(111)
    #         ax2 = self.results_2.figure.add_subplot(111)
    #         ax3 = self.results_3.figure.add_subplot(111)
    #         setAxs(ax1, ax2, ax3)
    #     else:
    #         self.plot_layover_2.setChecked(False)
    #         self.plot_layover.setChecked(False)
    #         self.plot_layover_3.setChecked(False)
    #         ax1 = self.results.figure.clf()
    #         ax2 = self.results_2.figure.clf()
    #         ax3 = self.results_3.figure.clf()
    #         ax1 = self.results.figure.add_subplot(111)
    #         ax2 = self.results_2.figure.add_subplot(111)
    #         ax3 = self.results_3.figure.add_subplot(111)
    #         setAxs(ax1, ax2, ax3)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Spectroscopy()
    w.show()
    #sys.exit(app.exec_())


