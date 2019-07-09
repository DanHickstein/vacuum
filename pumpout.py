#! /usr/bin/env python
# 2014-10-13 by Dan Hickstein
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

def main():
    diam_micron = np.linspace(1,100,200)
    diam_cm = diam_micron * 1e-4
    
    length = 6  # length in cm
    
    pressure = 1e-3  # pressure in mbar.
    
    volumes = length * (0.5*diam_cm)**2 * np.pi
    volumes = volumes * 1e-3 # convert cm3 to liters
    
    conds = Cknud(pressure, length, diam_cm)
    
    fig, axs = plt.subplots(2,1,figsize=(8,8))
    
    axs[0].plot(diam_micron, conds)
    axs[0].set_ylabel('Conductance (L/s)')
    
    pumpout = volumes/conds
    
    axs[1].plot(diam_micron, pumpout)
    
    axs[1].set_yscale('log')
    
    axs[1].axvline(11, color='r', ls='dashed')
    
    axs[1].set_ylabel('Time for pumpout (sec)')
    
    for ax in axs:
        ax.grid(color='k', alpha=0.2)
        ax.set_xlabel('Tube diameter (cm)')
    
    plt.savefig('pumpout of tubes.png')

if __name__ == '__main__':
    main()
