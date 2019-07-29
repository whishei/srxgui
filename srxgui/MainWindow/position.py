from ophyd import (PseudoPositioner, PseudoSingle, EpicsMotor)
from ophyd import (Component as Cpt, Device)
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)
from ophyd.sim import SynSignal, SynAxis
from ophyd.positioner import SoftPositioner
from bluesky.run_engine import RunEngine
import bluesky.plan_stubs as bps
# from bluesky.run_engine import *

class HFSampleStage (Device):
    x = Cpt(SynAxis)
    y = Cpt(SynAxis)
    z = Cpt(SynAxis)
    th = Cpt(SynAxis)
    topx = Cpt(SynAxis)
    topz = Cpt(SynAxis)


hf_stage = HFSampleStage(name='hf_stage')
hf_stage.x.set(5)

hf_stage.read()


##############################################################################
####################################################################################
#Detector
from ophyd.sim import hw
from bluesky.plans import scan
from bluesky.run_engine import RunEngine
hw = hw()
detector = hw.det
detector.read()
simmotor1 = hw.motor
simmotor1.read()
simmotor1.set(0)
simmotor2 = hw.motor
simmotor2.read()
simmotor2.set(1)

# RE(scan([detector],simmotor1,0,14,10))


#Flyer
from ophyd.sim import hw
from bluesky.run_engine import RunEngine
from databroker import temp_config, Broker
from bluesky.plans import fly
import bluesky.plans as bp

hw = hw()
flying_zebra = hw.flyer1
db = Broker.named('temp')
RE = RunEngine()
RE.subscribe(db.insert)
RE(fly([flying_zebra]))
RE(fly([flying_zebra]))
hdr = db[-1]
hdr.stream_names
hdr.table('stream_name')

hw.direct_img

hw.det.exposure_time = 1

RE(bp.count([hw.det], num=3))

db[-1].table()