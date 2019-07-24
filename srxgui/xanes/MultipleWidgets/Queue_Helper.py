global queue, erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, index, xchanges, ychanges, zchanges
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

def Add_to_Queue(str_item):
    global queue
    queue.append(str_item)
    #print (queue)

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

def ReturnErangeItem():
    global erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges
    #print (erange_changes)
    return erange_changes, estep_changes, dwell_changes, xchanges, ychanges, zchanges

def ReturnKrangeItem():
    global erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges
    return erange_changes, estep_changes, krange_changes, kstep_changes, dwell_changes, xchanges, ychanges, zchanges


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