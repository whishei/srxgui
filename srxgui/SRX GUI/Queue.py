# Setting up the Queue Widget

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QInputDialog
from PyQt5 import uic
from MainScreen_Helper import *
from Queue_Helper import *


#Loads 4 different .uis: The main Queue, then if a scan is being edited: Erange_Editor, Krange_Editor (Both spectroscopy scans), and XRF_Editor
form, base = uic.loadUiType('Queue.ui')
form2, base2 = uic.loadUiType('Erange_Editor.ui')
form3, base3 = uic.loadUiType('Krange_Editor.ui')
form4, base4 = uic.loadUiType('XRF_Editor.ui')


#Loads an editor pop-up window for a Spectroscopy scan only in eV
class Erange_Editor(base2, form2):
    def __init__(self, parent = None):
        super(base2, self).__init__()
        self.setupUi(self)
        self.Okay.clicked.connect(self.Edits)

    def Edits(self):
        erange_changes = (self.erange.text())
        erange_changes = erange_changes.split(', ')
        erange_changes = [float(i) for i in erange_changes]
        estep_changes = self.estep.text()
        estep_changes = estep_changes.split(', ')
        estep_changes = [float(i) for i in estep_changes]
        dwell_changes = float(self.dwell.text())
        xmotor_changes = float(self.x_motor.text())
        ymotor_changes = float(self.y_motor.text())
        zmotor_changes = float(self.z_motor.text())
        EditErangeItem(erange_changes,estep_changes, dwell_changes, xmotor_changes, ymotor_changes, zmotor_changes)
        Erange_Editor.close(self)


#Loads an editor pop-up window for a Spectroscopy scan with k-space
class Krange_Editor(base3, form3):
    def __init__(self, parent = None):
        super(base3, self).__init__()
        self.setupUi(self)
        self.Okay_2.clicked.connect(self.Edits)

    def Edits(self):
        erange_changes = (self.erange.text())
        erange_changes = erange_changes.split(', ')
        erange_changes = [float(i) for i in erange_changes]
        estep_changes = self.estep.text()
        estep_changes = estep_changes.split(', ')
        estep_changes = [float(i) for i in estep_changes]
        dwell_changes = float(self.dwell.text())
        krange_changes = (self.krange.text())
        krange_changes = krange_changes.split(', ')
        krange_changes = [float(i) for i in krange_changes]
        kstep_changes = self.kstep.text()
        kstep_changes = kstep_changes.split(', ')
        kstep_changes = [float(i) for i in kstep_changes]
        xmotor_changes = float(self.x_motor.text())
        ymotor_changes = float(self.y_motor.text())
        zmotor_changes = float(self.z_motor.text())
        EditKrangeItem(erange_changes,estep_changes, krange_changes, kstep_changes, dwell_changes, xmotor_changes, ymotor_changes, zmotor_changes)
        Krange_Editor.close(self)


#Loads an editor pop-up window for an XRF scan
class XRF_Editor(base4, form4):
    def __init__(self, parent = None):
        super(base4, self).__init__()
        self.setupUi(self)
        self.Okay.clicked.connect(self.Edits)

    def Edits(self):
        xstart_changes = float(self.xstart.text())
        xstop_changes = float(self.xstop.text())
        xnum_changes = float(self.xnum.text())
        ystart_changes = float(self.ystart.text())
        ystop_changes = float(self.ystop.text())
        ynum_changes = float(self.ynum.text())
        EditXRFItem(xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes)
        XRF_Editor.close(self)



