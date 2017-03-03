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
    fig = plt.figure(figsize=(10,7))
    ax = plt.subplot(111)

    # KF 16 is 3/4inch ID - 2 cm
    # KF 25 is 1 inch ID - 2.5 cm
    # FK 40 is 1.5 inch ID - 3.8 cm
    # KF 50 is 2 inch ID - 5.0 cm

    for length in (100,1000):
        for diam in (2.5,3.8,5):
            if diam==3.8:
                sty='dashed'
                txt='KF40'
            elif diam==2.5:
                sty='dotted'
                txt='KF25'
            elif diam==5:
                sty='solid'
                txt='KF50'
            else:
                sty='solid'
                txt=''
    		
            if   length==100:  color='red'
            elif length==1000: color='blue'
            else:        color='black'
            ax.plot(pressure,Cknud(pressure,length=length,diameter=diam),
    			    label='%.1f cm diameter (%s), %.0f meter length'%(diam,txt,length/100.),linestyle=sty,color=color)

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.axhline(260,label='260 L/s (HiPace 300)',color='m',alpha=0.2,lw=2)
    ax.axhline(71,label='71 L/s (HiPace 80)',color='m',alpha=0.2,lw=1)
    ax.axhline(7.8,label='7.8 L/s (ACP 28)',color='k',alpha=0.2,lw=2)
    ax.axhline(4,label='4.2 L/s (ACP 15)',color='k',alpha=0.2,lw=1)

    ax.set_title('Conductance of tubing using Knudson equation\n(valid for viscous and molecular flow)')
    ax.set_xlabel('Pressure (mbar)')
    ax.set_ylabel('Conductance (L/s)')

    leg = ax.legend(loc='upper left',fontsize='small'); leg.draw_frame(False)

    plt.savefig('Tubing conductance 1.1.pdf',dpi=300)
    plt.show()

if __name__ == '__main__':
    main()
