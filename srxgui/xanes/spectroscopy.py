import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import numpy
import xraylib
import math
from Helper import *
import datetime
import json
#########Simulating Plans
from ophyd.sim import det, motor
from bluesky.plans import count, scan, rel_scan, list_scan, grid_scan, spiral
from bluesky.simulators import plot_raster_path
from bluesky.callbacks.mpl_plotting import LivePlot
from PyQt5.QtGui import QIcon, QPixmap


Ui_MainWindow, QtBaseClass = uic.loadUiType('xanes.ui')


class spectroscopy(QtBaseClass, Ui_MainWindow):

    global element
    element = 0

    def __init__(self):
        super(QtBaseClass, self).__init__()
        #self = Ui_MainWindow()
        self.setupUi(self)
        self.start_scan.clicked.connect(self.CalculateTime)
        #self.start_scan.clicked.connect(self.plan1)
        self.index.clicked.connect(self.page2)
        self.index2.clicked.connect(self.page1)
        self.index3.clicked.connect(self.page1)
        self.choice.activated[str].connect(self.onActivated)
        self.edge.activated[str].connect(self.onChanged)
        self.normalized2.clicked.connect(self.normalizedgraph)
        self.normalized3.clicked.connect(self.normalizedgraph)
        self.raw1.clicked.connect(self.rawgraph)
        self.raw3.clicked.connect(self.rawgraph)
        self.count1.clicked.connect(self.countgraph)
        self.count2.clicked.connect(self.countgraph)


    ##################### Regions ########################

    def regions(self):
        '''
        :signal: set number of regions
        :return: disables/enables regions
        '''
        regions = int(self.num_regions.text())
        if regions == 1 or regions == 2 or regions == 3 or regions == 4:
            self.xafs3_start.setDisabled(True)
            self.xafs3_stop.setDisabled(True)
            self.xafs3_step.setDisabled(True)
            self.xafs3_npts.setDisabled(True)
            self.xafs3_dwell.setDisabled(True)
            self.xafs3_start.setRange(0,0)
            self.xafs3_stop.setRange(0,0)
            if regions == 2 or regions == 3 or regions == 4:
                self.xanes_start.setEnabled(True)
                self.xanes_stop.setEnabled(True)
                self.xanes_step.setEnabled(True)
                self.xanes_npts.setEnabled(True)
                self.xanes_dwell.setEnabled(True)
                self.xanes_start.setRange(-50,50)
                self.xanes_stop.setRange(-50,50)
                if regions == 3 or regions == 4:
                    self.xafs1_start.setEnabled(True)
                    self.xafs1_stop.setEnabled(True)
                    self.xafs1_step.setEnabled(True)
                    self.xafs1_npts.setEnabled(True)
                    self.xafs1_dwell.setEnabled(True)
                    self.xafs1_start.setRange(-50,50)
                    self.xafs1_stop.setRange(-50,50)
                    if regions == 4:
                        self.xafs2_start.setEnabled(True)
                        self.xafs2_stop.setEnabled(True)
                        self.xafs2_step.setEnabled(True)
                        self.xafs2_npts.setEnabled(True)
                        self.xafs2_dwell.setEnabled(True)
                        self.xafs2_start.setRange(-50,50)
                        self.xafs2_stop.setRange(-50,50)
        if regions == 1 or regions == 2 or regions == 3:
            self.xafs2_start.setDisabled(True)
            self.xafs2_stop.setDisabled(True)
            self.xafs2_step.setDisabled(True)
            self.xafs2_npts.setDisabled(True)
            self.xafs2_dwell.setDisabled(True)
            self.xafs2_start.setRange(0,0)
            self.xafs2_stop.setRange(0,0)
        if regions == 1 or regions == 2:
            self.xafs1_start.setDisabled(True)
            self.xafs1_stop.setDisabled(True)
            self.xafs1_step.setDisabled(True)
            self.xafs1_npts.setDisabled(True)
            self.xafs1_dwell.setDisabled(True)
            self.xafs1_start.setRange(0,0)
            self.xafs1_stop.setRange(0,0)
        if regions == 1:
            self.xanes_start.setDisabled(True)
            self.xanes_stop.setDisabled(True)
            self.xanes_step.setDisabled(True)
            self.xanes_npts.setDisabled(True)
            self.xanes_dwell.setDisabled(True)
            self.xanes_start.setRange(0,0)
            self.xanes_stop.setRange(0,0)
        if regions == 5:
            self.xafs3_start.setEnabled(True)
            self.xafs3_stop.setEnabled(True)
            self.xafs3_step.setEnabled(True)
            self.xafs3_npts.setEnabled(True)
            self.xafs3_dwell.setEnabled(True)
            self.xafs3_start.setRange(-50,50)
            self.xafs3_stop.setRange(-50,50)


    ##################### Graph Widgets ##########################

    def rawgraph(self):
        self.stackedWidget_2.setCurrentIndex(1)

    def normalizedgraph(self):
        self.stackedWidget_2.setCurrentIndex(0)

    def countgraph(self):
        self.stackedWidget_2.setCurrentIndex(2)


    ################## Accessing Element Index ###################
    def page2(self):
        self.stackedWidget.setCurrentIndex(1)

    def page1(self):
        self.stackedWidget.setCurrentIndex(0)


    ########################### Absolute #######################

    def absolute(self):
        '''
        :signal: set mode
        :param: edge energy changed
        :return: for Absolute
                    sets all regions' start/stop values to edge energy
                 for Relative
                    sets all regions' start/stop values to 0
        '''
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        if mode == 'Absolute':
            self.pe_start.setValue(edge_energy)
            self.xanes_start.setValue(edge_energy)
            self.xafs1_start.setValue(edge_energy)
            self.xafs2_start.setValue(edge_energy)
            self.xafs3_start.setValue(edge_energy)
            self.pe_stop.setValue(edge_energy)
            self.xanes_stop.setValue(edge_energy)
            self.xafs1_stop.setValue(edge_energy)
            self.xafs2_stop.setValue(edge_energy)
            self.xafs3_stop.setValue(edge_energy)
        if mode == 'Relative':
            self.pe_start.setValue(0)
            self.xanes_start.setValue(0)
            self.xafs1_start.setValue(0)
            self.xafs2_start.setValue(0)
            self.xafs3_start.setValue(0)
            self.pe_stop.setValue(0)
            self.xanes_stop.setValue(0)
            self.xafs1_stop.setValue(0)
            self.xafs2_stop.setValue(0)
            self.xafs3_stop.setValue(0)


    ############################ Element Activated #########################

    def onActivated(self, text):
        '''
        :param text: (str) choice of element
        :param element: (int) element's atomic number (needed to obtain edge energy)
        :return: sets an element's edge energy and a suggested edge (as long as it is in the range 4.5 - 25)
        '''
        global element
        element = xraylib.SymbolToAtomicNumber(text)
        if xraylib.EdgeEnergy(element, xraylib.K_SHELL) >= 4.5 and xraylib.EdgeEnergy(element, xraylib.K_SHELL) <= 25:
            self.edge.setCurrentIndex(0)
            self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.K_SHELL))
        else:
            if xraylib.EdgeEnergy(element, xraylib.L1_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,xraylib.L1_SHELL) <= 25:
                self.edge.setCurrentIndex(1)
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L1_SHELL))
            else:
                if xraylib.EdgeEnergy(element, xraylib.L2_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,xraylib.L2_SHELL) <= 25:
                    self.edge.setCurrentIndex(2)
                    self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L2_SHELL))
                else:
                    if xraylib.EdgeEnergy(element, xraylib.L3_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,xraylib.L3_SHELL) <= 25:
                        self.edge.setCurrentIndex(3)
                        self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L3_SHELL))


    ############################# Edge Activated ###############################

    def onChanged(self, text):
        '''
        :param text: (str) choice of edge
        :return: sets an element's edge energy based off the chosen edge (as long as it is in the range 4.5 - 25)
        '''
        edge = str(text)
        if edge == 'K':
            if xraylib.EdgeEnergy(element, xraylib.K_SHELL) >= 4.5 and xraylib.EdgeEnergy(element, xraylib.K_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.K_SHELL))
            else:
                self.edge_energy.setValue(0)
        if edge == 'L1':
            if xraylib.EdgeEnergy(element, xraylib.L1_SHELL) >= 4.5 and xraylib.EdgeEnergy(element, xraylib.L1_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L1_SHELL))
            else:
                self.edge_energy.setValue(0)
        if edge == 'L2':
            if xraylib.EdgeEnergy(element, xraylib.L2_SHELL) >= 4.5 and xraylib.EdgeEnergy(element, xraylib.L2_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L2_SHELL))
            else:
                self.edge_energy.setValue(0)
        if edge == 'L3':
            if xraylib.EdgeEnergy(element, xraylib.L3_SHELL) >= 4.5 and xraylib.EdgeEnergy(element, xraylib.L3_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L3_SHELL))
            else:
                self.edge_energy.setValue(0)


    ##################### Stop Limits #########################
    def stoplimit(self):
        '''
        :param pe_start: (float) start of pre-edge region
        :param xanes_start: (float) start of xanes region
        :param xafs1_start: (float) start of xafs1 region
        :param xafs2_start: (float) start of xafs2 region
        :param xafs3_start: (float) start of xafs3 region
        :return: limits the stop of each region to be greater than the start
        '''
        pe_start = float(self.pe_start.text())
        xanes_start = float(self.xanes_start.text())
        xafs1_start = float(self.xafs1_start.text())
        xafs2_start = float(self.xafs2_start.text())
        xafs3_start = float(self.xafs3_start.text())
        if pe_start != 0:
            self.pe_stop.setRange(pe_start, 50)
        if xanes_start != 0:
            self.xanes_stop.setRange(xanes_start, 50)
        if xafs1_start != 0:
            self.xafs1_stop.setRange(xafs1_start, 50)
        if xafs2_start != 0:
            self.xafs2_stop.setRange(xafs2_start, 50)
        if xafs3_start != 0:
            self.xafs3_stop.setRange(xafs3_start, 50)


    ##################### Set Start ###########################
    def setstart(self):
        '''
        :param pe_stop: (float) stop of pre_edge region
        :param xanes_stop: (float) stop of xanes region
        :param xafs1_stop: (float) stop of xafs1 region
        :param xafs2_stop: (float) stop of xafs2 region
        :return: sets the start of the next region to be the previous of the past region (only a suggestion)
        '''
        pe_stop = float(self.pe_stop.text())
        xanes_stop = float(self.xanes_stop.text())
        xafs1_stop = float(self.xafs1_stop.text())
        xafs2_stop = float(self.xafs2_stop.text())
        if pe_stop != 0:
            self.xanes_start.setValue(pe_stop)
        if xanes_stop != 0:
            self.xafs1_start.setValue(xanes_stop)
        if xafs1_stop != 0:
            self.xafs2_start.setValue(xafs1_stop)
        if xafs2_stop != 0:
            self.xafs3_start.setValue(xafs2_stop)


