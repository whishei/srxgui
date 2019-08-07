#Setting up the Parameter Widget  (Used for Spectroscopy Scans)

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import numpy as np
import xraylib
from Parameter_Helper import *
from MainScreen_Helper import *
import json
import sys

Ui_MainWindow, QtBaseClass = uic.loadUiType('Parameters.ui')

class Parameters(QtBaseClass, Ui_MainWindow):

    def __init__(self, parent = None):
        super(QtBaseClass, self).__init__()
        self.setupUi(self)
        self.edge_energy.setDisabled(True)
        self.elements.activated[str].connect(self.onActivated)
        self.edge.activated[str].connect(self.onChanged)
        self.xafs1_units.activated[str].connect(self.Units1)
        self.xafs2_units.activated[str].connect(self.Units2)
        self.xafs3_units.activated[str].connect(self.Units3)
        self.mode.activated[str].connect(self.Mode)
        #Filling the element options
        y = []
        for i in range(22,47):
            y = np.append(y, xraylib.AtomicNumberToSymbol(i))
        for i in range(51,103):
            y = np.append(y, xraylib.AtomicNumberToSymbol(i))
        for item in range(len(y)):
            self.elements.addItem(y[item])

    def Mode(self):
        mode = self.mode.currentText()
        energy = float(self.edge_energy.text())
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
        xafs1_units = self.xafs1_units.currentText()
        xafs2_units = self.xafs2_units.currentText()
        xafs3_units = self.xafs3_units.currentText()
        if self.edge_energy.isEnabled() == True:
            if mode == 'Absolute':
                pe_start = energy + pe_start
                pe_stop = energy + pe_stop
                xanes_start = energy + xanes_start
                xanes_stop = energy + xanes_stop
                xafs1_start = energy + xafs1_start
                xafs1_stop = energy + xafs1_stop
                xafs2_start = energy + xafs2_start
                xafs2_stop = energy + xafs2_stop
                xafs3_start = energy + xafs3_start
                xafs3_stop = energy + xafs3_stop
                self.pe_start.setValue(pe_start)
                self.pe_stop.setValue(pe_stop)
                self.xanes_start.setValue(xanes_start)
                self.xanes_stop.setValue(xanes_stop)
                self.xafs1_start.setValue(xafs1_start)
                self.xafs1_stop.setValue(xafs1_stop)
                self.xafs2_start.setValue(xafs2_start)
                self.xafs2_stop.setValue(xafs2_stop)
                self.xafs3_start.setValue(xafs3_start)
                self.xafs3_stop.setValue(xafs3_stop)
                self.pe_start.setRange(4500, 25000)
                self.pe_stop.setRange(4500, 25000)
                self.xanes_start.setRange(4500, 25000)
                self.xanes_stop.setRange(4500, 25000)
                if xafs1_units == 'eV':
                    self.xafs1_start.setRange(4500, 25000)
                    self.xafs1_stop.setRange(4500, 25000)
                if xafs2_units == 'eV':
                    self.xafs2_start.setRange(4500, 25000)
                    self.xafs2_stop.setRange(4500, 25000)
                if xafs3_units == 'eV':
                    self.xafs3_start.setRange(4500, 25000)
                    self.xafs3_stop.setRange(4500, 25000)



            if mode =='Relative':
                self.pe_start.setRange(4500 - energy, 25000 - energy)
                self.pe_stop.setRange(4500 - energy, 25000 - energy)
                self.xanes_start.setRange(4500 - energy, 25000 - energy)
                self.xanes_stop.setRange(4500 - energy, 25000 - energy)
                self.xafs1_start.setRange(4500 - energy, 25000 - energy)
                self.xafs1_stop.setRange(4500 - energy, 25000 - energy)
                self.xafs2_start.setRange(4500 - energy, 25000 - energy)
                self.xafs2_stop.setRange(4500 - energy, 25000 - energy)
                self.xafs3_start.setRange(4500 - energy, 25000 - energy)
                self.xafs3_stop.setRange(4500 - energy, 25000 - energy)
                pe_start =  pe_start - energy
                pe_stop = pe_stop - energy
                xanes_start = xanes_start- energy
                xanes_stop =  xanes_stop- energy
                xafs1_start =  xafs1_start- energy
                xafs1_stop = xafs1_stop- energy
                xafs2_start = xafs2_start- energy
                xafs2_stop = xafs2_stop - energy
                xafs3_start = xafs3_start- energy
                xafs3_stop = xafs3_stop- energy
                self.pe_start.setValue(pe_start)
                self.pe_stop.setValue(pe_stop)
                self.xanes_start.setValue(xanes_start)
                self.xanes_stop.setValue(xanes_stop)
                self.xafs1_start.setValue(xafs1_start)
                self.xafs1_stop.setValue(xafs1_stop)
                self.xafs2_start.setValue(xafs2_start)
                self.xafs2_stop.setValue(xafs2_stop)
                self.xafs3_start.setValue(xafs3_start)
                self.xafs3_stop.setValue(xafs3_stop)




