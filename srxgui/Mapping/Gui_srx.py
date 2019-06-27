import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolTip, QMessageBox
from PyQt5.QtCore import QCoreApplication
import datetime 
from PyQt5 import uic
import json
from bluesky.plans import scan, rel_scan
from ophyd.sim import det4, motor1, motor2

#limit

import numpy as np
from bluesky.plans import (scan, )
from bluesky.plan_stubs import (one_1d_step, kickoff, collect, complete,
                                abs_set, mv)

import bluesky.plan_stubs as bps


from bluesky.preprocessors import (stage_decorator,
                                   run_decorator, subs_decorator,
                                   monitor_during_decorator)
from ophyd.sim import NullStatus
from bluesky.callbacks import CallbackBase, LiveGrid
from ophyd import Device
import uuid
#import h5py
from collections import ChainMap
from ophyd.areadetector.filestore_mixins import resource_factory

#from hxntools.handlers import register
#register(db)



Ui_MainWindow, QtBaseClass = uic.loadUiType('MyGui.ui')
class MyApp(QMainWindow):
    
        def __init__(self):
            super(MyApp, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.scan.clicked.connect(self.Calculate_TheEstimatedScanTime)
            self.ui.setButton_x.clicked.connect(self.AssignStart)
            self.ui.setButton_y.clicked.connect(self.AssignStop)
            self.ui.scan.clicked.connect(self.mapscan)
            self.ui.scan.clicked.connect(self.Calculate_The_SteppingStepsize)
            self.ui.scan.clicked.connect(self.Calculate_The_SteppingNpts)
            self.ui.scan.clicked.connect(self.Calculate_The_FlyingExtent)
            self.ui.scan.clicked.connect(self.Calculate_The_SteppingExtent)
            self.ui.scan.clicked.connect(self.Calculate_The_FlyingStepsize)
            self.ui.scan.clicked.connect(self.Calculate_The_FlyingNpts)
            
            #self.ui.scan.clicked.connect(self.scan_and_fly_base)
            #Reading the Overhead per line, the Stepping and flying Motors  from the Json file "myJsonfile.json"
            with open ('myJsonfile.json') as json_data:
                
                data = json.load(json_data)
                overhead_ = data['XRF']['overhead']
                overhead_string = str(overhead_)
                
                flyingMotor = data['XRF']['Flying Motors']
                steppingMotor = data['XRF']['Stepping Motors']
                for items in flyingMotor:
                    x = flyingMotor[0]
                    y = steppingMotor[0]
                    z = flyingMotor[1]
                    a = steppingMotor[1]
                    if flyingMotor == x:
                        self.ui.y.setEnabled(True)

                    if flyingMotor == z:
                        self.ui.a.setDisabled(True)
                    self.ui.flyingMotor.addItem(items) 
               
                for item in  steppingMotor:
                    x = flyingMotor[0]
                    y = steppingMotor[0]
                    z = flyingMotor[1]
                    a = steppingMotor[1]
                    if steppingMotor == y:
                        self.ui.x.setDisabled(True)
                    if steppingMotor == a:
                        self.ui.z.setDisabled(True)
                    self.ui. steppingMotor.addItem(item)
        
            self.ui.overhead_.setText(overhead_string)
              
        def Calculate_The_FlyingStepsize(self):
            message = 'None'
            xstart = float(self.ui.xstartLineE.text())
            xstop = float(self.ui.xstopLineE.text())
            Xnpts = float(self.ui.XnptsLineE.text())
            if xstart < -40 or xstart >40:
                message = 'ERROR: X START RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif  xstop < -40 or xstop > 40:
                message = 'ERROR: X STOP RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif xstop < xstart:
                message = 'PLEASE CHECK YOUR RANGES.'
                
                self.ui.x.setText(message)
            else:
                xStepsize = ((xstop - xstart)/(Xnpts - 1))
                xStepsize_string = str(xStepsize)
                self.ui.xStepsize.setText(xStepsize_string)
                
            
        def  Calculate_The_FlyingNpts(self):
            XnptsLineE = 0
            xStepsize_string = '0'
            stepsize_x = float(xStepsize_string)
            stepsize_x = float(self.ui.xStepsize.text())
            xstart = float(self.ui.xstartLineE.text())
            xstop = float(self.ui.xstopLineE.text())
            if xstart < -40 or xstart >40:
                message = 'ERROR: X START RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif  xstop < -40 or xstop > 40:
                message = 'ERROR: X STOP RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif xstop < xstart:
                message ='PLEASE CHECK YOUR RANGES.'
                self.ui.x.setText(message)
            else:
                XnptsLineE = ((xstop - xstart)/(stepsize_x) + 1)
                XnptsLineE_string = str(XnptsLineE)
                self.ui.XnptsLineE.setText(XnptsLineE_string)
               
        def Calculate_The_SteppingStepsize(self):
            message = 'None'
            ystart = float(self.ui.ystartLineE.text())
            ystop = float(self.ui.ystopLineE.text())
            Ynpts = float(self.ui.YnptsLineE.text())
            if ystart < 0 or ystart >50:
                message = 'ERROR: Y START RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif  ystop < 0 or ystop > 50:
                message = 'ERROR: Y STOP RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif ystop < ystart:
                message = 'PLEASE CHECK YOUR RANGES.'
                self.ui.x.setText(message)
#             elif len(xstart)!= 0 and len
            else:
                yStepsize = ((ystop - ystart)/(Ynpts - 1))
                yStepsize_string = str(yStepsize)
                self.ui.yStepsize.setText(yStepsize_string)
                
        def Calculate_The_SteppingNpts(self):
            YnptsLineE = 0
            yStepsize_string = '0'
            stepsize_y = float(self.ui.yStepsize.text())
            ystart = float(self.ui.ystartLineE.text())
            ystop = float(self.ui.ystopLineE.text())
            if ystart < -50 or ystart >50:
                message = 'ERROR: Y START RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif  ystop < -50 or ystop > 50:
                message = 'ERROR: Y STOP RANGE IS NOT IN THE RANGE'
                self.ui.x.setText(message)
            elif ystop < ystart:
                message = 'PLEASE CHECK YOUR RANGES.'
                self.ui.x.setText(message)
            else:
                YnptsLineE = ((ystop - ystart)/(stepsize_y) + 1)
                YnptsLineE_string = str(YnptsLineE)
                self.ui.YnptsLineE.setText(YnptsLineE_string)
                
        def Calculate_TheEstimatedScanTime(self):
            
            #gettin the overhead from the json file (myJsonfile.json)
            with open ('myJsonfile.json') as json_data:
                data = json.load(json_data)
                overhead_ = data['XRF']['overhead']
                overhead_string = str(overhead_)
            self.ui.overhead_.setText(overhead_string)
            #Collecting values from different parameters.
            dwell = float(self.ui.Dwell_t.text())
            
            
#             overH = float(self.ui.overhead_txt.text())
            xstart = float(self.ui.xstartLineE.text())
            xstop = float(self.ui.xstopLineE.text())
            ystart = float(self.ui.ystartLineE.text())
            ystop = float(self.ui.ystopLineE.text())
            Xnpts = float(self.ui.XnptsLineE.text())
            Ynpts = float(self.ui.YnptsLineE.text())
            current = float(self.ui.current_txt_x.text())
            currenty = float(self.ui.current_txt_y.text())
            xStepsize = ((xstop - xstart)/(Xnpts - 1))
            xStepsize_string = str(xStepsize)
            self.ui.xStepsize.setText(xStepsize_string)
            yStepsize = ((ystop - ystart)/(Ynpts - 1))
            yStepsize_string = str(yStepsize)
            self.ui.yStepsize.setText(yStepsize_string)
            stepsize_x = float(xStepsize_string)
            stepsize_x = float(self.ui.xStepsize.text())
            stepsize_y = float(yStepsize_string)
            stepsize_y = float(self.ui.yStepsize.text())
            XnptsLineE = ((xstop - xstart)/(stepsize_x) + 1)
            YnptsLineE = ((ystop - ystart)/(stepsize_y) + 1)
            
             #calculating the total second whicch is the estimated scan time
            second = (XnptsLineE* YnptsLineE* dwell ) + (overhead_ * XnptsLineE)
             #converting the float estimated time to days, hours, minutes, second
            self.ui.EstimateScanTime.setText(str(datetime.timedelta(seconds = round(second))))

             #calculate the size (between stop and start)
                
        def Calculate_The_FlyingExtent(self):
            xstart = float(self.ui.xstartLineE.text())
            xstop = float(self.ui.xstopLineE.text())
#             ystart = float(self.ui.ystartLineE.text())
#             ystop = float(self.ui.ystopLineE.text())
            Xsize = (xstop - xstart)
            Xsize_string = str(Xsize)
            self.ui.Xsize.setText(Xsize_string)
        def Calculate_The_SteppingExtent(self):
            xstart = float(self.ui.xstartLineE.text())
            xstop = float(self.ui.xstopLineE.text())
            ystart = float(self.ui.ystartLineE.text())
            ystop = float(self.ui.ystopLineE.text())
            Xsize = (xstop - xstart)
            Xsize_string = str(Xsize)
            Ysize = (ystop - ystart)
            Ysize_string = str(Ysize)
            self.ui.Ysize.setText(Ysize_string)
            self.ui.Xsize.setText(Xsize_string)
            
#         RE(Scanner(xstart, xstop, Xnpts, ystart, ystop, Ynpts, dwell, Xsize, Ysize))
         
        def AssignStart(self):
            current = float(self.ui.current_txt_x.text())
            #currenty = float(self.ui.current_txt_y.text())
            current_string = str(current)
            #currenty_string = str(currenty)
            self.ui.xstartLineE.setText(current_string)
            self.ui.ystartLineE.setText(current_string)
        def AssignStop(self):
            #current = float(self.ui.current_txt_x.text())
            currenty = float(self.ui.current_txt_y.text())
            #current_string = str(current)
            currenty_string = str(currenty)
            self.ui.xstopLineE.setText(currenty_string)
            self.ui.ystopLineE.setText(currenty_string)
        def mapscan (self, **args):
             #motor1 = str(self.ui.p_txt_x.Text())
#             motor2=  str(self.ui.p_txt_y.Text())
#             for 'Fine X' in motor1 and 'Fine Y' in motor2:
            dets = [det4]
            xstart = float(self.ui.xstartLineE.text())
            xstop = float(self.ui.xstopLineE.text())
            ystart = float(self.ui.ystartLineE.text())
            ystop = float(self.ui.ystopLineE.text())
            Xnpts = float(self.ui.XnptsLineE.text())
            Ynpts = float(self.ui.YnptsLineE.text())
            dwell = float(self.ui.Dwell_t.text())
           #totalnpts = Xnpts * Ynpts
            #RE(scan(dets,
            #              motor1, xstart, xstop,  #scan motor1 from xstart to xstop
            #              motor2, ystart, ystop, #...while scanning motor2 from ystart yo ystop
            #              Xnpts))#...both in 11 steps

            RE(self.scan_and_fly_base(dets, xstart, xstop, Xnpts, ystart, ystop, Ynpts, dwell,
                              flying_zebra=None, xmotor=motor1, ymotor=motor2))

        def scan_and_fly_base(self, detectors, xstart, xstop, Xnpts, ystart, ystop, Ynpts, dwell, *,
                              flying_zebra, xmotor, ymotor,
                              delta=None, shutter=True, align=False,
                              md=None):
        #def scan_and_fly_base(self, **args):
            yield bps.sleep(1)
            print(xstop)




#      if __name__ == '__main__':
app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())      