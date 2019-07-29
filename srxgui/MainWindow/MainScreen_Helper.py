########## Used as a connection between main, parameters, queue, and location

import numpy
from bluesky.plans import grid_scan
from ophyd.sim import det4, motor1, motor2, noisy_det
import bluesky.preprocessors as bpp

#For Spectroscopy Scans
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


############################# Setting Parameters (Used in parameters) #################################

def RunScan(range1,step1,dwell,sample1,file1, range2 = numpy.array([]), step2 = numpy.array([]), energy = 0):
    'Collects the erange, estep, dwell, samplename, filename, krange, kstep, and E0 to run a Spectroscopy Scan'

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


############################# Setting Seconds (Used in parameters) #################################

def CalcTime(sec):
    'Collecting the seconds for a Spectroscopy Scan (Used for estimated scan time)'
    global scan_sec
    scan_sec = 0
    scan_sec = sec


############################# Retrieving the Parameters (Used in main) #################################

def collect_args(ax11 = None, ax22 = None, ax33 = None):
    'Sending main the kwargs to run a my_xanes plan'
    global erange, estep, acqtime, sample, file, krange, kstep, E0, ax1, ax2, ax3, xmotor, ymotor, zmotor
    ax1 = ax11
    ax2 = ax22
    ax3 = ax33
    if erange == []:
        #The user forgot to save the parameters
        return 0
    elif krange == []:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange,
                'k_steps': kstep, 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}
    else:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange.tolist(),
                'k_steps': kstep.tolist(), 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}



############################# Retrieving the Parameters (Used in Queue) #################################

def add_to_queue():
    'Sending the queue the kwargs to add to the queue'
    global krange, kstep, E0, erange, estep, acqtime, sample, file, ax1, ax2, ax3, xmotor, ymotor, zmotor
    if erange == []:
        #The user forgot to save the parameters
        return 0
    elif krange == []:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange,
                'k_steps': kstep, 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}
    else:
        return {'x_motor': xmotor, 'y_motor': ymotor, 'z_motor': zmotor, 'e_range': erange.tolist(), 'e_steps': estep.tolist(),  'E_0': E0, 'k_range': krange.tolist(),
                'k_steps': kstep.tolist(), 'dwell': acqtime, 'samplename': sample,
                'filename': file, 'ax11': ax1, 'ax22': ax2, 'ax33': ax3}



################################### Retrieving Seconds (Used in main) ###################################

def collect_secs():
    global scan_sec
    return scan_sec


################################## Setting Motors (Used in Location)#######################################

def set_motors(x, y, z):
    global xmotor, ymotor, zmotor
    xmotor = 0
    ymotor = 0
    zmotor = 0
    xmotor = x
    ymotor = y
    zmotor = z






#For XRF Mapping
global xstart,xstop,xnum, ystart,ystop, ynum, xrf_dwell, second, flymotor, stepmotor
xstart = 0
ystart = 0
xstop = 0
ystop = 0
ynum = 0
xnum = 0
xrf_dwell = 0
second = 0
flymotor = ''
stepmotor = ''



############################# Setting Parameters (Used in Window_) #################################

def SavingXRF(xstart1,xstop1,xnum1, ystart1,ystop1, ynum1, xrf_dwell1, second1, flymotor1, stepmotor1 ):
    'Collects the xstart, xstop xnum, ystart, ystop, ynum, dwell, seonds, flymotor, and stepping motor to run a Spectroscopy Scan'
    global xstart, xstop, xnum, ystart, ystop, ynum, xrf_dwell, second, flymotor, stepmotor
    xstart = 0
    ystart = 0
    xstop = 0
    ystop = 0
    ynum = 0
    xnum = 0
    xrf_dwell = 0
    second = 0
    flymotor = ''
    stepmotor = ''
    xstart = xstart1
    ystart = ystart1
    xstop = xstop1
    ystop = ystop1
    xnum = xnum1
    ynum = ynum1
    xrf_dwell = xrf_dwell1
    second = second1
    flymotor = flymotor1
    stepmotor = stepmotor1


############################# Retrieving the Parameters (Used in main) #################################

def Collecting_XRF(lg):
    'Sending main the args and plan to run a grid scan'
    global xstart, xstop, xnum, ystart, ystop, ynum
    print (xstart,xstop,xnum,ystart,ystop, ynum)
    detectors = [noisy_det]
    return bpp.subs_decorator([lg])(grid_scan), (detectors, motor1, xstart, xstop, xnum, motor2, ystart, ystop, ynum, False)


############################# Retrieving the Parameters (Used in queue) #################################

def add_xrf_to_queue():
    'Used to set up display item in queue'
    global xstart, xstop, xnum, ystart, ystop, ynum
    return [xstart, xstop, xnum, ystart, ystop, ynum]


############################# Retrieving the Parameters (Used in queue) #################################

def add_xrf_args():
    'Adding the args to the queue'
    global xstart, xstop, xnum, ystart, ystop, ynum
    detectors = [noisy_det]
    return (detectors, motor1, xstart, xstop, xnum, motor2, ystart, ystop, ynum, False)


############################### Retrieving Seconds (Used in main) ###################################

def Seconds_XRF():
    global second
    return second



############################## Retrieving xnum, ynum (Used in main) #################################

def NeedXandY():
    'Needed to set up the plot for grid scans'
    global xnum,ynum
    return xnum,ynum



############################# Retrieving the Flymotor, Stepmotor (Used in main) ###################

def ReadFlyandStep():
    global flymotor, stepmotor
    return flymotor, stepmotor


