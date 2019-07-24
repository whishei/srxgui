import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from MainScreen_Helper import *
from Queue_Helper import GetQueue
import warnings
import datetime
import time


warnings.filterwarnings("ignore", message =  'Adding an axes using the same arguments as a previous axes currently reuses the earlier instance.  In a future version, a new instance will always be created and returned.  Meanwhile, this warning can be suppressed, and the future behavior ensured, by passing a unique label to each axes instance.')
#sys.tracebacklimit=0

form, base = uic.loadUiType('MainWindow.ui')

class MainWidget(base,form):

    def __init__(self):
        super(base, self).__init__()
        self.setupUi(self)
        self.submit.clicked.connect(self.changepage2)
        self.userdataform.clicked.connect(self.changepage1)
        self.start_scan.clicked.connect(self.plan1)
        self.pause_resume_scan.clicked.connect(self.Pause)
        self.abort_scan.clicked.connect(self.Abort)
        self.stop_scan.clicked.connect(self.Stop)
        self.run_queue.clicked.connect(self.RunQueue)
        self.plot_layover.stateChanged.connect(self.Plot1)
        self.plot_layover_2.stateChanged.connect(self.Plot2)
        self.plot_layover_3.stateChanged.connect(self.Plot3)
        ax1 = self.results.figure.add_subplot(111)
        ax2 = self.results_2.figure.add_subplot(111)
        ax3 = self.results_3.figure.add_subplot(111)
        self.plot_layover.setChecked(True)
        self.plot_layover_2.setChecked(True)
        self.plot_layover_3.setChecked(True)
        # setAxs(ax1, ax2, ax3)

    ######################## Graph Widgets #######################

    def rawgraph(self):
        self.stackedWidget_3.setCurrentIndex(1)

    def normalizedgraph(self):
        self.stackedWidget_3.setCurrentIndex(0)

    def countgraph(self):
        self.stackedWidget_3.setCurrentIndex(2)

    ###########################################################################################

    def Plot1(self):
        if self.plot_layover.isChecked():
            self.plot_layover_2.setChecked(True)
            self.plot_layover_3.setChecked(True)
            # ax1 = self.results.figure.add_subplot(111)
            # ax2 = self.results_2.figure.add_subplot(111)
            # ax3 = self.results_3.figure.add_subplot(111)
            # setAxs(ax1, ax2, ax3)
        else:
            self.plot_layover_2.setChecked(False)
            self.plot_layover.setChecked(False)
            self.plot_layover_3.setChecked(False)
            # ax1 = self.results.figure.clf()
            # ax2 = self.results_2.figure.clf()
            # ax3 = self.results_3.figure.clf()
            # ax1 = self.results.figure.add_subplot(111)
            # ax2 = self.results_2.figure.add_subplot(111)
            # ax3 = self.results_3.figure.add_subplot(111)
            # setAxs(ax1, ax2, ax3)

    def Plot2(self):
        if self.plot_layover_2.isChecked():
            self.plot_layover.setChecked(True)
            self.plot_layover_3.setChecked(True)
            # ax1 = self.results.figure.add_subplot(111)
            # ax2 = self.results_2.figure.add_subplot(111)
            # ax3 = self.results_3.figure.add_subplot(111)
            # setAxs(ax1, ax2, ax3)
        else:
            self.plot_layover_2.setChecked(False)
            self.plot_layover.setChecked(False)
            self.plot_layover_3.setChecked(False)
            # ax1 = self.results.figure.clf()
            # ax2 = self.results_2.figure.clf()
            # ax3 = self.results_3.figure.clf()
            # ax1 = self.results.figure.add_subplot(111)
            # ax2 = self.results_2.figure.add_subplot(111)
            # ax3 = self.results_3.figure.add_subplot(111)
            # setAxs(ax1, ax2, ax3)

    def Plot3(self):
        if self.plot_layover_3.isChecked():
            self.plot_layover_2.setChecked(True)
            self.plot_layover.setChecked(True)
            # ax1 = self.results.figure.add_subplot(111)
            # ax2 = self.results_2.figure.add_subplot(111)
            # ax3 = self.results_3.figure.add_subplot(111)
            # setAxs(ax1, ax2, ax3)
        else:
            self.plot_layover_2.setChecked(False)
            self.plot_layover.setChecked(False)
            # self.plot_layover_3.setChecked(False)
            # ax1 = self.results.figure.clf()
            # ax2 = self.results_2.figure.clf()
            # ax3 = self.results_3.figure.clf()
            # ax1 = self.results.figure.add_subplot(111)
            # ax2 = self.results_2.figure.add_subplot(111)
            # ax3 = self.results_3.figure.add_subplot(111)
            # setAxs(ax1, ax2, ax3)

    def changepage2(self):
        self.stackedWidget.setCurrentIndex(1)

    def changepage1(self):
        self.stackedWidget.setCurrentIndex(0)

    def Pause(self):
        try:
            RE.request_pause()
        except:
            w = QMessageBox.warning(self, 'Error Message',
                                    'TransitionError: Please do not try to Pause the scan before it Starts.')
    def Abort(self):
        try:
            RE.abort()
        except:
            w = QMessageBox.warning(self, 'Error Message',
                                    'TransitionError: Please do not try to Pause the scan before it Starts.')

    def Stop(self):
        try:
            RE.stop()
        except:
            w = QMessageBox.warning(self, 'Error Message',
                                    'TransitionError: Please do not try to Pause the scan before it Starts.')

    ##############################Calculates Scan Time ###################################
    def plan1(self):
        if self.tabWidget.currentIndex() == 0:
            if self.plot_layover.isChecked():
                ax1 = self.results.figure.add_subplot(111)
                ax2 = self.results_2.figure.add_subplot(111)
                ax3 = self.results_3.figure.add_subplot(111)
            else:
                ax1 = self.results.figure.clf()
                ax2 = self.results_2.figure.clf()
                ax3 = self.results_3.figure.clf()
                ax1 = self.results.figure.add_subplot(111)
                ax2 = self.results_2.figure.add_subplot(111)
                ax3 = self.results_3.figure.add_subplot(111)
            kwargs = collect_args(ax1, ax2, ax3)
            print (kwargs)
            if kwargs == 0:
                w = QMessageBox.warning(self, 'Error Message', 'You must save the scan before you can start.',
                                        QMessageBox.Ok)
            else:
                scan_sec = collect_secs()
                print (scan_sec)
                self.scan_time.setText(str(datetime.timedelta(seconds=round(scan_sec))))
                try:
                    RE(my_xanes(**kwargs))
                    erange = kwargs['e_range']
                    estep = kwargs['e_steps']
                    krange = kwargs['k_range']
                    kstep = kwargs['k_steps']
                    E0 = kwargs ['E_0']
                    acqtime = kwargs['dwell']
                    print ('RE(my_xanes(e_range =' + str(erange) + ', e_steps = ' + str(estep) + ', E_0 = ' + str(E0) + ', k_range = ' + str(krange) + ', k_steps = ' + str(kstep) +  ', dwell = ' + str(acqtime) + '))')
                except ValueError:
                    w = QMessageBox.warning(self, 'Error Message',
                                            'ValueError: Please check your ranges, may need to change mode before choosing element',
                                            QMessageBox.Ok)
                # except:
                #     w = QMessageBox.warning(self, 'Error Message', 'Unknown Error', QMessageBox.Ok)
        else:
            w = QMessageBox.warning(self, 'Error Message', 'Tab 2 is not yet set up.',
                                    QMessageBox.Ok)


    def RunQueue(self):
        queue = GetQueue()
        for i in range(len(queue)):
            if self.plot_layover.isChecked():
                ax1 = self.results.figure.add_subplot(111)
                ax2 = self.results_2.figure.add_subplot(111)
                ax3 = self.results_3.figure.add_subplot(111)
            else:
                ax1 = self.results.figure.clf()
                ax2 = self.results_2.figure.clf()
                ax3 = self.results_3.figure.clf()
                ax1 = self.results.figure.add_subplot(111)
                ax2 = self.results_2.figure.add_subplot(111)
                ax3 = self.results_3.figure.add_subplot(111)
            kwargs = (queue[i])
            kwargs['ax11'] = ax1
            kwargs['ax22'] = ax2
            kwargs['ax33'] = ax3
            RE(my_xanes(**kwargs))
            #time.sleep(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())