#Loads the Queue widget into the Main Window
class Queue(base,form):

    def __init__(self, parent = None):
        super(base, self).__init__()
        self.setupUi(self)
        self.add.clicked.connect(self.Adding)
        self.delete_2.clicked.connect(self.Deleting)
        self.Queue_list.itemDoubleClicked.connect(self.Editing)
        self.Save_queue.clicked.connect(self.SaveEditing)
        self.load_queue.clicked.connect(self.LoadQueue)



    def LoadQueue(self):
        '''
        Loading the previously saved queue back into the GUI
        '''
        file = open("queue.txt", "r")
        contents = file.read()
        print (contents)
        for i in range(len(contents)):
            pln= contents[i]
            print (pln)
            args = contents[i]
            kwargs = contents[i]
            if pln == 'S':
                if kwargs == 0:
                    w = QMessageBox.warning(self, 'Error Message',
                                            'You must save the scan before you can add to queue.',
                                            QMessageBox.Ok)
                else:
                    erange = kwargs['e_range']
                    estep = kwargs['e_steps']
                    krange = kwargs['k_range']
                    kstep = kwargs['k_steps']
                    E0 = kwargs['E_0']
                    dwell = kwargs['dwell']
                    xmotor = kwargs['x_motor']
                    ymotor = kwargs['y_motor']
                    zmotor = kwargs['z_motor']
                    if krange == []:
                        display_item = 'Spectroscopy Scan: Erange = ' + str(erange) + ', Estep = ' + str(
                            estep) + ', E0 = ' + str(E0) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(
                            xmotor) + ', Y = ' + str(ymotor) + ', Z =' + str(zmotor)
                    else:
                        display_item = 'Spectroscopy Scan: Erange = ' + str(erange) + ', Estep = ' + str(
                            estep) + ', E0 = ' + str(E0) + 'Krange = ' + str(krange) + ', Kstep = ' + str(
                            kstep) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(xmotor) + ', Y = ' + str(
                            ymotor) + ', Z =' + str(zmotor)
                    item = [pln, args, kwargs]
                    Add_to_Queue(item)  # Adds a scan to the queue
                    self.Queue_list.addItem(display_item)  # Adds a scan to the displayed list
            if pln == 'X':
                xstart = args[0]
                xstop = args[1]
                xnum = args[2]
                ystart = args[3]
                ystop = args[4]
                ynum = args[5]
                args = add_xrf_args()
                item = [pln, args, kwargs]
                Add_to_Queue(item)  # Adds a scan to the queue
                display_item = 'XRF Mapping: Xstart = ' + str(xstart) + ', Xstop = ' + str(xstop) + ', Xnum = ' + str(
                    xnum) + ', Ystart = ' + str(ystart) + ', Ystop = ' + str(ystop) + ', Ynum = ' + str(ynum)
                self.Queue_list.addItem(display_item)  # Adds a scan to the displayed list
        file.close()



