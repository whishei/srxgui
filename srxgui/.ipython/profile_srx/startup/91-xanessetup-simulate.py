from bluesky.plans import list_scan
import bluesky.plans as bp
from bluesky.plan_stubs import mv
from bluesky.plan_stubs import one_1d_step
from bluesky.preprocessors import finalize_wrapper
from bluesky.preprocessors import subs_wrapper
from bluesky.utils import short_uid as _short_uid
#import scanoutput
import numpy
import time
#from databroker import get_table
import collections
from bluesky.callbacks import LiveTable, LivePlot
from ophyd.sim import noisy_det


def xanes_afterscan_plan(scanid, filename, roinum):
    #print(scanid,filename,roinum)
    # custom header list 
    headeritem = [] 
    # load header for our scan
    h=db[scanid]

    # construct basic header information
    userheaderitem = {}
    userheaderitem['uid'] = h.start['uid']
    userheaderitem['sample.name'] = h.start['sample']['name']
    userheaderitem['initial_sample_position.hf_stage.x'] = h.start['initial_sample_position']['hf_stage_x']
    userheaderitem['initial_sample_position.hf_stage.y'] = h.start['initial_sample_position']['hf_stage_y']
    userheaderitem['hfm.y'] = h.start['hfm']['y']
    userheaderitem['hfm.bend'] = h.start['hfm']['bend']

    # create columns for data file
    columnitem = ['energy_energy', 'energy_u_gap_readback', 'energy_bragg', 'energy_c2_x']
    # columnitem = ['energy_energy', 'energy_u_gap_readback', 'energy_bragg']
    # include I_0 and I_t from either the SRS or Oxford preamp, raise expection
    # if neither present
    if 'sclr1' in h.start['detectors']:
        # columnitem = columnitem + ['sclr_i0', 'sclr_it']
        columnitem = columnitem + ['sclr_i0', 'sclr_im', 'sclr_it']
    elif 'current_preamp' in h.start['detectors']:
        columnitem = columnitem + ['current_preamp_ch0', 'current_preamp_ch2']
    else:
        raise KeyError("Neither SRS nor Oxford preamplifier found in data!")
    # include fluorescence data if present, allow multiple rois
    if 'xs' in h.start['detectors']:
        if type(roinum) is not list:
            roinum = [roinum]
        for i in roinum:
            roi_name = 'roi{:02}'.format(i)
            roi_key = []
            roi_key.append(getattr(xs.channel1.rois, roi_name).value.name)
            roi_key.append(getattr(xs.channel2.rois, roi_name).value.name)
            roi_key.append(getattr(xs.channel3.rois, roi_name).value.name)

        [ columnitem.append(roi) for roi in roi_key ]
    # construct user convenience columns allowing prescaling of ion chamber, diode and
    # fluorescence detector data
    usercolumnitem = {}
    datatablenames = []
    
    # assume that we are using either the SRS or Oxford preamp for both I_0 and I_T
    if 'xs' in h.start['detectors']:
        datatablenames = datatablenames + [ str(roi) for roi in roi_key]
    if 'sclr1' in  h.start['detectors']:
        # datatablenames = datatablenames + ['sclr_i0', 'sclr_it']
        datatablenames = datatablenames + ['sclr_i0', 'sclr_im', 'sclr_it']
        datatable = h.table(stream_name='primary',fields=datatablenames)        
        i0_array = numpy.array(datatable['sclr_i0'])
        im_array = numpy.array(datatable['sclr_im'])
        it_array = numpy.array(datatable['sclr_it'])
    elif 'current_preamp' in h.start['detectors']:
        datatablenames = datatablenames + ['current_preamp_ch2', 'current_preamp_ch0']
        datatable = h.table(stream_name='primary',fields=datatablenames)        
        i0_array = numpy.array(datatable['current_preamp_ch2'])
        it_array = numpy.array(datatable['current_preamp_ch0'])
    else:
        raise KeyError
    # calculate sums for xspress3 channels of interest
    if 'xs' in h.start['detectors']:
        for i in roinum:
            roi_name = 'roi{:02}'.format(i)
            roisum = datatable[getattr(xs.channel1.rois, roi_name).value.name] 
            #roisum.index += -1
            roisum = roisum + datatable[getattr(xs.channel2.rois, roi_name).value.name] 
            roisum = roisum + datatable[getattr(xs.channel3.rois, roi_name).value.name] 
            usercolumnitem['If-{:02}'.format(i)] = roisum
            usercolumnitem['If-{:02}'.format(i)].round(0)

    scanoutput.textout(scan = scanid, header = headeritem, 
                        userheader = userheaderitem, column = columnitem, 
                        usercolumn = usercolumnitem, 
                        usercolumnname = usercolumnitem.keys(), 
                        output = False, filename_add = filename) 

