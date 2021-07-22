"""Functions for the tracks model"""

import math

from scipy import constants
from scipy import optimize

from actinrings import analytical


def calc_ring_energy(R_ring, N, Nmin, params):
    R_ring_max = analytical.calc_max_radius(params['Lf'], Nmin)
    overlap_L = 2*math.pi*(R_ring_max - R_ring)/Nmin
    overlaps = Nmin + 2*(N - Nmin)
    sliding_energy = overlaps*analytical.calc_sliding_energy(overlap_L, params)
    bending_energy = N*analytical.calc_bending_energy(R_ring, params)
    total_energy = sliding_energy + bending_energy

    return total_energy


def calc_ring_force(R_ring, N, Nmin, params):
    sliding_force = (2*math.pi*constants.k*params['T']*(2*N - Nmin) *
                     math.log(params['Xc'] / params['kd'] + 1) /
                     (params['delta']*Nmin))
    bending_force = -params['EI']*N*params['Lf']/R_ring**3
    total_force = sliding_force + bending_force

    return total_force


def calc_equilibrium_ring_radius(N, Nmin, params):
    num = params['EI']*N*params['delta']*params['Lf']*Nmin
    denom = (2*math.pi*params['T']*constants.k *
             math.log(params['Xc']/params['kd'] + 1)*(2*N - Nmin))

    return (num/denom)**(1/3)


def calc_equilibrium_radius_numerical(N, Nmin, params):
    max_radius = analytical.calc_max_radius(params['Lf'], Nmin)
    min_radius = max_radius/2
    res = optimize.minimize_scalar(calc_ring_energy,
                                   method='bounded',
                                   bounds=(1e-30, 2*max_radius),
                                   args=(N, Nmin, params),
                                   options={'xatol': 1e-12})

    radius = res.x
    if (radius > max_radius):
        print('Ring will fall apart under these conditions')
        print(f'Max radius {max_radius}, calculated radius: {radius}')
        raise

    elif (radius < min_radius):
        print('Ring will violate overlap assumptions under these conditions')
        print(f'Min radius {min_radius}, calculated radius: {radius}')
        raise

    return res.x