############################## Dwell Time #####################################
    # Sets all dwell times to be the same based off of which one was changed

    def dwell1(self):
        '''
        :param dwell: (float) pre-edge dwell time
        :return: sets all other regions to pre-edge dwell
        '''
        dwell = float(self.pe_dwell.text())
        self.xanes_dwell.setValue(dwell)
        self.xafs1_dwell.setValue(dwell)
        self.xafs2_dwell.setValue(dwell)
        self.xafs3_dwell.setValue(dwell)

    def dwell2(self):
        '''
        :param dwell: (float) xanes dwell time
        :return: sets all other regions to xanes dwell
        '''
        dwell = float(self.xanes_dwell.text())
        self.pe_dwell.setValue(dwell)
        self.xafs1_dwell.setValue(dwell)
        self.xafs2_dwell.setValue(dwell)
        self.xafs3_dwell.setValue(dwell)

    def dwell3(self):
        '''
        :param dwell: (float) xafs1 dwell time
        :return: sets all other regions to xafs1 dwell
        '''
        dwell = float(self.xafs1_dwell.text())
        self.xanes_dwell.setValue(dwell)
        self.pe_dwell.setValue(dwell)
        self.xafs2_dwell.setValue(dwell)
        self.xafs3_dwell.setValue(dwell)

    def dwell4(self):
        '''
        :param dwell: (float) xafs2 dwell time
        :return: sets all other regions to xafs2 dwell
        '''
        dwell = float(self.xafs2_dwell.text())
        self.xanes_dwell.setValue(dwell)
        self.xafs1_dwell.setValue(dwell)
        self.pe_dwell.setValue(dwell)
        self.xafs3_dwell.setValue(dwell)

    def dwell5(self):
        '''
        :param dwell: (float) xafs3 dwell time
        :return: sets all other regions to xafs3 dwell
        '''
        dwell = float(self.xafs3_dwell.text())
        self.xanes_dwell.setValue(dwell)
        self.xafs1_dwell.setValue(dwell)
        self.xafs2_dwell.setValue(dwell)
        self.pe_dwell.setValue(dwell)


