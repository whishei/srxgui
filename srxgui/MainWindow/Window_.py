import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QToolTip, QMessageBox
from PyQt5.QtCore import QCoreApplication
import datetime 
#print(datetime)
from PyQt5 import uic
import json
from MainScreen_Helper import SavingXRF
from bluesky.plans import scan, rel_scan
from ophyd.sim import det4, motor1, motor2
#print(datetime)
#limit

import numpy as np
from bluesky.plans import (scan, )
from bluesky.plan_stubs import (one_1d_step, kickoff, collect, complete,
                                abs_set, mv)
#print(datetime)
import bluesky.plan_stubs as bps
from bluesky.preprocessors import (stage_decorator,
                                   run_decorator, subs_decorator,
                                   monitor_during_decorator)
from ophyd.sim import NullStatus
# from bluesky.callbacks import CallbackBase, LiveGrid, LivePlot
from ophyd import Device
import uuid
# import h5py
from collections import ChainMap
from ophyd.areadetector.filestore_mixins import resource_factory
# from hxntools.handlers import register
# register(db)
from ophyd.sim import hw
from bluesky.plans import scan
#print(datetime)
from ophyd.sim import hw
from bluesky.run_engine import RunEngine
from databroker import temp_config, Broker
from bluesky.plans import fly
import bluesky.plans as bp
#print(datetime)
########################
from bluesky.plans import grid_scan
from ophyd.sim import det4, motor1, motor2

from bluesky.callbacks.mpl_plotting import LiveGrid
from bluesky.callbacks.mpl_plotting import LivePlot
#print(datetime)
from position import *
#print(datetime)
# from scan_and_fly91 import *
#Fin limit
Ui_Widget, QtBaseClass = uic.loadUiType('XRFmappingGui.ui')
#print(datetime)

class DrawingLiveGrid(LiveGrid):
    def event(self, *args, **kwargs):
        ret = super().event(*args, **kwargs)
        self.ax.figure.canvas.draw_idle()
        return ret