def xanes_plan(erange = [], estep = [],  
            harmonic=1, correct_c2_x=True, correct_c1_r = False, detune = None,
            acqtime=1., roinum=1, delaytime = 0.00, struck=True, fluor = True,
            samplename = '', filename = '', shutter = True, align = False, align_at = None, per_step=None, ax1 = None, ax2 = None, ax3 = None):
                
    '''
    erange (list of floats): energy ranges for XANES in eV, e.g. erange = [7112-50, 7112-20, 7112+50, 7112+120]
    estep  (list of floats): energy step size for each energy range in eV, e.g. estep = [2, 1, 5]
    
    harmonic (odd integer): when set to 1, use the highest harmonic achievable automatically. 
                                    when set to an odd integer, force the XANES scan to use that harmonic
    correct_c2_x (boolean or float): when True, automatically correct the c2x 
                                     when False, c2x will not be moved during the XANES scan
    correct_c1_r (False or float): when False, c1r will not be moved during a XANES scan
                                   when set to a float, c1r will be set to that value before a XANES scan but will remain the same during the whole scan
    detune:  add this value to the gap of the undulator to reduce flux [mm]

    acqtime (float): acqusition time to be set for both xspress3 and preamplifier                                   
    roinum: select the roi to be used to calculate the XANES spectrum
    delaytime:  reduce acquisition time of F460 by this value [sec]
    struck:  Use the SRS and Struck scaler for the ion chamber and diode.  Set to False to use the F460.
    fluorescence:  indicate the presence of fluorescence data [bool]

    samplename (string): sample name to be saved in the scan metadata
    filename (string): filename to be added to the scan id as the text output filename

    shutter:  instruct the scan to control the B shutter [bool]
    align:  control the tuning of the DCM pointing before each XANES scan [bool]
    align_at:  energy at which to align, default is the first energy point
    ax1: give the GUI's ax to plug the graph into
    ax2: give the GUI's ax to plug the graph into
    ax3: give the GUI's ax to plug the graph into
    '''                                
                
    ept = numpy.array([])
    det = []
    filename=filename
    last_time_pt = time.time()
    # ringbuf = collections.deque(maxlen=10)
    # c2pitch_kill=EpicsSignal("XF:05IDA-OP:1{Mono:HDCM-Ax:P2}Cmd:Kill-Cmd")
    # xs.external_trig.put(False)

    #make sure user provided correct input
    if erange is []:
        raise AttributeError("An energy range must be provided in a list by means of the 'erange' keyword.")
    if estep is []:
        raise AttributeError("A list of energy steps must be provided by means of the 'esteps' keyword.")
    if (not isinstance(erange,list)) or (not isinstance(estep,list)):
        raise TypeError("The keywords 'estep' and 'erange' must be lists.")
    if len(erange)-len(estep) is not 1:
        raise ValueError("The 'erange' and 'estep' lists are inconsistent;"\
                         +'c.f., erange = [7000, 7100, 7150, 7500], estep = [2, 0.5, 5] ')
    if type(roinum) is not list:
        roinum = [roinum]
    if detune is not None:
        yield from abs_set(energy.detune,detune)

    #record relevant meta data in the Start document, defined in 90-usersetup.py
    # metadata_record()
    #add user meta data
    RE.md['sample']  = {'name': samplename}
    RE.md['scaninfo']  = {'type': 'XANES','ROI': roinum,'raster' : False, 'dwell':acqtime}
    RE.md['scan_input'] = str(np.around(erange, 2)) + ', ' + str(np.around(estep, 2))
   
    #convert erange and estep to numpy array
    erange = numpy.array(erange)
    estep = numpy.array(estep)
    #calculation for the energy points        
    for i in range(len(estep)):
        ept = numpy.append(ept, numpy.arange(erange[i], erange[i+1], estep[i]))
    ept = numpy.append(ept, numpy.array(erange[-1]))

    # Debugging
    # Convert energy to bragg angle
    egap = np.array(())
    ebragg = np.array(())
    exgap = np.array(())
    for i in ept:
        # Convert from eV to keV
        # if (i > 4500):
        #    i = i / 1000
        # Convert keV to bragg angle
        #b, _, _ = energy.energy_to_positions(i, 5, 0)
        eg, eb, ex = energy.forward(i)
        egap = np.append(egap, eg)
        ebragg = np.append(ebragg, eb)
        exgap = np.append(exgap, ex)
        # print(ebragg)

    #register the detectors
    # det = [ring_current]
    # if struck == True:
        # det.append(sclr1)
    # else:
        # det.append(current_preamp)
    # if fluor == True:
        # det.append(xs)
        #setup xspress3
        # yield from abs_set(xs.settings.acquire_time,acqtime)
        # yield from abs_set(xs.total_points,len(ept))
    det.append(sclr1)
    det.append(xs)
    
    #setup the preamp
    # if struck == True:
        # yield from abs_set(sclr1.preset_time,acqtime)
    # else:
        # yield from abs_set(current_preamp.exp_time,acqtime-delaytime)
    #setup dcm/energy options
    # if correct_c2_x is False:
        # yield from abs_set(energy.move_c2_x,False)
    # if correct_c1_r is not False:
        # yield from abs_set(dcm.c1_roll,correct_c1_r)
    if harmonic != 1: 
        yield from abs_set(energy.harmonic, harmonic)
    #prepare to peak up DCM at first scan point
    # if align_at is not None:
        # align = True
    # if align is True:
        # if align_at == None:
            # yield from abs_set(energy, ept[0], wait = True)
        # else:
            # print("aligning at ",align_at)
            # yield from abs_set(energy, float(align_at), wait = True)
    # energy.u_gap.corrfunc_dis.put(1)
    #open b shutter
    # if shutter is True:
        #shut_b.open()
        # yield from mv(shut_b, 'Open')
        #yield from abs_set(shut_b,1,wait=True)
    #peak up DCM at first scan point
    # if align is True:
        # ps = PeakStats(dcm.c2_pitch.name,'sclr_i0')
        # e_value = energy.energy.get()[1]
