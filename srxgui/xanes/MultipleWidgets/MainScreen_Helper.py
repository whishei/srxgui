
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
import numpy

global erange, estep, acqtime, scan_sec, sample, file, krange, kstep, E0 , ax1, ax2, ax3, xmotor, ymotor, zmotor
erange = []
estep = []
acqtime = 0
scan_sec = 0
sample = ''
file = ''
ax1 = None
ax2 = None
ax3 = None
krange = []
kstep = []
E0 = 0
xmotor = 0
ymotor = 0
zmotor= 0



# def setAxs(ax_1 = None, ax_2 = None, ax_3 = None):
#     global ax1, ax2, ax3
#     ax1 = ax_1
#     ax2 = ax_2
#     ax3 = ax_3


def RunScan(range1,step1,dwell,sample1,file1, range2 = numpy.array([]), step2 = numpy.array([]), energy = 0):
    global erange, estep, acqtime, sample, file, krange, kstep, E0
    erange = []
    estep = []
    krange = numpy.array([])
    kstep = numpy.array([])
    E0 = 0
    acqtime = 0
    erange = range1
    estep = step1
    krange = range2
    kstep = step2
    E0 = energy
    acqtime = dwell
    sample = sample1
    file = file1

def CalcTime(sec):
    global scan_sec
    scan_sec = 0
    scan_sec = sec


def collect_args(ax11 = None, ax22 = None, ax33 = None):
    global erange, estep, acqtime, sample, file, krange, kstep, E0, ax1, ax2, ax3, xmotor, ymotor, zmotor
    ax1 = ax11
    ax2 = ax22
    ax3 = ax33
    if erange == []:
        return 0
    elif krange == []:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange,
                'k_steps': kstep, 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}
    else:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange.tolist(),
                'k_steps': kstep.tolist(), 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}


def add_to_queue():
    global krange, kstep, E0, erange, estep, acqtime, sample, file, ax1, ax2, ax3, xmotor, ymotor, zmotor
    if erange == []:
        return 0
    elif krange == []:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange,
                'k_steps': kstep, 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}
    else:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange.tolist(),
                'k_steps': kstep.tolist(), 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}

def collect_secs():
    global scan_sec
    return scan_sec

def set_motors(x, y, z):
    global xmotor, ymotor, zmotor
    xmotor = 0
    ymotor = 0
    zmotor = 0
    xmotor = x
    ymotor = y
    zmotor = z


# def getAxs():
#     global ax1, ax2, ax3
#     return ax1, ax2, ax3