import ophyd.sim
from ophyd.sim import DetWithCountTime, DetWithConf, det, FakeEpicsSignal, FakeEpicsSignalRO, Device, Signal
from ophyd.sim import Component as Cpt
from ophyd.sim import DDC
from collections import OrderedDict


# From 20-detectors
class EpicsSignalROLazyier(FakeEpicsSignalRO):

    def get(self, *args, timeout=5, **kwargs):
        return super().get(*args, timeout=timeout, **kwargs)


def _scaler_fields(attr_base, field_base, range_, **kwargs):
    defn = OrderedDict()

    for i in range_:
        attr = '{attr}{i}'.format(attr=attr_base, i=i)

        suffix = '{field}{i}'.format(field=field_base, i=i)

        defn[attr] = (EpicsSignalROLazyier, suffix, kwargs)

    return defn


class SRXScaler(Device):
    # acquire_mode = Cpt(FakeEpicsSignal, 'AcquireMode')
    #
    # acquiring = Cpt(FakeEpicsSignal, 'Acquiring')
    #
    # asyn = Cpt(FakeEpicsSignal, 'Asyn')
    #
    # channel1_source = Cpt(FakeEpicsSignal, 'Channel1Source')
    #
    # channel_advance = Cpt(FakeEpicsSignal, 'ChannelAdvance', string=True)
    #
    # channels = DDC(_scaler_fields('chan', '.S', range(1, 33)))
    #
    # client_wait = Cpt(FakeEpicsSignal, 'ClientWait')
    #
    # count_on_start = Cpt(FakeEpicsSignal, 'CountOnStart')
    #
    # current_channel = Cpt(FakeEpicsSignal, 'CurrentChannel')
    #
    # disable_auto_count = Cpt(FakeEpicsSignal, 'DisableAutoCount')
    #
    # do_read_all = Cpt(FakeEpicsSignal, 'DoReadAll')
    #
    # dwell = Cpt(FakeEpicsSignal, 'Dwell')
    #
    # elapsed_real = Cpt(FakeEpicsSignal, 'ElapsedReal')
    #
    # enable_client_wait = Cpt(FakeEpicsSignal, 'EnableClientWait')
    #
    # erase_all = Cpt(FakeEpicsSignal, 'EraseAll')
    #
    # erase_start = Cpt(FakeEpicsSignal, 'EraseStart')
    #
    # firmware = Cpt(FakeEpicsSignal, 'Firmware')
    #
    # hardware_acquiring = Cpt(FakeEpicsSignal, 'HardwareAcquiring')
    #
    # input_mode = Cpt(FakeEpicsSignal, 'InputMode')
    #
    # max_channels = Cpt(FakeEpicsSignal, 'MaxChannels')
    #
    # model = Cpt(FakeEpicsSignal, 'Model')
    #
    # mux_output = Cpt(FakeEpicsSignal, 'MUXOutput')
    #
    # nuse_all = Cpt(FakeEpicsSignal, 'NuseAll')
    #
    # output_mode = Cpt(FakeEpicsSignal, 'OutputMode')
    #
    # output_polarity = Cpt(FakeEpicsSignal, 'OutputPolarity')
    #
    # prescale = Cpt(FakeEpicsSignal, 'Prescale')
    #
    # preset_real = Cpt(FakeEpicsSignal, 'PresetReal')
    #
    # read_all = Cpt(FakeEpicsSignal, 'ReadAll')
    #
    # read_all_once = Cpt(FakeEpicsSignal, 'ReadAllOnce')
    #
    # set_acquiring = Cpt(FakeEpicsSignal, 'SetAcquiring')
    #
    # set_client_wait = Cpt(FakeEpicsSignal, 'SetClientWait')
    #
    # snl_connected = Cpt(FakeEpicsSignal, 'SNL_Connected')
    #
    # software_channel_advance = Cpt(FakeEpicsSignal, 'SoftwareChannelAdvance')
    #
    # count_mode = Cpt(FakeEpicsSignal, '.CONT')
    #
    # start_all = Cpt(FakeEpicsSignal, 'StartAll')
    #
    # stop_all = Cpt(FakeEpicsSignal, 'StopAll')
    #
    # user_led = Cpt(FakeEpicsSignal, 'UserLED')

    # wfrm = Cpt(FakeEpicsSignal, 'Wfrm')

    mca1 = Cpt(FakeEpicsSignalRO, 'mca1')

    mca2 = Cpt(FakeEpicsSignalRO, 'mca2')

    mca3 = Cpt(FakeEpicsSignalRO, 'mca3')

    mca4 = Cpt(FakeEpicsSignalRO, 'mca4')

    i0 = Cpt(Signal)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class SimSrxXspress3Detector(DetWithCountTime):
    # external_trig = ophyd.sim.Component(name = 'external_trig')
    def __init__(self, *, configuration_attrs=None, read_attrs=None, **kwargs):
        '''
        if configuration_attrs is None:

            configuration_attrs = ['external_trig', 'total_points',

                                   'spectra_per_point', 'settings',

                                   'rewindable']

        if read_attrs is None:

            read_attrs = ['channel1', 'channel2', 'channel3', 'hdf5']
        '''

        super().__init__(configuration_attrs=configuration_attrs,

                     read_attrs=read_attrs, **kwargs)

    # this is possiblely one too many places to store this

    # in the parent class it looks at if the extrenal_trig signal is high

    # self._mode = SRXMode.step

    # self.create_dir.put(-3)


