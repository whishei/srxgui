import sys
from PyQt5 import uic
import numpy
import xraylib
import math


###################### Solves for npts #########################
def PTShelper(start, stop, step):
    '''
    :param start: (float) the beginning of the energy region
    :param stop: (float) the end of the energy region
    :param step: (float) the step of the energy region
    :return: the number of points in that region
    '''
    if start == 0 and stop == 0:
        return 1
    else:
        pts = (stop - start) / step + 1
        return pts


##################### Solves for steps ##########################
def STEPShelper(start, stop, npts):
    '''
    :param start: (float) the beginning of the energy region
    :param stop: (float) the end of the energy region
    :param npts: (int) the number of points in that region
    :return: the step of the energy region
    '''
    if (start == 0 and stop == 0) or npts == 1:
        return 0.1
    else:
        steps = (stop - start)/ (npts - 1)
        return steps


############## Defines Erange, Estep, and num_pts ###############
def Erange(start, stop, step, erange, estep, num_pts):
    '''
    :param start: (float) the beginning of the energy region
    :param stop: (float) the end of the energy region
    :param step: (float) the step of the energy region
    :return: Does not return anything. Solves for the erange and the estep regions needed for the xanes_plan
    '''

    if (erange != []):
        erange = numpy.append(erange, stop)
    else:
        erange = numpy.append(erange, start)
        erange = numpy.append(erange, stop)
    estep = numpy.append(estep, step)

    ept = numpy.array([])  # ept is not the number of points, it is the energy points\n",

    # convert erange and estep to numpy array\n",
    erange = numpy.array(erange)
    ept = numpy.append(ept, numpy.arange(start, stop, step))
    ept = numpy.append(ept, numpy.array(erange[-1]),)
    pt = int(ept.size)
    num_pts = num_pts + pt
    return erange, estep, num_pts