################# Saving a Spectroscopy Scan #######################

    def Saving(self):
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
        global erange, estep, krange, kstep, num_pts
        erange = []
        estep = []
        num_pts = 0
        krange = []
        kstep = []
        edge = float(self.edge_energy.text())
        if edge == 4500.00:
            w = QMessageBox.warning(self, 'Error Message', 'You must chose an element and/or an edge before Saving.', QMessageBox.Ok)
        mode = self.mode.currentText()
        regions = int(self.num_regions.text())
        xafs1_units = self.xafs1_units.currentText()
        xafs2_units = self.xafs2_units.currentText()
        xafs3_units = self.xafs3_units.currentText()
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

        #Calculating the Erange, Estep, and Overall number of points
        if mode == 'Relative':
            pe_start = edge + float(self.pe_start.text())
            pe_stop = edge + float(self.pe_stop.text())
        erange, estep, num_pts = Erange(pe_start, pe_stop, pe_step, erange, estep, num_pts)
        if regions > 1:
            if mode == 'Relative':
                xanes_start = edge + float(self.xanes_start.text())
                xanes_stop = edge + float(self.xanes_stop.text())
            erange, estep, num_pts = Erange(xanes_start, xanes_stop, xanes_step, erange, estep, num_pts)
        if regions > 2:
            if xafs1_units == 'eV':
                if mode == 'Relative':
                    xafs1_start = edge + float(self.xafs1_start.text())
                    xafs1_stop = edge + float(self.xafs1_stop.text())
                erange, estep, num_pts = Erange(xafs1_start, xafs1_stop, xafs1_step, erange, estep, num_pts)
            else:
                krange, kstep, num_pts = Krange(xafs1_start, xafs1_stop, xafs1_step, krange, kstep, num_pts)
        if regions > 3:
            if xafs2_units == 'eV':
                if mode == 'Relative':
                    xafs2_start = edge + float(self.xafs2_start.text())
                    xafs2_stop = edge + float(self.xafs2_stop.text())
                erange, estep, num_pts = Erange(xafs2_start, xafs2_stop, xafs2_step, erange, estep, num_pts)
            else:
                krange, kstep, num_pts = Krange(xafs2_start, xafs2_stop, xafs2_step, krange, kstep, num_pts)
        if regions > 4:
            if xafs1_units == 'eV':
                if mode == 'Relative':
                    xafs3_start = edge + float(self.xafs3_start.text())
                    xafs3_stop = edge + float(self.xafs3_stop.text())
                erange, estep, num_pts = Erange(xafs3_start, xafs3_stop, xafs3_step, erange, estep, num_pts)
            else:
                krange, kstep, num_pts = Krange(xafs3_start, xafs3_stop, xafs3_step, krange, kstep, num_pts)

        dwell = float(self.pe_dwell.text())
        with open('testingjson.txt') as f:
            data = json.load(f)
            total_overhead = data['XAS']['overhead']
        #Calculating estimated scan time
        scan_sec = num_pts * (dwell + total_overhead)
        sample = str(self.sample_name.text())
        file = str(self.file_name.text())
        #Saving the collected parameters to MainScreen_Helper
        RunScan(erange, estep, dwell, sample, file, krange, kstep, edge)
        CalcTime(scan_sec)



    ############################# Points ##################################
    # Requires helper function

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
        if mode == 'Absolute':
            pe_start = float(self.pe_start.text())
            pe_stop = float(self.pe_stop.text())
        else:
            pe_start = edge + float(self.pe_start.text())
            pe_stop = edge + float(self.pe_stop.text())
        self.pe_npts.setRange(1, PTShelper(pe_start, pe_stop, 0.1))
        self.pe_npts.setValue(PTShelper(pe_start, pe_stop, pe_step))
        if mode == 'Absolute':
            xanes_start = float(self.xanes_start.text())
            xanes_stop = float(self.xanes_stop.text())
        else:
            xanes_start = edge + float(self.xanes_start.text())
            xanes_stop = edge + float(self.xanes_stop.text())
        self.xanes_npts.setRange(1, PTShelper(xanes_start, xanes_stop, 0.1))
        self.xanes_npts.setValue(PTShelper(xanes_start, xanes_stop, xanes_step))

        if mode == 'Absolute':
            xafs1_start = float(self.xafs1_start.text())
            xafs1_stop = float(self.xafs1_stop.text())
        else:
            xafs1_start = edge + float(self.xafs1_start.text())
            xafs1_stop = edge + float(self.xafs1_stop.text())
        self.xafs1_npts.setRange(1, PTShelper(xafs1_start, xafs1_stop, 0.1))
        self.xafs1_npts.setValue(PTShelper(xafs1_start, xafs1_stop, xafs1_step))

        if mode == 'Absolute':
            xafs2_start = float(self.xafs2_start.text())
            xafs2_stop = float(self.xafs2_stop.text())
        else:
            xafs2_start = edge + float(self.xafs2_start.text())
            xafs2_stop = edge + float(self.xafs2_stop.text())
        self.xafs2_npts.setRange(1, PTShelper(xafs2_start, xafs2_stop, 0.1))
        self.xafs2_npts.setValue(PTShelper(xafs2_start, xafs2_stop, xafs2_step))
        if mode == 'Absolute':
            xafs3_start = float(self.xafs3_start.text())
            xafs3_stop = float(self.xafs3_stop.text())
        else:
            xafs3_start = edge + float(self.xafs3_start.text())
            xafs3_stop = edge + float(self.xafs3_stop.text())
        self.xafs3_npts.setRange(1, PTShelper(xafs3_start, xafs3_stop, 0.1))
        self.xafs3_npts.setValue(PTShelper(xafs3_start, xafs3_stop, xafs3_step))



    ########################### Steps ###################################
    # Requires helper function

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
        if mode == 'Absolute':
            pe_start = float(self.pe_start.text())
            pe_stop = float(self.pe_stop.text())
        else:
            pe_start = edge + float(self.pe_start.text())
            pe_stop = edge + float(self.pe_stop.text())
        self.pe_step.setValue(STEPShelper(pe_start, pe_stop, pe_npts))

        if mode == 'Absolute':
            xanes_start = float(self.xanes_start.text())
            xanes_stop = float(self.xanes_stop.text())
        else:
            xanes_start = edge + float(self.xanes_start.text())
            xanes_stop = edge + float(self.xanes_stop.text())
        self.xanes_step.setValue(STEPShelper(xanes_start, xanes_stop, xanes_npts))

        if mode == 'Absolute':
            xafs1_start = float(self.xafs1_start.text())
            xafs1_stop = float(self.xafs1_stop.text())
        else:
            xafs1_start = edge + float(self.xafs1_start.text())
            xafs1_stop = edge + float(self.xafs1_stop.text())
        self.xafs1_step.setValue(STEPShelper(xafs1_start, xafs1_stop, xafs1_npts))

        if mode == 'Absolute':
            xafs2_start = float(self.xafs2_start.text())
            xafs2_stop = float(self.xafs2_stop.text())
        else:
            xafs2_start = edge + float(self.xafs2_start.text())
            xafs2_stop = edge + float(self.xafs2_stop.text())
        self.xafs2_step.setValue(STEPShelper(xafs2_start, xafs2_stop, xafs2_npts))

        if mode == 'Absolute':
            xafs3_start = float(self.xafs3_start.text())
            xafs3_stop = float(self.xafs3_stop.text())
        else:
            xafs3_start = edge + float(self.xafs3_start.text())
            xafs3_stop = edge + float(self.xafs3_stop.text())
        self.xafs3_step.setValue(STEPShelper(xafs3_start, xafs3_stop, xafs3_npts))
        
        
    ##################### Regions ########################

    def regions(self):
        '''
        :signal: set number of regions
        :return: disables/enables regions
        '''
        regions = int(self.num_regions.text())
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        if regions == 1 or regions == 2 or regions == 3 or regions == 4:
            self.xafs3_start.setDisabled(True)
            self.xafs3_stop.setDisabled(True)
            self.xafs3_step.setDisabled(True)
            self.xafs3_npts.setDisabled(True)
            self.xafs3_dwell.setDisabled(True)
            self.xafs3_units.setDisabled(True)
            self.xafs3_start.setRange(0,0)
            self.xafs3_stop.setRange(0,0)
            if regions == 2 or regions == 3 or regions == 4:
                self.xanes_start.setEnabled(True)
                self.xanes_stop.setEnabled(True)
                self.xanes_step.setEnabled(True)
                self.xanes_npts.setEnabled(True)
                self.xanes_dwell.setEnabled(True)
                if mode == 'Absolute':
                    self.xanes_start.setRange(4500, 25000)
                    self.xanes_stop.setRange(4500, 25000)
                if mode == 'Relative':
                    self.xanes_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                    self.xanes_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
                if regions == 3 or regions == 4:
                    self.xafs1_start.setEnabled(True)
                    self.xafs1_stop.setEnabled(True)
                    self.xafs1_step.setEnabled(True)
                    self.xafs1_npts.setEnabled(True)
                    self.xafs1_dwell.setEnabled(True)
                    self.xafs1_units.setEnabled(True)
                    if mode == 'Absolute':
                        self.xafs1_start.setRange(4500, 25000)
                        self.xafs1_stop.setRange(4500, 25000)
                    if mode == 'Relative':
                        self.xafs1_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                        self.xafs1_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
                    if regions == 4:
                        self.xafs2_start.setEnabled(True)
                        self.xafs2_stop.setEnabled(True)
                        self.xafs2_step.setEnabled(True)
                        self.xafs2_npts.setEnabled(True)
                        self.xafs2_dwell.setEnabled(True)
                        self.xafs2_units.setEnabled(True)
                        if mode == 'Absolute':
                            self.xafs2_start.setRange(4500, 25000)
                            self.xafs2_stop.setRange(4500, 25000)
                        if mode == 'Relative':
                            self.xafs2_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                            self.xafs2_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
        if regions == 1 or regions == 2 or regions == 3:
            self.xafs2_start.setDisabled(True)
            self.xafs2_stop.setDisabled(True)
            self.xafs2_step.setDisabled(True)
            self.xafs2_npts.setDisabled(True)
            self.xafs2_dwell.setDisabled(True)
            self.xafs2_units.setDisabled(True)
            self.xafs2_start.setRange(0,0)
            self.xafs2_stop.setRange(0,0)
        if regions == 1 or regions == 2:
            self.xafs1_start.setDisabled(True)
            self.xafs1_stop.setDisabled(True)
            self.xafs1_step.setDisabled(True)
            self.xafs1_npts.setDisabled(True)
            self.xafs1_dwell.setDisabled(True)
            self.xafs1_units.setDisabled(True)
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
            self.xafs3_units.setEnabled(True)
            if mode == 'Absolute':
                self.xafs3_start.setRange(4500, 25000)
                self.xafs3_stop.setRange(4500, 25000)
            if mode == 'Relative':
                self.xafs3_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                self.xafs3_stop.setRange(4500 - edge_energy, 25000 - edge_energy)



    ############################ Element Activated #########################

    def onActivated(self, text):
        '''
        :param text: (str) choice of element
        :param element: (int) element's atomic number (needed to obtain edge energy)
        :return: sets an element's edge energy and a suggested edge (as long as it is in the range 4.5 - 25)
        '''
        global element
        element = xraylib.SymbolToAtomicNumber(text)
        self.edge_energy.setDisabled(False)
        if xraylib.EdgeEnergy(element, xraylib.K_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                      xraylib.K_SHELL) <= 25:
            self.edge.setCurrentIndex(0)
            self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.K_SHELL) * 1000)
        else:
            if xraylib.EdgeEnergy(element, xraylib.L1_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                           xraylib.L1_SHELL) <= 25:
                self.edge.setCurrentIndex(1)
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L1_SHELL) * 1000)
            else:
                if xraylib.EdgeEnergy(element, xraylib.L2_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                               xraylib.L2_SHELL) <= 25:
                    self.edge.setCurrentIndex(2)
                    self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L2_SHELL) * 1000)
                else:
                    if xraylib.EdgeEnergy(element, xraylib.L3_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                                   xraylib.L3_SHELL) <= 25:
                        self.edge.setCurrentIndex(3)
                        self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L3_SHELL) * 1000)

        edge_energy = float(self.edge_energy.text())
        mode = self.mode.currentText()
        xafs1_units = self.xafs1_units.currentText()
        xafs2_units = self.xafs2_units.currentText()
        xafs3_units = self.xafs3_units.currentText()
        if mode == 'Relative':
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
            self.pe_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.pe_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xanes_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xanes_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs1_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs1_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs2_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs2_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs3_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs3_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.pe_start.setValue(pe_start)
            self.xanes_start.setValue(xanes_start)
            self.xafs1_start.setValue(xafs1_start)
            self.xafs2_start.setValue(xafs2_start)
            self.xafs3_start.setValue(xafs3_start)
            self.pe_stop.setValue(pe_stop)
            self.xanes_stop.setValue(xanes_stop)
            self.xafs1_stop.setValue(xafs1_stop)
            self.xafs2_stop.setValue(xafs2_stop)
            self.xafs3_stop.setValue(xafs3_stop)

        if mode == 'Absolute':
            self.pe_start.setRange(4500, 25000)
            self.pe_stop.setRange(4500, 25000)
            self.xanes_start.setRange(4500, 25000)
            self.xanes_stop.setRange(4500, 25000)
            self.pe_start.setValue(edge_energy)
            self.xanes_start.setValue(edge_energy)
            self.pe_stop.setValue(edge_energy)
            self.xanes_stop.setValue(edge_energy)
            if xafs1_units == 'eV':
                self.xafs1_start.setRange(4500, 25000)
                self.xafs1_stop.setRange(4500, 25000)
                self.xafs1_start.setValue(edge_energy)
                self.xafs1_stop.setValue(edge_energy)

            if xafs2_units == 'eV':
                self.xafs2_start.setRange(4500, 25000)
                self.xafs2_stop.setRange(4500, 25000)
                self.xafs2_start.setValue(edge_energy)
                self.xafs2_stop.setValue(edge_energy)
            if xafs3_units == 'eV':
                self.xafs3_start.setRange(4500, 25000)
                self.xafs3_stop.setRange(4500, 25000)
                self.xafs3_start.setValue(edge_energy)
                self.xafs3_stop.setValue(edge_energy)



    ############################# Edge Activated ###############################

    def onChanged(self, text):
        '''
        :param text: (str) choice of edge
        :return: sets an element's edge energy based off the chosen edge (as long as it is in the range 4.5 - 25)
        '''
        edge = str(text)
        if edge == 'K':
            if xraylib.EdgeEnergy(element, xraylib.K_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                          xraylib.K_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.K_SHELL) * 1000)
                self.edge_energy.setDisabled(False)
            else:
                self.edge_energy.setDisabled(True)
        if edge == 'L1':
            if xraylib.EdgeEnergy(element, xraylib.L1_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                           xraylib.L1_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L1_SHELL) * 1000)
                self.edge_energy.setDisabled(False)
            else:
                self.edge_energy.setDisabled(True)
        if edge == 'L2':
            if xraylib.EdgeEnergy(element, xraylib.L2_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                           xraylib.L2_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L2_SHELL) * 1000)
                self.edge_energy.setDisabled(False)
            else:
                self.edge_energy.setDisabled(True)
        if edge == 'L3':
            if xraylib.EdgeEnergy(element, xraylib.L3_SHELL) >= 4.5 and xraylib.EdgeEnergy(element,
                                                                                           xraylib.L3_SHELL) <= 25:
                self.edge_energy.setValue(xraylib.EdgeEnergy(element, xraylib.L3_SHELL) * 1000)
                self.edge_energy.setDisabled(False)
            else:
                self.edge_energy.setDisabled(True)
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        xafs1_units = self.xafs1_units.currentText()
        xafs2_units = self.xafs2_units.currentText()
        xafs3_units = self.xafs3_units.currentText()
        if mode == 'Relative':
            self.pe_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.pe_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xanes_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xanes_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs1_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs1_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs2_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs2_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs3_start.setRange(4500 - edge_energy, 25000 - edge_energy)
            self.xafs3_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
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

        if mode == 'Absolute':
            self.pe_start.setRange(4500, 25000)
            self.pe_stop.setRange(4500, 25000)
            self.xanes_start.setRange(4500, 25000)
            self.xanes_stop.setRange(4500, 25000)
            self.pe_start.setValue(edge_energy)
            self.xanes_start.setValue(edge_energy)
            self.pe_stop.setValue(edge_energy)
            self.xanes_stop.setValue(edge_energy)
            if xafs1_units == 'eV':
                self.xafs1_start.setRange(4500, 25000)
                self.xafs1_stop.setRange(4500, 25000)
                self.xafs1_start.setValue(edge_energy)
                self.xafs1_stop.setValue(edge_energy)

            if xafs2_units == 'eV':
                self.xafs2_start.setRange(4500, 25000)
                self.xafs2_stop.setRange(4500, 25000)
                self.xafs2_start.setValue(edge_energy)
                self.xafs2_stop.setValue(edge_energy)
            if xafs3_units == 'eV':
                self.xafs3_start.setRange(4500, 25000)
                self.xafs3_stop.setRange(4500, 25000)
                self.xafs3_start.setValue(edge_energy)
                self.xafs3_stop.setValue(edge_energy)



    ######################### k space ####################################

    def Units1(self, text):
        '''
        :param text: (str) choice of units
        :return: changes everything :(
        '''
        units = str(text)
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        regions = int(self.num_regions.text())
        try:
            if regions > 2:
                if units == 'k':
                    self.xafs2_units.setCurrentIndex(1)
                    self.xafs3_units.setCurrentIndex(1)
                    if mode == 'Relative':
                        xafs1_start = float(self.xafs1_start.text()) + edge_energy
                        xafs1_stop = float(self.xafs1_stop.text()) + edge_energy
                    else:
                        xafs1_start = float(self.xafs1_start.text())
                        xafs1_stop = float(self.xafs1_stop.text())
                    print (xafs1_start, xafs1_stop)
                    start = Etok(xafs1_start, edge_energy)
                    stop = Etok(xafs1_stop, edge_energy)
                    self.xafs1_start.setRange(0, Etok(25000, edge_energy))
                    self.xafs1_stop.setRange(0, Etok(25000, edge_energy))
                    self.xafs1_start.setValue(start)
                    self.xafs1_stop.setValue(stop)
                    self.Units2(self.xafs2_units.currentText())
                if units == 'eV':
                    xafs1_start = float(self.xafs1_start.text())
                    xafs1_stop = float(self.xafs1_stop.text())
                    start = ktoE(xafs1_start, edge_energy)
                    stop = ktoE(xafs1_stop, edge_energy)
                    if mode == 'Relative':
                        self.xafs1_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                        self.xafs1_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
                        self.xafs1_start.setValue(start - edge_energy)
                        self.xafs1_stop.setValue(stop - edge_energy)
                    else:
                        self.xafs1_start.setRange(4500, 25000)
                        self.xafs1_stop.setRange(4500, 25000)
                        self.xafs1_start.setValue(start)
                        self.xafs1_stop.setValue(stop)
        except RuntimeWarning:
            print ('the')


    def Units2(self, text):
        '''
        :param text: (str) choice of units
        :return: changes everything :(
        '''
        units = str(text)
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        regions = int(self.num_regions.text())
        if regions > 3:
            if units == 'k':
                self.xafs3_units.setCurrentIndex(1)
                if mode == 'Relative':
                    xafs2_start = float(self.xafs2_start.text()) + edge_energy
                    xafs2_stop = float(self.xafs2_stop.text()) + edge_energy
                else:
                    xafs2_start = float(self.xafs2_start.text())
                    xafs2_stop = float(self.xafs2_stop.text())
                start = Etok(xafs2_start, edge_energy)
                stop = Etok(xafs2_stop, edge_energy)
                self.xafs2_start.setRange(0, Etok(25000, edge_energy))
                self.xafs2_stop.setRange(0, Etok(25000, edge_energy))
                self.xafs2_start.setValue(start)
                self.xafs2_stop.setValue(stop)
                self.Units3(self.xafs3_units.currentText())
            if units == 'eV':
                xafs2_start = float(self.xafs2_start.text())
                xafs2_stop = float(self.xafs2_stop.text())
                start = ktoE(xafs2_start, edge_energy)
                stop = ktoE(xafs2_stop, edge_energy)
                if mode == 'Relative':
                    self.xafs2_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                    self.xafs2_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
                    self.xafs2_start.setValue(start - edge_energy)
                    self.xafs2_stop.setValue(stop - edge_energy)
                else:
                    self.xafs2_start.setRange(4500, 25000)
                    self.xafs2_stop.setRange(4500, 25000)
                    self.xafs2_start.setValue(start)
                    self.xafs2_stop.setValue(stop)

    def Units3(self, text):
        '''
        :param text: (str) choice of units
        :return: changes everything :(
        '''
        units = str(text)
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        regions = int(self.num_regions.text())
        if regions > 4:
            if units == 'k':
                if mode == 'Relative':
                    xafs3_start = float(self.xafs3_start.text()) + edge_energy
                    xafs3_stop = float(self.xafs3_stop.text()) + edge_energy
                else:
                    xafs3_start = float(self.xafs3_start.text())
                    xafs3_stop = float(self.xafs3_stop.text())
                start = Etok(xafs3_start, edge_energy)
                stop = Etok(xafs3_stop, edge_energy)
                self.xafs3_start.setRange(0, Etok(25000, edge_energy))
                self.xafs3_stop.setRange(0, Etok(25000, edge_energy))
                self.xafs3_start.setValue(start)
                self.xafs3_stop.setValue(stop)
            if units == 'eV':
                xafs3_start = float(self.xafs3_start.text())
                xafs3_stop = float(self.xafs3_stop.text())
                start = ktoE(xafs3_start, edge_energy)
                stop = ktoE(xafs3_stop, edge_energy)
                if mode == 'Relative':
                    self.xafs3_start.setRange(4500 - edge_energy, 25000 - edge_energy)
                    self.xafs3_stop.setRange(4500 - edge_energy, 25000 - edge_energy)
                    self.xafs3_start.setValue(start - edge_energy)
                    self.xafs3_stop.setValue(stop - edge_energy)
                else:
                    self.xafs3_start.setRange(4500, 25000)
                    self.xafs3_stop.setRange(4500, 25000)
                    self.xafs3_start.setValue(start)
                    self.xafs3_stop.setValue(stop)



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
        mode = self.mode.currentText()
        edge_energy = float(self.edge_energy.text())
        pe_start = float(self.pe_start.text())
        xanes_start = float(self.xanes_start.text())
        xafs1_start = float(self.xafs1_start.text())
        xafs2_start = float(self.xafs2_start.text())
        xafs3_start = float(self.xafs3_start.text())
        if mode == 'Absolute':
            if pe_start != 4500:
                self.pe_stop.setRange(pe_start, 25000)
            if xanes_start != 4500:
                self.xanes_stop.setRange(xanes_start, 25000)
            if xafs1_start != 4500:
                self.xafs1_stop.setRange(xafs1_start, 25000)
            if xafs2_start != 4500:
                self.xafs2_stop.setRange(xafs2_start, 25000)
            if xafs3_start != 4500:
                self.xafs3_stop.setRange(xafs3_start, 25000)
        if mode == 'Relative':
            if pe_start != 4500:
                self.pe_stop.setRange(pe_start, 25000 - edge_energy)
            if xanes_start != 4500:
                self.xanes_stop.setRange(xanes_start, 25000 - edge_energy)
            if xafs1_start != 4500:
                self.xafs1_stop.setRange(xafs1_start, 25000 - edge_energy)
            if xafs2_start != 4500:
                self.xafs2_stop.setRange(xafs2_start, 25000 - edge_energy)
            if xafs3_start != 4500:
                self.xafs3_stop.setRange(xafs3_start, 25000 - edge_energy)



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
        xafs1_units = self.xafs1_units.currentText()
        xafs2_units = self.xafs2_units.currentText()
        xafs3_units = self.xafs3_units.currentText()
        if pe_stop != 4500:
            self.xanes_start.setValue(pe_stop)
        if xanes_stop != 4500 and xafs1_units == 'eV':
            self.xafs1_start.setValue(xanes_stop)
        if xafs1_stop != 4500 and xafs2_units == 'eV':
            self.xafs2_start.setValue(xafs1_stop)
        if xafs2_stop != 4500 and xafs3_units == 'eV':
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Parameters()
    w.show()
    sys.exit(app.exec_())