# xs = SrxXspress3Detector('XF:05IDD-ES{Xsp:1}:', name='xs')
xs = SimSrxXspress3Detector(name='xs')
sclr1 = SRXScaler(name = 'sclr1')
sclr1.mca1.sim_put([1,1,1])
sclr1.mca2.sim_put([2,2,2])
sclr1.read_attrs = ['mca1', 'mca2']
#Energy
from ophyd import (PseudoPositioner, PseudoSingle, EpicsMotor)
from ophyd import (Component as Cpt, Device)
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)
from ophyd.sim import SynSignal, SynAxis
from ophyd.positioner import SoftPositioner


#Energy Simulator
class FakeEnergy(PseudoPositioner):
    # The pseudo positioner axes:
    energy = Cpt(PseudoSingle, limits=(4500, 25000))

    # The real (or physical) positioners:\n",
    harmonic = Cpt(SoftPositioner, init_pos=1)
    fundamental = Cpt(SoftPositioner, init_pos=4500)

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        pseudo_pos = self.PseudoPosition(*pseudo_pos)
        return self.RealPosition(harmonic=self.harmonic.position,
                                 fundamental=pseudo_pos.energy / self.harmonic.position)

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        real_pos = self.RealPosition(*real_pos)
        return self.PseudoPosition(energy=real_pos.fundamental * real_pos.harmonic)

en = FakeEnergy(name='en')
en.harmonic
en.energy
en.fundamental
en.harmonic.set(3)

en.read()

# xs.channel1.rois.read_attrs = ['roi{:02}'.format(j) for j in [1, 2, 3, 4]]
#
# xs.channel2.rois.read_attrs = ['roi{:02}'.format(j) for j in [1, 2, 3, 4]]
#
# xs.channel3.rois.read_attrs = ['roi{:02}'.format(j) for j in [1, 2, 3, 4]]
#
# xs.hdf5.num_extra_dims.put(0)
#
# xs.channel2.vis_enabled.put(1)
#
# xs.channel3.vis_enabled.put(1)
#
# xs.settings.num_channels.put(3)
#
#
#
# xs.settings.configuration_attrs = ['acquire_period',
#
# 			'acquire_time',
#
# 			'gain',
#
# 			'image_mode',
#
# 			'manufacturer',
#
# 			'model',
#
# 			'num_exposures',
#
# 			'num_images',
#
# 			'temperature',
#
# 			'temperature_actual',
#
# 			'trigger_mode',
#
# 			'config_path',
#
# 			'config_save_path',
#
# 			'invert_f0',
#
# 			'invert_veto',
#
# 			'xsp_name',
#
# 			'num_channels',
#
# 			'num_frames_config',
#
# 			'run_flags',
#
# 			'trigger_signal']

