from bluesky.plans import grid_scan
import bluesky.preprocessors as bpp


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

def Add_to_Queue(str_item):
    global queue
    queue.append(str_item)
    print (queue)

def Delete_from_Queue(item):
    global queue
    del queue[item]

def EditErangeItem(changes1, changes2, changes3, x, y, z):
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

def EditKrangeItem(changes1, changes2, changes3, changes4, changes5, x, y ,z):
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

def EditXRFItem(xstart_changes1, xstop_changes1, xnum_changes1, ystart_changes1, ystop_changes1, ynum_changes1):
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

def ReturnErangeItem():
    global erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges
    return erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges

def ReturnKrangeItem():
    global erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges
    return erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges

def ReturnXRFItem():
    global xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes
    return xstart_changes, xstop_changes, xnum_changes, ystart_changes, ystop_changes, ynum_changes

def GetQueue():
    global queue
    return queue

def GetQueueItem(index1):
    global index, queue
    index = index1
    return queue[index1]

def ReturnQueueItem(index,list):
    global queue
    queue[index] = list
   # print (queue)

def SendIndex(index1):
    global index
    index = index1

def GetIndex():
    global index
    return index

def set_up_xrf(lg):
    return bpp.subs_decorator([lg])(grid_scan)