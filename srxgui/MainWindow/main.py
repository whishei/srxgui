#The Complete GUI

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton
from PyQt5 import uic
from MainScreen_Helper import *
from Queue_Helper import GetQueue, SendIndex, set_up_xrf, GetscanSecs
import warnings
import datetime
from bluesky.callbacks.mpl_plotting import LiveGrid


#Needed to draw XRF maps
class DrawingLiveGrid(LiveGrid):
    def event(self, *args, **kwargs):
        ret = super().event(*args, **kwargs)
        self.ax.figure.canvas.draw_idle()
        return ret

#Blocks the matplotlib deprecation error and other unknown tracebacks
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
        xrf_ax = self.map_.figure.add_subplot(111)
        index = self.tabWidget.currentIndex()
        SendIndex(index)
        self.save_queue.clicked.connect(self.SaveQueue)

    ######################## Graph Widgets #######################

    def rawgraph(self):
        self.stackedWidget_3.setCurrentIndex(1)

    def normalizedgraph(self):
        self.stackedWidget_3.setCurrentIndex(0)

    def countgraph(self):
        self.stackedWidget_3.setCurrentIndex(2)

    ####################### Needed to determine XRF / Spectroscopy ######################

    def tabs(self):
        index = self.tabWidget.currentIndex()
        SendIndex(index)

    ############################# Spectroscopy Plot Layover #######################################

    def Plot1(self):
        if self.plot_layover.isChecked():
            self.plot_layover_2.setChecked(True)
            self.plot_layover_3.setChecked(True)

        else:
            self.plot_layover_2.setChecked(False)
            self.plot_layover.setChecked(False)
            self.plot_layover_3.setChecked(False)

    def Plot2(self):

        if self.plot_layover_2.isChecked():
            self.plot_layover.setChecked(True)
            self.plot_layover_3.setChecked(True)
        else:
            self.plot_layover_2.setChecked(False)
            self.plot_layover.setChecked(False)
            self.plot_layover_3.setChecked(False)

    def Plot3(self):
        if self.plot_layover_3.isChecked():
            self.plot_layover_2.setChecked(True)
            self.plot_layover.setChecked(True)

        else:
            self.plot_layover_2.setChecked(False)
            self.plot_layover.setChecked(False)


    ##################### Moving between the Metadata and the Scans ####################

    def changepage2(self):
        self.stackedWidget.setCurrentIndex(1)

    def changepage1(self):
        self.stackedWidget.setCurrentIndex(0)


    ######################## Pause, Resume, Abort, Stop ##############################

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

    ############################## Runs the Scans ###################################
    def plan1(self):

        if self.tabWidget.currentIndex() == 0:      #Spectroscopy Tab
            #Sets up the axs
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

            #Collecting the kwargs from the parameter widget
            kwargs = collect_args(ax1, ax2, ax3)
            if kwargs == 0:
                w = QMessageBox.warning(self, 'Error Message', 'You must save the scan before you can start.',
                                        QMessageBox.Ok)
            else:
                #Collects and displays estimated scan time
                scan_sec = collect_secs()
                self.scan_time.setText(str(datetime.timedelta(seconds=round(scan_sec))))
                #Running the scan
                try:
                    RE(my_xanes(**kwargs))
                    #Printing command
                    erange = kwargs['e_range']
                    estep = kwargs['e_steps']
                    krange = kwargs['k_range']
                    kstep = kwargs['k_steps']
                    E0 = kwargs ['E_0']
                    acqtime = kwargs['dwell']
                    print ('RE(my_xanes(e_range =' + str(erange) + ', e_steps = ' + str(estep) + ', E_0 = ' + str(E0) + ', k_range = ' + str(krange) + ', k_steps = ' + str(kstep) +  ', dwell = ' + str(acqtime) + '))')
                #Common Error
                except ValueError:
                    w = QMessageBox.warning(self, 'Error Message',
                                            'ValueError: Please check your ranges, may need to change mode before choosing element',
                                            QMessageBox.Ok)
                #Unknown Error
                # except:
                #     w = QMessageBox.warning(self, 'Error Message', 'Unknown Error', QMessageBox.Ok)


        else:      #XRF Scan
            #Collecting and displaying estimated scan time
            secs = Seconds_XRF()
            self.es_time.setText(str(datetime.timedelta(seconds=round(secs))))
            #Setting up graph for xrf
            self.map_.figure.clf()
            xrf_ax = self.map_.figure.add_subplot(111)
            xnum,ynum = NeedXandY()
            self.lg = lg = DrawingLiveGrid((xnum, ynum), 'noisy_det', ax=xrf_ax)
            #collecting plan and args
            pln, args = Collecting_XRF(lg)
            #Running scan
            RE(pln(*args))
            #Printing the command
            flymotor,stepmotor = ReadFlyandStep()
            if flymotor == 'Coarse X':
                print('RE(scan_and_fly(' + str(args) + '))')
            else:
                print('RE(y_scan_and_fly(' + str(args) + '))')


    ##################### Running the Queue #########################

    def RunQueue(self):
        queue = GetQueue()
        for i in range(len(queue)):
            try:     #Looking for a dictionary, if yes, Spectroscopy Scan

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

            except:     #XRF scan
                args = (queue[i])
                self.map_.figure.clf()
                xrf_ax = self.map_.figure.add_subplot(111)
                xnum = args[4]
                ynum = args[8]
                self.lg = lg = DrawingLiveGrid((xnum, ynum), 'noisy_det', ax=xrf_ax)
                pln = set_up_xrf(lg)
                RE(pln(*args))
        secs = GetscanSecs()
        self.queue_time.setText(str(datetime.timedelta(seconds=round(secs))))

    ########################### Saving Queue ####################

    def SaveQueue(self):
        queue = GetQueue()
        file = open("queue.txt", "w")
        file.write(str(queue))
        file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())