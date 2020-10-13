#!/usr/bin/env python
import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# volume factors for each lattice type
factor = {'cubic' : 1.,
          'bcc' : 1./2.,
          'fcc' : 1./4.,
          'diamond' : 1./4.}


def eos_murnaghan(vol, E0, B0, BP, V0):
    """ Murnaghan equation of state (energy as a function of volume).
    From PRB 28,5480 (1983). """
   
    return E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1)+1) - V0*B0/(BP-1)

def read_data( filename ):
    """ Function that read the results from a data file and returns the
    lattice type and the volume and energy vectors as numpy arrays."""

    # read first word at first line
    with open( filename, 'r' ) as f:
        lattice = f.readline().split()[0] 


    # read volumen and energy results 
    data = np.loadtxt(filename, skiprows=1)    

    return lattice, factor[lattice]*data[:,0]**3, data[:,1]

def fit_murnaghan(volume, energy ):
    """ Function that fits the results to a Murnaghan EOS. """

    # fit a parabola for initial parameter guess
    p_coefs = np.polyfit(volume, energy, 2)
    # minimum of the parabola dE/dV = 0 ( p_coefs = [c,b,a] )
    p_min = - p_coefs[1]/(2.*p_coefs[0])
    # warn if min volume not in result range 
    if (p_min < volume.min() or p_min > volume.max()):
        print "Warning: minimum volume not in range of results"
    # goundstate energy estimation form parabola minimum    
    E0 = np.polyval(p_coefs, p_min)
    # bulk modulus estimation
    B0 = 2.*p_coefs[2]*p_min

    # initial parameters (BP is usually small)
    init_par = [E0, B0, 4, p_min]
    best_par, cov_matrix = curve_fit(eos_murnaghan, volume, energy, p0 = init_par)

    return best_par

def fit_and_plot(filename):
    """ Function that reads data from a filename and fits a Murnaghan EOS.
    The fitted parameters and a plot are returned. """
    # read data from file
    lattice, volume, energy = read_data(filename)   
    # fit data to Murnaghan EOS
    best_par = fit_murnaghan(volume, energy)
    # print optimal paramaters
    print "Fit parameters:"
    print " V0     =  {:1.4f} A^3 ".format(best_par[3])
    print " E0     =  {:1.4f} eV  ".format(best_par[0])
    print " B(V0)  =  {:1.4f} eV/A^3".format(best_par[1])
    print " B'(VO) =  {:1.4f} ".format(best_par[2])
    # theoretical lattice constant
    lattice_const = (best_par[3]/factor[lattice])**(1./3.)
    print "Theoretical lattice constant: {:1.4f} A".format(lattice_const)

    # generate Murnaghan model with fitted parameters
    m_volume = np.linspace(volume.min(), volume.max(), 1000) 
    m_energy = eos_murnaghan(m_volume, *best_par) 
    
    # plot data and model together
    lines = plt.plot(volume, energy, 'ok', m_volume, m_energy, '--r' )
    plt.xlabel(r"Volume [$\rm{A}^3$]")
    plt.ylabel(r"Energy [$\rm{eV}$]")

    return  best_par, lines


# to be executed when called as a script
if __name__ == "__main__":
    # parse filename argument
    if len(sys.argv) < 2:
        print 'Command usage: python fit_results.py filename [fig_filename]'
        sys.exit()
    else:
        filename = sys.argv[1] 
        # check if figure should be saved to file
        if len(sys.argv) > 2:
            fig_filename = sys.argv[2]
        else:
            fig_filename = None

    # fit and plot data from file
    fit_and_plot(filename)
    # draw plot 
    plt.draw()

    if fig_filename:
        plt.savefig(fig_filename)
    else:
        plt.show()
    
    sys.exit()

    
    

    





    
