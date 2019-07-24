import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from MainScreen_Helper import *
from Queue_Helper import *

form, base = uic.loadUiType('Queue.ui')
form2, base2 = uic.loadUiType('Erange_Editor.ui')
form3, base3 = uic.loadUiType('Krange_Editor.ui')

class Erange_Editor(base2, form2):
    def __init__(self, parent = None):
        super(base2, self).__init__()
        self.setupUi(self)
        self.Okay.clicked.connect(self.Edits)

    def Edits(self):
        #erange_changes = []
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

class Queue(base,form):

    def __init__(self, parent = None):
        super(base, self).__init__()
        self.setupUi(self)
        self.add.clicked.connect(self.Adding)
        self.delete_2.clicked.connect(self.Deleting)
        self.Queue_list.itemDoubleClicked.connect(self.Editing)
        self.Save_queue.clicked.connect(self.SaveEditing)

    def Adding(self):
        kwargs = add_to_queue()
        if kwargs == 0:
            w = QMessageBox.warning(self, 'Error Message', 'You must save the scan before you can start.',
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
                #str_item = 'Spectroscopy Scan: RE(exafs_plan(erange = ' + str(erange) + ', estep = ' + str(estep) +', dwell = ' + str(dwell) + '))'

            else:
                display_item = 'Spectroscopy Scan: Erange = ' + str(erange) + ', Estep = ' + str(estep) + ', E0 = ' + str(E0)  + 'Krange = ' + str(krange) + ', Kstep = ' + str(kstep) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(xmotor) + ', Y = ' + str(ymotor) + ', Z =' + str(zmotor)
                #str_item = 'Spectroscopy Scan: RE(exafs_plan(erange = ' + str(erange) + ', estep = ' + str(estep) + ', krange = '+ str(krange) + ', kstep = ' + str(kstep) + ', dwell = ' + str(dwell) + '))'
            Add_to_Queue(kwargs)
            self.Queue_list.addItem(display_item)

    def Deleting(self):
        item = self.Queue_list.currentRow()
        Delete_from_Queue(item)
        self.Queue_list.takeItem(item)

    def Editing(self):
        queue = self.Queue_list
        item_index = queue.currentRow()
        print (item_index)
        item = GetQueueItem(item_index)
        print (item)
        erange = str(item['e_range'])
        erange = erange.strip('[]')
        estep= str(item['e_steps'])
        estep = estep.strip('[]')
        xmotor = float(item['x_motor'])
        ymotor = float(item['y_motor'])
        zmotor = float(item['z_motor'])
        E0 = item['E_0']
        if item['k_range'] == []:
            self.ErangeWindow = Erange_Editor()
            #str(item['erange'])
            self.ErangeWindow.erange.setText(erange)
            self.ErangeWindow.estep.setText(estep)
            self.ErangeWindow.dwell.setText(str(item['dwell']))
            self.ErangeWindow.x_motor.setValue(xmotor)
            self.ErangeWindow.y_motor.setValue(ymotor)
            self.ErangeWindow.z_motor.setValue(zmotor)
            self.ErangeWindow.E0.setText(str(E0))
            self.ErangeWindow.show()
        else:
            self.KrangeWindow = Krange_Editor()
            krange = str(item['k_range'])
            krange = krange.strip('[]')
            kstep = str(item['k_steps'])
            krange = kstep.strip('[]')
            self.KrangeWindow.erange_2.setText(str(item['e_range']))
            self.KrangeWindow.estep_2.setText(str(item['e_steps']))
            self.KrangeWindow.krange.setText(krange)
            self.KrangeWindow.kstep.setText(kstep)
            self.KrangeWindow.dwell_2.setText(str(item['dwell']))
            self.KrangeWindow.x_motor.setValue(xmotor)
            self.KrangeWindow.y_motor.setValue(ymotor)
            self.KrangeWindow.z_motor.setValue(zmotor)
            self.KrangeWindow.E0.setText(str(E0))
            self.KrangeWindow.show()

    def SaveEditing(self):
        item_txt = self.Queue_list.currentItem()
        queue = self.Queue_list
        item_index = queue.currentRow()
        item = GetQueueItem(item_index)
        E0 = item['E_0']
        if item['k_range'] == []:
            erange_change, estep_change, dwell_change, xchange, ychange, zchange= ReturnErangeItem()
            item['e_range'] = erange_change
            item['e_steps'] = estep_change
            item['dwell'] = dwell_change
            item['x_motor'] = xchange
            item['y_motor'] = ychange
            item['z_motor'] = zchange
            ReturnQueueItem(item_index,item)
            item_txt.setText('Spectroscopy Scan: Erange = ' + str(erange_change) + ', Estep = ' + str(estep_change) + ', E0 = ' + str(E0) + ', Dwell Time = ' + str(dwell_change) + ', X = ' + str(xchange) + ', Y = ' + str(ychange) + ', Z =' + str(zchange))
        else:
            erange_change, estep_change, krange_change, kstep_change, dwell_change, xchange, ychange, zchange  = ReturnKrangeItem()
            item['erange'] = erange_change
            item['estep'] = estep_change
            item['krange'] = krange_change
            item['kstep'] = kstep_change
            item['acqtime'] = dwell_change
            item['x_motor'] = xchange
            item['y_motor'] = ychange
            item['z_motor'] = zchange
            ReturnQueueItem(item_index,item)
            item_txt.setText('Spectroscopy Scan: Erange = ' + str(erange_change) + ', Estep = ' + str(estep_change) + ', E0 = ' + str(E0)  + 'Krange = ' + str(krange_change) + ', Kstep = ' + str(kstep_change) + ', Dwell Time = ' + str(dwell) + ', X = ' + str(xchange) + ', Y = ' + str(ychange) + ', Z =' + str(zchange))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Queue()
    w.show()
    sys.exit(app.exec_())