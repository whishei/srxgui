# from bluesky.plan_stubs import mv
from ophyd.sim import SynAxis


class Energy(SynAxis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def forward(self, p_pos):
        return 10, 6, 7000


energy = Energy(name='energy')