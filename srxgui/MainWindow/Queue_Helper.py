#Helper for the Queue, also allows the queue to connect to the Main Window

from bluesky.plans import grid_scan
import bluesky.preprocessors as bpp
import json
import numpy


#For all scans
global queue, erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, index, xchanges, ychanges, zchanges, index, \
    xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes, xrf_dwell_changes
queue = []
erange_changes = ''
estep_changes = ''
krange_changes = ''
kstep_changes = ''
dwell_changes = ''
index = 0
xchanges = ''
ychanges = ''
zchanges = ''
xstart_changes = 0
xstop_changes = 0
xnum_changes = 0
ystart_changes = 0
ystop_changes = 0
ynum_changes = 0
xrf_dwell_changes = 0


#Adding an item to the queue
def Add_to_Queue(str_item):
    global queue
    queue.append(str_item)
    print (queue)


#Deleting an item from the queue
def Delete_from_Queue(item):
    global queue
    del queue[item]


#Editing a Spectroscopy Scan without k-space
def EditErangeItem(changes1, changes2, changes3, x, y, z):
    '''Collecting the erange changes, estep changes, dwell changes, xmotor changes, ymotor changes, zmotor changes '''
    global erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges
    erange_changes = ''
    estep_changes = ''
    dwell_changes = ''
    xchanges = ''
    ychanges = ''
    zchanges = ''
    erange_changes = changes1
    estep_changes = changes2
    dwell_changes = changes3
    xchanges = x
    ychanges = y
    zchanges = z
    print (xchanges)


#Editing a Spectroscopy Scan with k-space
def EditKrangeItem(changes1, changes2, changes3, changes4, changes5, x, y ,z):
    ''' Collecting the erange changes, estep changes, krange changes, kstep changes, dwell changes, xmotor changes, ymotor changes, zmotor changes'''
    global erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges
    erange_changes = ''
    estep_changes = ''
    krange_changes = ''
    kstep_changes = ''
    dwell_changes = ''
    xchanges = ''
    ychanges = ''
    zchanges = ''
    erange_changes = changes1
    estep_changes = changes2
    krange_changes = changes3
    kstep_changes = changes4
    dwell_changes = changes5
    xchanges = x
    ychanges = y
    zchanges = z
    print (erange_changes)


#Editing an XRF scan
def EditXRFItem(xstart_changes1, xstop_changes1, xnum_changes1, ystart_changes1, ystop_changes1, ynum_changes1):
    ''' Collecting the xstart changes, xstop_ changes, xnum changes, ystart changes, ystop changes, ynum changes'''
    global xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes
    xstart_changes = 0
    xstop_changes = 0
    xnum_changes = 0
    ystart_changes = 0
    ystop_changes = 0
    ynum_changes = 0
    xstart_changes = xstart_changes1
    xstop_changes = xstop_changes1
    xnum_changes = xnum_changes1
    ystart_changes = ystart_changes1
    ystop_changes = ystop_changes1
    ynum_changes = ynum_changes1


#Returning an Edited Spectroscopy Scan without k-space
def ReturnErangeItem():
    global erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges
    return erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges


#Returning an Edited Spectroscopy Scan with k-space
def ReturnKrangeItem():
    global erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges
    return erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges


#Returning an Edited XRF scan
def ReturnXRFItem():
    global xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes
    return xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes


#Returning the queue
def GetQueue():
    global queue
    return queue


#Returning the current queue item
def GetQueueItem(index1):
    global index, queue
    index = index1
    return queue[index1]


#Returning the edited queue item to change the queue itself
def ReturnQueueItem(index,list):
    global queue
    queue[index] = list


#Setting the current index
def SendIndex(index1):
    global index
    index = index1


#Retrieving the current index
def GetIndex():
    global index
    return index


#Set up for xrf scans
def set_up_xrf(lg):
    return bpp.subs_decorator([lg])(grid_scan)



def GetscanSecs():
    total_sec = 0
    ept = numpy.array([])
    for i in range(len(queue)):
        try:
            kwargs = (queue[i])
            erange = kwargs['e_range']
            estep = kwargs['e_steps']
            erange = numpy.array(erange)
            estep = numpy.array(estep)
            for i in range(len(estep)):
                ept = numpy.append(ept, numpy.arange(erange[i], erange[i + 1], estep[i]))
            ept = numpy.append(ept, numpy.array(erange[-1]))
            krange = kwargs['k_range']
            if krange != []:
                kstep = kwargs['k_steps']
                kpt = np.array([], dtype=np.float)
                krange = np.array(krange, dtype=np.float)
                if (krange[0] == -1):
                    krange[0] = Etok(ept[-1], E0)
                kstep = np.array(kstep, dtype=np.float)
                for i in range(len(kstep)):
                    kpt = np.append(kpt, np.arange(krange[i], krange[i + 1], kstep[i]))
                kpt = np.append(kpt, np.array(krange[-1]))
                kptE = ktoE(kpt, E0)

                ept = np.append(ept, kptE)
            num_pts = int(ept.size)
            num_pts = num_pts + 1
            dwell = kwargs['dwell']
            with open('testingjson.txt') as f:
                data = json.load(f)
                total_overhead = data['XAS']['overhead']
            scan_sec = num_pts * (dwell + total_overhead)
            total_sec = total_sec + scan_sec
        except:
            print ('nope')
    return total_sec