############################# Points ##################################
    #Requires helper function

    def pts(self):
        '''
        :param edge: (float) the edge energy
        :param mode: (str) chosen mode
        :param pe_step: (float) pre-edge region step
        :param xanes_step: (float) xanes region step
        :param xafs1_step: (float) xafs1 region step
        :param xafs2_step: (float) xafs2 region step
        :param xafs3_step: (float) xafs3 region step
        :param pe_start: (float) pre-edge region start
        :param pe_stop: (float) pre-edge region stop
        :param xanes_start: (float) xanes region start
        :param xanes_stop: (float) xanes region stop
        :param xafs1_start: (float) xafs1 region start
        :param xafs1_stop: (float) xafs1 region stop
        :param xafs2_start: (float) xafs2 region start
        :param xafs2_stop: (float) xafs2 region stop
        :param xafs3_start: (float) xafs3 region start
        :param xafs3_stop: (float) xafs3 region stop
        :return: solves for the number of points of every region based upon what parameters are supplied.
        '''
        edge = float(self.edge_energy.text())
        mode = self.mode.currentText()
        pe_step = float(self.pe_step.text())
        xanes_step = float(self.xanes_step.text())
        xafs1_step = float(self.xafs1_step.text())
        xafs2_step = float(self.xafs2_step.text())
        xafs3_step = float(self.xafs3_step.text())
        if pe_step != 0:
            if mode == 'Absolute':
                pe_start = float(self.pe_start.text())
                pe_stop = float(self.pe_stop.text())
            else:
                pe_start = edge + float(self.pe_start.text())
                pe_stop = edge + float(self.pe_stop.text())
            self.pe_npts.setValue(PTShelper(pe_start, pe_stop, pe_step))
        if xanes_step != 0:
            if mode == 'Absolute':
                xanes_start = float(self.xanes_start.text())
                xanes_stop = float(self.xanes_stop.text())
            else:
                xanes_start = edge + float(self.xanes_start.text())
                xanes_stop = edge + float(self.xanes_stop.text())
            self.xanes_npts.setValue(PTShelper(xanes_start, xanes_stop, xanes_step))
        if xafs1_step != 0:
            if mode == 'Absolute':
                xafs1_start = float(self.xafs1_start.text())
                xafs1_stop = float(self.xafs1_stop.text())
            else:
                xafs1_start = edge + float(self.xafs1_start.text())
                xafs1_stop = edge + float(self.xafs1_stop.text())
            self.xafs1_npts.setValue(PTShelper(xafs1_start, xafs1_stop, xafs1_step))
        if xafs2_step != 0:
            if mode == 'Absolute':
                xafs2_start = float(self.xafs2_start.text())
                xafs2_stop = float(self.xafs2_stop.text())
            else:
                xafs2_start = edge + float(self.xafs2_start.text())
                xafs2_stop = edge + float(self.xafs2_stop.text())
            self.xafs2_npts.setValue(PTShelper(xafs2_start, xafs2_stop, xafs2_step))
        if mode == 'Absolute':
            xafs3_start = float(self.xafs3_start.text())
            xafs3_stop = float(self.xafs3_stop.text())
        else:
            xafs3_start = edge + float(self.xafs3_start.text())
            xafs3_stop = edge + float(self.xafs3_stop.text())
        self.xafs3_npts.setValue(PTShelper(xafs3_start, xafs3_stop, xafs3_step))


    ########################### Steps ###################################
    #Requires helper function

    def steps(self):
        '''
        :param edge: (float) the edge energy
        :param mode: (str) chosen mode
        :param pe_npts: (int) pre-edge region number of points
        :param xanes_npts: (int) xanes region number of points
        :param xafs1_npts: (int) xafs1 region number of points
        :param xafs2_npts: (int) xafs2 region number of points
        :param xafs3_npts: (int) xafs3 region number of points
        :param pe_start: (float) pre-edge region start
        :param pe_stop: (float) pre-edge region stop
        :param xanes_start: (float) xanes region start
        :param xanes_stop: (float) xanes region stop
        :param xafs1_start: (float) xafs1 region start
        :param xafs1_stop: (float) xafs1 region stop
        :param xafs2_start: (float) xafs2 region start
        :param xafs2_stop: (float) xafs2 region stop
        :param xafs3_start: (float) xafs3 region start
        :param xafs3_stop: (float) xafs3 region stop
        :return: solves for the number of steps of every region based upon what parameters are supplied.
        '''
        edge = float(self.edge_energy.text())
        mode = self.mode.currentText()
        pe_npts = float(self.pe_npts.text())
        xanes_npts = float(self.xanes_npts.text())
        xafs1_npts = float(self.xafs1_npts.text())
        xafs2_npts = float(self.xafs2_npts.text())
        xafs3_npts = float(self.xafs3_npts.text())
        if pe_npts != 0:
            if mode == 'Absolute':
                pe_start = float(self.pe_start.text())
                pe_stop = float(self.pe_stop.text())
            else:
                pe_start = edge + float(self.pe_start.text())
                pe_stop = edge + float(self.pe_stop.text())
            self.pe_step.setValue(STEPShelper(pe_start,pe_stop,pe_npts))
        if xanes_npts != 0:
            if mode == 'Absolute':
                xanes_start = float(self.xanes_start.text())
                xanes_stop = float(self.xanes_stop.text())
            else:
                xanes_start = edge + float(self.xanes_start.text())
                xanes_stop = edge + float(self.xanes_stop.text())
            self.xanes_step.setValue(STEPShelper(xanes_start,xanes_stop,xanes_npts))
        if xafs1_npts != 0:
            if mode == 'Absolute':
                xafs1_start = float(self.xafs1_start.text())
                xafs1_stop = float(self.xafs1_stop.text())
            else:
                xafs1_start = edge + float(self.xafs1_start.text())
                xafs1_stop = edge + float(self.xafs1_stop.text())
            self.xafs1_step.setValue(STEPShelper(xafs1_start, xafs1_stop, xafs1_npts))
        if xafs2_npts != 0:
            if mode == 'Absolute':
                xafs2_start = float(self.xafs2_start.text())
                xafs2_stop = float(self.xafs2_stop.text())
            else:
                xafs2_start = edge + float(self.xafs2_start.text())
                xafs2_stop = edge + float(self.xafs2_stop.text())
            self.xafs2_step.setValue(STEPShelper(xafs2_start, xafs2_stop, xafs2_npts))
        if xafs3_npts != 0:
            if mode == 'Absolute':
                xafs3_start = float(self.xafs3_start.text())
                xafs3_stop = float(self.xafs3_stop.text())
            else:
                xafs3_start = edge + float(self.xafs3_start.text())
                xafs3_stop = edge + float(self.xafs3_stop.text())
            self.xafs3_step.setValue(STEPShelper(xafs3_start, xafs3_stop, xafs3_npts))


    ##############################Calculates Scan Time ###################################

    def CalculateTime(self):
        '''
        :param edge: (float) the edge energy
        :param mode: (str) chosen mode
        :param pe_step: (float) pre-edge region step
        :param xanes_step: (float) xanes region step
        :param xafs1_step: (float) xafs1 region step
        :param xafs2_step: (float) xafs2 region step
        :param xafs3_step: (float) xafs3 region step
        :param pe_start: (float) pre-edge region start
        :param pe_stop: (float) pre-edge region stop
        :param xanes_start: (float) xanes region start
        :param xanes_stop: (float) xanes region stop
        :param xafs1_start: (float) xafs1 region start
        :param xafs1_stop: (float) xafs1 region stop
        :param xafs2_start: (float) xafs2 region start
        :param xafs2_stop: (float) xafs2 region stop
        :param xafs3_start: (float) xafs3 region start
        :param xafs3_stop: (float) xafs3 region stop
        :param num_pts: (int) total number of points of the scan
        :param dwell: (float) dwell time for the scan (consistent throughout)
        :param total_overhead: (float)  read in from a json file
                                        the total overhead for the scan
        :return: solves for the predicted scan time
        '''
        edge = float(self.edge_energy.text())
        mode = self.mode.currentText()
        pe_start = float(self.pe_start.text())
        pe_stop = float(self.pe_stop.text())
        xanes_start = float(self.xanes_start.text())
        xanes_stop = float(self.xanes_stop.text())
        xafs1_start = float(self.xafs1_start.text())
        xafs1_stop = float(self.xafs1_stop.text())
        xafs2_start = float(self.xafs2_start.text())
        xafs2_stop = float(self.xafs2_stop.text())
        xafs3_start = float(self.xafs3_start.text())
        xafs3_stop = float(self.xafs3_stop.text())
        pe_step = float(self.pe_step.text())
        xanes_step = float(self.xanes_step.text())
        xafs1_step = float(self.xafs1_step.text())
        xafs2_step = float(self.xafs2_step.text())
        xafs3_step = float(self.xafs3_step.text())
        if mode == 'Relative':
            pe_start = edge + float(self.pe_start.text())
            pe_stop = edge + float(self.pe_stop.text())
        Erange(pe_start, pe_stop, pe_step)
        if xanes_start != 0 and xanes_stop != 0:
            if mode == 'Relative':
                xanes_start = edge + float(self.xanes_start.text())
                xanes_stop = edge + float(self.xanes_stop.text())
            Erange(xanes_start, xanes_stop, xanes_step)
        if xafs1_start != 0 and xafs1_stop != 0:
            if mode == 'Relative':
                xafs1_start = edge + float(self.xafs1_start.text())
                xafs1_stop = edge + float(self.xafs1_stop.text())
            Erange(xafs1_start, xafs1_stop, xafs1_step)
        if xafs2_start != 0 and xafs2_stop != 0:
            if mode == 'Relative':
                xafs2_start = edge + float(self.xafs2_start.text())
                xafs2_stop = edge + float(self.xafs2_stop.text())
            Erange(xafs2_start, xafs2_stop, xafs2_step)
        if xafs3_start != 0 and xafs3_stop != 0:
            if mode == 'Relative':
                xafs3_start = edge + float(self.xafs3_start.text())
                xafs3_stop = edge + float(self.xafs3_stop.text())
            Erange(xafs3_start, xafs3_stop,  xafs3_step)
        num_pts = getpts()
        dwell = float(self.pe_dwell.text())
        with open('testingjson.txt') as f:
            data = json.load(f)
            total_overhead = data['XAS']['overhead']
        scan_sec = num_pts * (dwell + total_overhead)
        self.scan_time.setText(str(datetime.timedelta(seconds=round(scan_sec))))
        self.results.setText(str(geterange()) + '\n' + str(getestep()))




