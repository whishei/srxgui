from bluesky import RunEngine
import ophyd
import databroker
from ophyd.sim import det1, det2
from bluesky.plans import count
import numpy as np
import matplotlib.pyplot as plt

RE = RunEngine({})
