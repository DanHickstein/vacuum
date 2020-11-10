#! /usr/bin/env python
# 2014-10-13 by Dan Hickstein
# 2020-11-09 - Updated to include price
import numpy as np
import matplotlib.pyplot as plt

pressure = np.logspace(-3,3,100)

def Cknud(pressure,length,diameter):
    """ The function calculates the conductance of a tube (in liters/sec),
    given the pressure drop across the tube, the length of the tube,
    and the diameter of the tube. Note that when the pressure drop is high,
    you can just use the pressure on the high-pressure side of the tube.

    This uses Equation 1.26, on page 16 of the Leybold handbook:
    https://www3.nd.edu/~nsl/Lectures/urls/LEYBOLD_FUNDAMENTALS.pdf

    Parameters
    ----------
    pressure : float
        The pressure drop across the tube in mBar
        1 mBar = 0.750062 Torr
        1 mBar = 0.000986923 atmospheres
        1 mBar = 0.0145038 psi (pounds-force per square inch)

    length : float
        the length of the tube in cm

    diameter : float
        the diameter of the tube in cm

    Returns
    -------
    conductance : float
        the conductance of the tube in liters/second
    """
    p = pressure; l = length; d = diameter
    conductance = 135*d**4/l*p + 12.1*d**3/l* (1+192*d*p)/(1+237*d*p)
    return conductance


def print_conductances(label='', press=1000, leng=3, diam=0.015, price=1.0):
    '''
    press is in mbar
    leng is in cm
    diam is in cm
    price is dollars per liter atm
    '''

    cond = Cknud(press, leng, diam)

    atm_liters_per_sec = cond*press/1013.25
    cost_per_sec = atm_liters_per_sec * price
    cost_per_hour = cost_per_sec * 3600.0

    print(label)
    print('Inputs')
    print('  Diameter: %.2e m \n  Length: %.2e m\n  Pressure: %.2e mbar \n  Price: %.4f dollars per liter atm'%(diam*1e-2, leng*1e-2, press, price))

    print('Outputs')
    print('  Conductance: %.2e liters/sec'%cond)
    print('  Mass flow: %.2e mbar L/sec'%(cond*press))
    print('  Mass flow: %.2e atm L/sec'%(atm_liters_per_sec))
    print('  Mass flow: %.2e atm L/hour'%(atm_liters_per_sec*3600))

    print('  Cost: %.2e dollars per sec\n  Cost: %.2e dollars per hour. \n\n\n'%(cost_per_sec, cost_per_hour))

if __name__ == '__main__':
    print_conductances(label='Neon (best case)',  press=200, leng=3, diam=0.015, price=0.5)
    print_conductances(label='Neon (worst case)', press=1000, leng=1.5, diam=0.015, price=1.0)
    print_conductances(label='Xenon (best case)', press=15, leng=3, diam=0.015, price=25)
    print_conductances(label='Xenon (worst case)', press=40, leng=1.5, diam=0.015, price=35)