###########################################################################################
    # The Scan Itself


    def collect_args(self):
        '''
        :return: xanes_plan: Running a XANES scan
        '''
        dets = [det]
        #plan = spiral(dets, motor1,motor2, x_start = float(self.pe_start.text()),y_start = float(self.pe_start.text()), x_range = float(self.pe_stop.text()), y_range = float(self.pe_stop.text()), dr = float(self.pe_step.text()), nth = float(self.pe_npts.text()))
        #return count, ([dets]), {'num': int(self.num_scans.text())}
        return scan, (dets, motor,float(self.pe_start.text()),  float(self.pe_stop.text())), {'num': float(self.pe_npts.text())}
        #return plot_raster_path, plan, {'x_motor': motor1, 'y_motor': motor2}
        #return xanes_plan, {'erange' : geterange().tolist(), 'estep' : getestep().tolist(), 'acqtime' : float(self.pe_dwell.text()), 'samplename' :str(self.sample_name.text()), 'filename' : str(self.file_name.text())}


    # Running  the scans
    # def plan1(self):
    #     '''
    #     :return: runs the xanes scan. Should change the erange, estep, and acqtime. Possibly move the motors if needed.
    #     '''
    #     pln, args, kwargs = self.collect_args()
    #     pixmap = LivePlot('det', 'motor')
    #     RE(pln(*args, **kwargs),pixmap)
    #     pixmap = QPixmap(pixmap)
    #     self.results.setPixmap(pixmap)
    #
    #     header = db[-1]
    #     string = str(header.table())
    #     self.results.setText(string)
        #  #RE(pln(*args, **kwargs))
        # #dets = [det]
        #
        # plan = spiral(dets, motor1, motor2, x_start=float(self.pe_start.text()),
        #               y_start=float(self.pe_start.text()), x_range=float(self.pe_stop.text()),
        #               y_range=float(self.pe_stop.text()), dr=float(self.pe_step.text()),
        #               nth=float(self.pe_npts.text()))
        # # plan = spiral([det], motor1, motor2, x_start=0.0, y_start=0.0, x_range=1.,
        # # y_range=1.0, dr=0.1, nth=10)
        # plot_raster_path(plan, 'motor1', 'motor2', probe_size=.01)
        #
        # #num = int(self.pe_npts.text())
        # #start = float(self.pe_start.text())
        # #stop = float(self.pe_stop.text())
        # #RE(xanes_plan(erange,estep,samplename,filename,dwell))
        # #dets = [det]
        # #RE(scan(dets, motor, start, stop, num))
        # #RE(count(dets,num))
        #
        # #works for scan
        #
        # dets = [det]
        # start = float(self.pe_start.text())
        # stop = float(self.pe_stop.text())
        # num = float(self.pe_npts.text())
        # RE(scan(dets, motor, start, stop, num))
        #
        # # plot_raster_path(plan, 'motor1', 'motor2', probe_size=.01)
        # header = db[-1]
        # string = str(header.table())
        # self.results.setText(string)

###############################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Spectroscopy()
    w.show()
    sys.exit(app.exec_())
