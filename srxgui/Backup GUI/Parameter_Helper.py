#Helper file for Parameters.py

import numpy

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

def Krange(start, stop, step, krange, kstep, num_pts):
    '''
    :param start: (float) the beginning of the energy region
    :param stop: (float) the end of the energy region
    :param step: (float) the step of the energy region
    :return: Does not return anything. Solves for the erange and the estep regions needed for the xanes_plan
    '''

    if (krange != []):
        krange = numpy.append(krange, stop)
    else:
        krange = numpy.append(krange, start)
        krange = numpy.append(krange, stop)
    kstep = numpy.append(kstep, step)

    kpt = numpy.array([])  # ept is not the number of points, it is the energy points\n",

    # convert erange and estep to numpy array\n",
    krange = numpy.array(krange)
    kpt = numpy.append(kpt, numpy.arange(start, stop, step))
    kpt = numpy.append(kpt, numpy.array(krange[-1]),)
    pt = int(kpt.size)
    num_pts = num_pts + pt
    return krange, kstep, num_pts


def Checker(energy):
    ranger = energy.tolist()
    for i in range(1, len(ranger)):
        if ranger[i] == ranger[i-1]:
            return []
    else:
        return energy


# E <--> k-space functions
def Etok(E, E0):
    c = 2.99792458e8  # speed of light, [m/s]
    me = 0.5109989461e6 * numpy.power(c, -2)  # mass of electron [eV-s/m]
    h = 4.1357e-15  # Planck's constant in [eV-s]
    h_bar = h / (2 * numpy.pi)
    C = 2 * me / numpy.power(h_bar, 2) * 1e-20  # [1/A**2]
    return numpy.sqrt(C * (E - E0))


def ktoE(k, E0):
    c = 2.99792458e8  # speed of light, [m/s]
    me = 0.5109989461e6 * numpy.power(c, -2)  # mass of electron [eV-s/m]
    h = 4.1357e-15  # Planck's constant in [eV-s]
    h_bar = h / (2 * numpy.pi)
    C = 2 * me / numpy.power(h_bar, 2) * 1e-20  # [1/A**2]
    return E0 + (numpy.power(k, 2) / C)