########################## Adding a Scan to the Queue ###########################

    def Adding(self):
        '''
        Adds a scan to the queue:
        index = the index of the tab (0 = Spectroscopy scan, 1 = XRF Mapping)
        '''

        index = GetIndex()
        if index == 0:   #Spectroscopy Scan
            pln, args, kwargs = add_to_queue()
            if kwargs == 0:
                w = QMessageBox.warning(self, 'Error Message', 'You must save the scan before you can add to queue.',
                                        QMessageBox.Ok)
            else:
                erange = kwargs['e_range']
                estep = kwargs['e_steps']
                krange = kwargs['k_range']
                kstep = kwargs['k_steps']
                E0 = kwargs['E_0']
                dwell = kwargs['dwell']
                xmotor = kwargs['x_motor']
                ymotor = kwargs['y_motor']
                zmotor = kwargs['z_motor']
                if krange == []:
                    display_item = 'Spectroscopy Scan: Erange = ' + str(erange) + ', Estep = ' + str(estep) + ', E0 = ' + str(E0) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(xmotor) + ', Y = ' + str(ymotor) + ', Z =' + str(zmotor)
                else:
                    display_item = 'Spectroscopy Scan: Erange = ' + str(erange) + ', Estep = ' + str(estep) + ', E0 = ' + str(E0)  + 'Krange = ' + str(krange) + ', Kstep = ' + str(kstep) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(xmotor) + ', Y = ' + str(ymotor) + ', Z =' + str(zmotor)
                item = [pln, args, kwargs]
                Add_to_Queue(item)  #Adds a scan to the queue
                self.Queue_list.addItem(display_item) #Adds a scan to the displayed list

        if index == 1:    #XRF Mapping
            pln, args, kwargs = add_xrf_to_queue()
            xstart = args[0]
            xstop = args[1]
            xnum = args[2]
            ystart= args[3]
            ystop = args[4]
            ynum = args[5]
            args = add_xrf_args()
            item = [pln,args,kwargs]
            Add_to_Queue(item) #Adds a scan to the queue
            display_item = 'XRF Mapping: Xstart = ' + str(xstart) + ', Xstop = ' + str(xstop) + ', Xnum = ' + str(xnum) + ', Ystart = ' + str(ystart) + ', Ystop = ' + str(ystop) + ', Ynum = ' + str(ynum)
            self.Queue_list.addItem(display_item)  #Adds a scan to the displayed list


    ########################## Deleting a Scan from the Queue ###########################

    def Deleting(self):
        '''
        Deletes a scan from both the displayed list and the queue
        '''
        item = self.Queue_list.currentRow()
        Delete_from_Queue(item)
        self.Queue_list.takeItem(item)


    ########################## Editing a Scan from the Queue ###########################

    def Editing(self):
        '''
        Opens the appropriate editor for the scan type
        '''
        queue = self.Queue_list
        item_index = queue.currentRow()
        item = GetQueueItem(item_index)
        text = queue.currentItem().text()
        if text[0] == 'S':  #Spectroscopy Scan
            erange = str(item[2]['e_range'])
            erange = erange.strip('[]')
            estep= str(item[2]['e_steps'])
            estep = estep.strip('[]')
            xmotor = float(item[2]['x_motor'])
            ymotor = float(item[2]['y_motor'])
            zmotor = float(item[2]['z_motor'])
            E0 = item[2]['E_0']
            if item[2]['k_range'] == []:  #Does not include k-space
                self.ErangeWindow = Erange_Editor()
                #str(item['erange'])
                self.ErangeWindow.erange.setText(erange)
                self.ErangeWindow.estep.setText(estep)
                self.ErangeWindow.dwell.setText(str(item[2]['dwell']))
                self.ErangeWindow.x_motor.setValue(xmotor)
                self.ErangeWindow.y_motor.setValue(ymotor)
                self.ErangeWindow.z_motor.setValue(zmotor)
                self.ErangeWindow.E0.setText(str(E0))
                self.ErangeWindow.show()
            else:  #Includes k-space
                self.KrangeWindow = Krange_Editor()
                krange = str(item[2]['k_range'])
                krange = krange.strip('[]')
                kstep = str(item[2]['k_steps'])
                kstep = kstep.strip('[]')
                self.KrangeWindow.erange.setText(erange)
                self.KrangeWindow.estep.setText(estep)
                self.KrangeWindow.krange.setText(krange)
                self.KrangeWindow.kstep.setText(kstep)
                self.KrangeWindow.dwell.setText(str(item[2]['dwell']))
                self.KrangeWindow.x_motor.setValue(xmotor)
                self.KrangeWindow.y_motor.setValue(ymotor)
                self.KrangeWindow.z_motor.setValue(zmotor)
                self.KrangeWindow.E0.setText(str(E0))
                self.KrangeWindow.show()
        else: #XRF Mapping
            self.XRFWindow = XRF_Editor()
            self.XRFWindow.xstart.setText(str(item[1][2]))
            self.XRFWindow.xstop.setText(str(item[1][3]))
            self.XRFWindow.xnum.setText(str(item[1][4]))
            self.XRFWindow.ystart.setText(str(item[1][6]))
            self.XRFWindow.ystop.setText(str(item[1][7]))
            self.XRFWindow.ynum.setText(str(item[1][8]))
            self.XRFWindow.show()


    ########################## Saving the Edits ###########################

    def SaveEditing(self):
        '''
        Saves the edits to change the display item and the values in the queue
        '''
        item_txt = self.Queue_list.currentItem()
        queue = self.Queue_list
        item_index = queue.currentRow()
        item = GetQueueItem(item_index)
        text = queue.currentItem().text()
        if text[0] == 'S': #Spectroscopy Scan
            E0 = item[2]['E_0']
            if item[2]['k_range'] == []:  #No k-space
                erange_change, estep_change, dwell_change, xchange, ychange, zchange= ReturnErangeItem()
                item[2]['e_range'] = erange_change
                item[2]['e_steps'] = estep_change
                item[2]['dwell'] = dwell_change
                item[2]['x_motor'] = xchange
                item[2]['y_motor'] = ychange
                item[2]['z_motor'] = zchange
                ReturnQueueItem(item_index,item)
                item_txt.setText('Spectroscopy Scan: Erange = ' + str(erange_change) + ', Estep = ' + str(estep_change) + ', E0 = ' + str(E0) + ', Dwell Time = ' + str(dwell_change) + ', X = ' + str(xchange) + ', Y = ' + str(ychange) + ', Z =' + str(zchange))
            else: #k-space
                erange_change, estep_change, krange_change, kstep_change, dwell_change, xchange, ychange, zchange  = ReturnKrangeItem()
                item[2]['erange'] = erange_change
                item[2]['estep'] = estep_change
                item[2]['krange'] = krange_change
                item[2]['kstep'] = kstep_change
                item[2]['acqtime'] = dwell_change
                item[2]['x_motor'] = xchange
                item[2]['y_motor'] = ychange
                item[2]['z_motor'] = zchange
                ReturnQueueItem(item_index,item)
                item_txt.setText('Spectroscopy Scan: Erange = ' + str(erange_change) + ', Estep = ' + str(estep_change) + ', E0 = ' + str(E0)  + 'Krange = ' + str(krange_change) + ', Kstep = ' + str(kstep_change) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(xchange) + ', Y = ' + str(ychange) + ', Z =' + str(zchange))
        else: #XRF Mapping
            xstart_change, xstop_change, xnum_change, ystart_change, ystop_change, ynum_change = ReturnXRFItem()
            args = list(item[1])
            args[2] = xstart_change
            args[3] = xstop_change
            args[4] = xnum_change
            args[6] = ystart_change
            args[7] = ystop_change
            args[8] = ynum_change
            item[1] = tuple(args)
            ReturnQueueItem(item_index,item)
            item_txt.setText('XRF Mapping: Xstart = ' + str(xstart_change) + ', Xstop = ' + str(xstop_change) + ', Xnum = ' + str(xnum_change) + ', Ystart = ' + str(ystart_change) + ', Ystop = ' + str(ystop_change) + ', Ynum = ' + str(ynum_change))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Queue()
    w.show()
    sys.exit(app.exec_())