#        if e_value < 10.:
#            yield from abs_set(sclr1.preset_time,0.1, wait = True)
#            peakup = scan([sclr1], dcm.c2_pitch, -19.335, -19.305, 31)
#        else:
#            yield from abs_set(sclr1.preset_time,1., wait = True)
#            peakup = scan([sclr1], dcm.c2_pitch, -19.355, -19.320, 36)
        # if e_value < 14.:
            # sclr1.preset_time.put(0.1)
        # else:
            # sclr1.preset_time.put(1.)
        # peakup = scan([sclr1], dcm.c2_pitch, -19.320, -19.360, 41)
        # peakup = subs_wrapper(peakup,ps)
        # yield from peakup
        # yield from abs_set(dcm.c2_pitch, ps.cen, wait = True)
        #ttime.sleep(10)
        #yield from abs_set(c2pitch_kill, 1)

    #setup the live callbacks
    myscan = list_scan(det, energy, list(ept), per_step=per_step)
    livecallbacks = []    
    livetableitem = ['en.energy']
    if struck == True:
        livetableitem = livetableitem + ['sclr_i0', 'sclr_it']  
    # else:
        # livetableitem = livetableitem + ['current_preamp_ch0', 'current_preamp_ch2']  
    if fluor == True:
        # roi_name = 'roi{:02}'.format(roinum[0])
        # roi_key = []
        # roi_key.append(getattr(xs.channel1.rois, roi_name).value.name)
        # roi_key.append(getattr(xs.channel2.rois, roi_name).value.name)
        # roi_key.append(getattr(xs.channel3.rois, roi_name).value.name)
        # livetableitem.append(roi_key[0])    
        livecallbacks.append(LiveTable(['xs_intensity']))
        #liveploty = [xs]
        liveploty = xs.name
        liveplotx = en.energy.name
        #liveplotfig = plt.figure('raw xanes')
    # elif struck == True:
        # liveploty = 'sclr_it' 
        # liveplotx = energy.energy.name
        # liveplotfig = plt.figure('raw xanes')
    
    #livecallbacks.append(LiveTable([sclr1, xs, energy]))

    ########Tom said to edit it here!!!!!!!!!

    # livecallbacks.append(LivePlot(y =liveploty, x=liveplotx, fig=liveplotfig))
    #livecallbacks.append(LivePlot(y='xs_intensity', x=liveplotx, fig=liveplotfig))
    #livecallbacks.append(LivePlot(y =liveploty, x=liveplotx, ax=plt.gca(title='raw xanes')))
        
    if struck == True:
        liveploty = 'sclr_i0'
        i0 = 'sclr_i0'
    # else:
        # liveploty = 'current_preamp_ch2'
        # i0 = 'current_preamp_ch2'
    #liveplotfig2 = plt.figure(i0)
    #ax = ax2
    livecallbacks.append(LivePlot(liveploty, x=liveplotx, ax = ax2))
    #livecallbacks.append(LivePlot(liveploty, x=liveplotx, ax=plt.gca(title='incident intensity')))
    #livenormfig = plt.figure('normalized xanes')
    #if fluor == True:
        #livecallbacks.append(NormalizeLivePlot([xs], x=liveplotx, norm_key = i0, fig=livenormfig))
        #livecallbacks.append(NormalizeLivePlot(roi_key[0], x=liveplotx, norm_key = i0, ax=plt.gca(title='normalized xanes')))  
    # else:
        # livecallbacks.append(NormalizeLivePlot('sclr_it', x=liveplotx, norm_key = i0, fig=livenormfig))  
        #livecallbacks.append(NormalizeLivePlot(roi_key[0], x=liveplotx, norm_key = i0, ax=plt.gca(title='normalized xanes')))  
    # def after_scan(name, doc):
        # if name != 'stop':
            # print("You must export this scan data manually: xanes_afterscan_plan(doc[-1], <filename>, <roinum>)")
            # return
        # xanes_afterscan_plan(doc['run_start'], filename, roinum)
        # logscan_detailed('xanes')

    # def at_scan(name, doc):
        # scanrecord.current_scan.put(doc['uid'][:6])
        # scanrecord.current_scan_id.put(str(doc['scan_id']))
        # scanrecord.current_type.put(RE.md['scaninfo']['type'])
        # scanrecord.scanning.put(True)

    # def finalize_scan():
        # yield from abs_set(energy.u_gap.corrfunc_en,1)  # disabled to test if
        # undulator gets stuck -AMK
        # yield from abs_set(energy.move_c2_x, True)
        # yield from abs_set(energy.harmonic, 1)
        # scanrecord.scanning.put(False)
        # if shutter == True:
            # yield from mv(shut_b,'Close')
        # if detune is not None:
            # energy.detune.put(0)
        # del RE.md['sample']['name']
        # del RE.md['scaninfo']
    # det = noisy_det
    myscan = list_scan(det, en.energy, list(ept))
    #myscan = list_scan([sclr1], en.energy, list(ept))
    # myscan = list_scan(det, energy, list(ept), per_step=per_step(detectors, motor, step))
    # myscan = list_scan(det, energy.bragg, list(ebragg), energy.u_gap, list(egap), energy.c2_x, list(exgap))
    # myscan = scan_nd(det, energy.bragg, list(ebragg), energy.u_gap, list(egap), energy.c2_x, list(exgap))
    # myscan = finalize_wrapper(myscan,finalize_scan)
    livecallbacks = []
    #livecallbacks.append(LiveTable([xs, en.energy]))
    #liveplotfig = plt.figure('raw xanes')
    #livecallbacks.append(LivePlot(y = 'xs_intensity', x = 'en_energy', fig = liveplotfig))
    #livecallbacks.append(LiveTable([xs, en.energy]))
    #liveplotfig2 = plt.figure('io')
    ax = ax1
    livecallbacks.append(LivePlot(y = 'xs_intensity', x = 'en_energy', ax = ax))
    ax = ax2
    livecallbacks.append(LivePlot(y='sclr1', x='en_energy', ax = ax))

    #RE.subscribe(livecallbacks[1])
    return (yield from subs_wrapper(myscan,{'all':livecallbacks}))
    return (yield from subs_wrapper(myscan, LiveTable([xs, en.energy])))
    #return (yield from myscan)