class Window_(QtBaseClass,Ui_Widget):

    def __init__(self, parent = None):
        super(QtBaseClass, self).__init__()
        self.setupUi(self)
        self.save_xrf.clicked.connect(self.control)
        self.save_xrf.clicked.connect(self.calctheExtent_x)
        self.save_xrf.clicked.connect(self.calctheExtent_y)
        self.save_xrf.clicked.connect(self.calcFlyingNpts)
        self.save_xrf.clicked.connect(self.calcFlyingStepsize)
        self.save_xrf.clicked.connect(self.calcSteppingNpts)
        self.save_xrf.clicked.connect(self.calcSteppingStepsize)
        # self.save_xrf.clicked.connect(self.fly_and_scanX)
        # self.save_xrf.clicked.connect(self.collect_arg_kwargs)
        self.setstartbtn.clicked.connect(self.assignStartFromCurrent)
        self.setstopbtn.clicked.connect(self.assignStopFromCurrent)
        # self.save_xrf.clicked.connect(self.calculate_TheEstimatedScanTime)
        # self.save_xrf.clicked.connect(self.myplan)
        self.save_xrf.clicked.connect(self.saving_xrf)
        dwell = self.dwell_t.value()
        
        self.flying.activated[str].connect(self.control)
        self.stepping.activated[str].connect(self.control)

        with open ('myJsonfile.json') as json_data:
                data = json.load(json_data)
                overhead = data['XRF']['overhead']
                overhead_string = str(overhead)
                #Readong the Positionner from the Json file
                flyingMotor = data['XRF']['Flying Motors']
                steppingMotor = data['XRF']['Stepping Motors']
                courseXfly =data['XRF']['Flying Motors'][0]
                courseYfly =data['XRF']['Flying Motors'][1]
                courseXstep =data['XRF']['Stepping Motors'][0]
                courseYstep = data['XRF']['Stepping Motors'][1]
                courseZstep = data['XRF']['Stepping Motors'][2]
                rotationStep = data['XRF']['Stepping Motors'][3]

                #Flying Motor
                for items in flyingMotor:
                    self.flying.addItem(items) 
               #Stepping Motor
                for item in  steppingMotor:
                    self.stepping.addItem(item)

                self.overhead.setText(overhead_string)
        flymotor = self.flying.setCurrentIndex(0)
        stepmotor = self.stepping.setCurrentIndex(1)

        flymotor = self.flying.currentText()
        stepmotor = self.stepping.currentText()
        if flymotor == courseXfly and stepmotor == courseYstep:
            current = hf_stage.x.position
            current_string = str(current)
            currenty = hf_stage.y.position
            currenty_string = str(currenty)
            self.current_y_Label.setText(currenty_string)
            self.current_x_Label.setText(current_string)
        elif flymotor == courseYfly and stepmotor == courseXstep:
            currenty = hf_stage.y.position
            currenty_string = str(currenty)
            current = hf_stage.x.position
            current_string = str(current)
            self.current_x_Label.setText(currenty_string)
            self.current_y_Label.setText(current_string)
        elif flymotor == courseXstep and stepmotor == courseZstep:
            current = hf_stage.x.position
            current_string = str(current)
            currentz = hf_stage.z.position
            currentz_string = str(currentz)
            self.current_y_Label.setText(currentz_string)
            self.current_x_Label.setText(current_string)
        elif flymotor == courseXfly and stepmotor == rotationStep:
            current = hf_stage.x.position
            current_string = str(current)
            currentr = hf_stage.x.position
            currentr_string = str(currentr)
            self.current_y_Label.setText(currentr_string)
            self.current_x_Label.setText(current_string)
        elif flymotor == courseYfly and stepmotor == courseZstep:
            currenty = hf_stage.y.position
            currenty_string = str(currenty)
            currentz = hf_stage.z.position
            currentz_string = str(currentz)
            self.current_x_Label.setText(currenty_string)
            self.current_y_Label.setText(currentz_string)
        else:
            currenty = hf_stage.y.position
            currenty_string = str(currenty)
            currentr = hf_stage.x.position
            currentr_string = str(currentr)
            self.current_y_Label.setText(currentr_string)
            self.current_x_Label.setText(currenty_string)


    def control(self,message_):
            with open ('myJsonfile.json') as json_data:
                data = json.load(json_data)
                FlyingMotor = data['XRF']['Flying Motors']
                SteppingMotor = data['XRF']['Stepping Motors']
                courseXfly =data['XRF']['Flying Motors'][0]
                courseYfly =data['XRF']['Flying Motors'][1]
                courseXstep =data['XRF']['Stepping Motors'][0]
                courseYstep = data['XRF']['Stepping Motors'][1]
                courseZstep = data['XRF']['Stepping Motors'][2]
                rotationStep = data['XRF']['Stepping Motors'][3]

                #Checking the current value inside the flymotor and stepping motor  combobo
             
                flymotor = self.flying.currentText()
                stepmotor = self.stepping.currentText()
                message_ =  ''
                
                self.message.setText(message_)

            if flymotor == stepmotor:

                self.flyingStart.setDisabled(True)
                self.flyingStop.setDisabled(True)
                self.steppingStart.setDisabled(True)
                self.steppingStop.setDisabled(True)
                self.npts_x.setDisabled(True)
                self.npts_y.setDisabled(True)
                self.stepsize_y.setDisabled(True)
                self.stepsize_x.setDisabled(True)
                self.extent_x.setDisabled(True)
                self.extent_y.setDisabled(True)
                self.dwell_t.setDisabled(True)

                message_ =  'You cannot run the Scan with similar Motors'
                
                self.message.setText(message_)

            else:
                self.flyingStart.setDisabled(False)
                self.flyingStop.setDisabled(False)
                self.steppingStart.setDisabled(False)
                self.steppingStop.setDisabled(False)
                self.npts_x.setDisabled(False)
                self.npts_y.setDisabled(False)
                self.stepsize_y.setDisabled(False)
                self.stepsize_x.setDisabled(False)
                self.extent_x.setDisabled(False)
                self.extent_y.setDisabled(False)
                self.dwell_t.setDisabled(False)
                message_ =  ''
                
                self.message.setText(message_)


                if flymotor == courseXfly and stepmotor == courseYstep:
                    current = hf_stage.x.position
                    current_string = str(current)
                    currenty = hf_stage.y.position
                    currenty_string = str(currenty)
                    self.current_y_Label.setText(currenty_string)
                    self.current_x_Label.setText(current_string)
                elif flymotor == courseYfly and stepmotor == courseXstep:
                    currenty = hf_stage.y.position
                    currenty_string = str(currenty)
                    current = hf_stage.x.position
                    current_string = str(current)
                    self.current_x_Label.setText(currenty_string)
                    self.current_y_Label.setText(current_string)
                elif flymotor == courseXstep and stepmotor == courseZstep:
                    current = hf_stage.x.position
                    current_string = str(current)
                    currentz = hf_stage.z.position
                    currentz_string = str(currentz)
                    self.current_y_Label.setText(currentz_string)
                    self.current_x_Label.setText(current_string)
                elif flymotor == courseXfly and stepmotor == rotationStep:
                    current = hf_stage.x.position
                    current_string = str(current)
                    currentr = hf_stage.x.position
                    currentr_string = str(currentr)
                    self.current_y_Label.setText(currentr_string)
                    self.current_x_Label.setText(current_string)
                elif flymotor == courseYfly and stepmotor == courseZstep:
                    currenty = hf_stage.y.position
                    currenty_string = str(currenty)
                    currentz = hf_stage.z.position
                    currentz_string = str(currentz)
                    self.current_x_Label.setText(currenty_string)
                    self.current_y_Label.setText(currentz_string)
                else:
                    currenty = hf_stage.y.position
                    currenty_string = str(currenty)
                    currentr = hf_stage.x.position
                    currentr_string = str(currentr)
                    self.current_y_Label.setText(currentr_string)
                    self.current_x_Label.setText(currenty_string)

    
    def calctheExtent_x(self,extentx):
        xstart = self.flyingStart.value()
        xstop =self.flyingStop.value()
        if xstart < 0 or xstart >40:
            self.steppingStart.setDisabled(True)
            self.steppingStop.setDisabled(True)
            self.npts_x.setDisabled(True)
            self.npts_y.setDisabled(True)
            self.stepsize_y.setDisabled(True)
            self.stepsize_x.setDisabled(True)
            self.extent_x.setDisabled(True)
            self.extent_y.setDisabled(True)
            message_ = "WARNING: X Start is not in the range. Remember range must be from <0 to 40>"
            self.message.setText(message_)
            

        elif xstop < 0 or xstop > 40:
            self.steppingStart.setDisabled(True)
            self.steppingStop.setDisabled(True)
            self.npts_x.setDisabled(True)
            self.npts_y.setDisabled(True)
            self.stepsize_y.setDisabled(True)
            self.stepsize_x.setDisabled(True)
            self.extent_x.setDisabled(True)
            self.extent_y.setDisabled(True)
            message_ =  " "
            self.message.setText(message_)
            message_ =  "WARNING: X Stop is not in the range/n"+" Remember range must be from <0 to 40>"
            self.message.setText(message_)
            


        elif xstart > xstop or xstop < xstart:
            message_ =  " "
            self.message.setText(message_)
            message_ =  "WARNING: X Stop cannot be less than X Start"
            self.message.setText(message_)
            self.steppingStart.setDisabled(True)
            self.steppingStop.setDisabled(True)
            self.npts_x.setDisabled(True)
            self.npts_y.setDisabled(True)
            self.stepsize_y.setDisabled(True)
            self.stepsize_x.setDisabled(True)
            self.extent_x.setDisabled(True)
            self.extent_y.setDisabled(True)
        
        else:
            message_ =  " "
            self.message.setText(message_)
            self.steppingStart.setDisabled(False)
            self.steppingStop.setDisabled(False)
            self.npts_x.setDisabled(False)
            self.npts_y.setDisabled(False)
            self.stepsize_y.setDisabled(False)
            self.stepsize_x.setDisabled(False)
            self.extent_x.setDisabled(False)
            self.extent_y.setDisabled(False)
            extentx = xstop - xstart
            extentx_string = str(extentx)
            self.extent_x.setText(extentx_string)

    def calctheExtent_y(self,extenty):
        ystart = self.steppingStart.value()
        ystop =self.steppingStop.value()
        if ystart < 0 or ystart >50:
            message_ =  "WARNING: ""Y Start"" is not in the range. Remember range must be from <0 to 50>"
            self.message.setText(message_)

            self.flyingStart.setDisabled(True)
            self.flyingStop.setDisabled(True)
            self.npts_x.setDisabled(True)
            self.npts_y.setDisabled(True)
            self.stepsize_y.setDisabled(True)
            self.stepsize_x.setDisabled(True)
            self.extent_x.setDisabled(True)
            self.extent_y.setDisabled(True)
            
        elif ystop < 0 or ystop > 50:
            message_ = " "
            self.message.setText(message_)
            message_ =  "WARNING: ""Y Stop"" is not in the range/n"+" Remember range must be from <0 to 50>"
            self.message.setText(message_)

            self.flyingStart.setDisabled(True)
            self.flyingStop.setDisabled(True)
            self.npts_x.setDisabled(True)
            self.npts_y.setDisabled(True)
            self.stepsize_y.setDisabled(True)
            self.stepsize_x.setDisabled(True)
            self.extent_x.setDisabled(True)
            self.extent_y.setDisabled(True)
            
        elif ystart > ystop or ystop < ystart:
            message_ = " "
            self.message.setText(message_)
            message_ =  "WARNING: Y Stop cannot be less than Y Start"
            self.message.setText(message_)

            self.flyingStart.setDisabled(True)
            self.flyingStop.setDisabled(True)
            self.npts_x.setDisabled(True)
            self.npts_y.setDisabled(True)
            self.stepsize_y.setDisabled(True)
            self.stepsize_x.setDisabled(True)
            self.extent_x.setDisabled(True)
            self.extent_y.setDisabled(True)
           
        else:
            message_ = " "
            self.message.setText(message_)

            self.flyingStart.setDisabled(False)
            self.flyingStop.setDisabled(False)
            self.npts_x.setDisabled(False)
            self.npts_y.setDisabled(False)
            self.stepsize_y.setDisabled(False)
            self.stepsize_x.setDisabled(False)
            self.extent_x.setDisabled(False)
            self.extent_y.setDisabled(False)
            extenty = ystop - ystart
            extenty_string = str(extenty)
            self.extent_y.setText(extenty_string)
    def calcFlyingNpts(self,message_ = None,*args):
        xstart = self.flyingStart.value()
        xstop =self.flyingStop.value()
        stepsizex = self.stepsize_x.value()
        if stepsizex != 0:
            xnum = (((xstop -xstart)/stepsizex) + 1) 
            self.npts_x.setValue(xnum)
       
        else:
            message_ =  " "
            self.message.setText(message_)
            message_ =  "Warning: ""Flying Step Size"" cannot be less or equal 0"
            self.message.setText(message_)
        
    def calcFlyingStepsize(self,message_ =  None,*args):
        xstart = self.flyingStart.value()
        xstop =self.flyingStop.value()
        xnum = self.npts_x.value()
        # message_ =  " "
        # self.message.setText(message_)
        if xnum != 1:
            stepsizex = ((xstop -xstart)/(xnum - 1)) 
            self.stepsize_x.setValue(stepsizex)
            
        else:
            message_ = " "
            self.message.setText(message_)

            message_ =  "Warning: ""Flying Npts"" cannot be less or equal 1"
            self.message.setText(message_)
            
    def calcSteppingNpts(self,message_ =  None,*args):
        ystart = self.steppingStart.value()
        ystop =self.steppingStop.value()
        stepsizey = self.stepsize_y.value()
        if stepsizey != 0 or stepsizey < 0:
            ynum = ((ystop -ystart)/stepsizey) + 1
            self.npts_y.setValue(ynum)
            
        else:
            message_ = " "
            self.message.setText(message_)
            message_ =  "Warning: ""Stepping Step Size"" cannot be less or equal 0"
            self.message.setText(message_)
           
    def calcSteppingStepsize(self,message=None,*args):
        ystart = self.steppingStart.value()
        ystop =self.steppingStop.value()
        ynum = self.npts_y.value()
        # message_ = " "
        # self.message.setText(message_)
        if ynum != 1:
            stepsizey = ((ystop -ystart)/(ynum - 1)) 
            self.stepsize_y.setValue(stepsizey)
            
        else:
            message_ = " "
            self.message.setText(message_)
            message_ =  "Warning: ""Stepping Npts"" cannot be less or equal 1"
            self.message.setText(message_)
                

    def assignStartFromCurrent(self):
        current = float(self.current_x_Label.text())
        currenty = float(self.current_y_Label.text())
        self.flyingStart.setValue(current)
        self.steppingStart.setValue(currenty)
    def assignStopFromCurrent(self):
        current = float(self.current_x_Label.text())
        currenty = float(self.current_y_Label.text())
        self.flyingStop.setValue(current)
        self.steppingStop.setValue(currenty)
    def fly_and_scanX(self):
            with open ('myJsonfile.json') as json_data:
                data = json.load(json_data)
                FlyingMotor = data['XRF']['Flying Motors']
                SteppingMotor = data['XRF']['Stepping Motors']
                courseXfly =data['XRF']['Flying Motors'][0]
                courseYfly =data['XRF']['Flying Motors'][1]
                courseXstep =data['XRF']['Stepping Motors'][0]
                courseYstep = data['XRF']['Stepping Motors'][1]
                courseZstep = data['XRF']['Stepping Motors'][2]
                rotationStep = data['XRF']['Stepping Motors'][3]

                flymotor = self.flying.currentText()
                stepmotor = self.stepping.currentText()
                dwell = self.dwell_t.value()
                xstart = self.flyingStart.value()
                xstop =self.flyingStop.value()
                ystart = self.steppingStart.value()
                ystop =self.steppingStop.value()
                xnum = self.npts_x.value()
                ynum = self.npts_y.value()

            if flymotor == courseXfly:

                x_scan = ('RE(scan_and_fly( {} , {}, {}, {}, {}, {}, {} )'
                              .format(xstart, xstop, xnum, ystart, 
                                ystop, ynum,dwell))
                                    
                print (x_scan)
                print(" ")
            else:
                yscan = ('RE(y_scan_and_fly( {} , {}, {}, {}, {}, {}, {} )'
                    .format(ystart, ystop, ynum, xstart, xstop, xnum,dwell))
                print (yscan)
                print(" ")


    
    def calculate_TheEstimatedScanTime(self):
        with open ('myJsonfile.json') as json_data:
            data = json.load(json_data)
            overhead = data['XRF']['overhead']
            dwell = self.dwell_t.value()
            stop =self.steppingStop.value()
            xnum= self.npts_x.value()
            ynum= self.npts_y.value()

            second = ((xnum * ynum *dwell) + (overhead * ynum))
            self.es_time.setText(str(datetime.timedelta(seconds = round(second))))

    def saving_xrf(self):
        with open('myJsonfile.json') as json_data:
            data = json.load(json_data)
            xrf_overhead = data['XRF']['overhead']
        flymotor = self.flying.currentText()
        stepmotor = self.stepping.currentText()
        xrf_dwell = self.dwell_t.value()
        xstart = self.flyingStart.value()
        xstop = self.flyingStop.value()
        ystart = self.steppingStart.value()
        ystop = self.steppingStop.value()
        xnum = int(self.npts_x.value())
        ynum = int(self.npts_y.value())
        second = ((xnum * ynum *xrf_dwell) + (xrf_overhead * ynum))
        SavingXRF(xstart,xstop,xnum, ystart,ystop, ynum, xrf_dwell, second, flymotor, stepmotor)


    def collect_arg_kwargs(self):     
            dwell = self.dwell_t.value()
            xstart = self.flyingStart.value()
            xstop = self.flyingStop.value()
            ystart = self.steppingStart.value()
            ystop = self.steppingStop.value()
            xnum = int(self.npts_x.value())
            ynum = int(self.npts_y.value())
            detectors = [det4]
            # return scan, (detectors,motor1, xstart, xstop, xnum)
            self.map_.figure.clf()
            ax = self.map_.figure.add_subplot(111)
            self.lg = lg = DrawingLiveGrid((xnum, ynum), 'det4', ax=ax)
            import bluesky.preprocessors as bpp
            return bpp.subs_decorator([lg])(grid_scan), (detectors, motor1, xstart,xstop,xnum, motor2,ystart,ystop,ynum, False)

    def myplan(self):

        plan,args = self.collect_arg_kwargs()
        # RE(plan(*args ,num= None, per_step=None,md=None))
        # ax1 = self.ui.map_.figure.add_subplot(111)
        # RE(plan(*args),LiveGrid((15, 15), 'det4', ax = ax1))
        # plan,args= self.collect_arg_kwargs()

        RE(plan(*args))
        # RE(plan(*args),LivePlot('det4', 'motor1', ax = ax1))



if __name__ == '__main__':
#     import sys
#print(datetime)
#app = QApplication(sys.argv)
    window = Window_()
    window.show()
#sys.exit(app.exec_())
#print(datetime)