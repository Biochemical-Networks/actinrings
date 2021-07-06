"""Functions for calculating analytical results"""


import math

import scipy.constants as constants
import scipy.optimize as optimize


def calc_I_circle(R_filament):
    return math.pi*R_filament**4/4


def calc_I_square(height):
    return height**4/12


def calc_youngs_modulus(R_filament, EI):
    I_circle = calc_I_circle(R_filament)

    return EI/I_circle


def calc_beam_energy_cuboid_ring(length, height, R_ring):
    """Assumes that height and width are equal"""

    # I could make the cuboid approximation more accurate than assuming the
    # height of the beam is twice the radius
    R_filament = height/2
    E = calc_youngs_modulus(R_filament)
    I_square = calc_I_square(height)

    return 3*E*I_square*length/(4*R_ring**2)


def calc_wlc_energy_cuboid_ring(length, height, R_ring):
    """Assumes that height and width are equal"""

    # I could make the cuboid approximation more accurate than assuming the
    # height of the beam is twice the radius
    R_filament = height/2
    E = calc_youngs_modulus(R_filament)
    I_square = calc_I_square(height)

    return E*I_square*length/(2*R_ring**2)


def calc_sliding_force(T, X_C, kd, delta):
    return -constants.k*T/delta*math.log(1 + X_C/kd)


def calc_sliding_energy(T, X_C, kd, delta, overlap_L):
    return overlap_L*calc_sliding_force(T, X_C, kd, delta)


def calc_wlc_bending_radial_force(EI, filament_L, R_ring):
    return EI*filament_L/R_ring**3


def calc_wlc_bending_radial_energy(EI, filament_L, R_ring):
    return EI*filament_L/(2*R_ring**2)


def calc_force_balanced_radius(T, X_C, kd, delta, filament_L, EI):
    num = EI*filament_L*delta
    denom = 2*math.pi*constants.k*T*math.log(1 + X_C/kd)

    return (num/denom)**(1/3)


def calc_force_balanced_concentration(R_ring, T, kd, delta, filament_L, EI):
    return kd*(math.exp(EI*filament_L*delta /
                        (2*math.pi*R_ring**3*constants.k*T)) - 1)


def calc_circular_double_overlap_ring_energy(R_ring, T, X_C, kd, delta,
                                             filament_L, N, EI):
    R_ring_max = N*filament_L/(2*math.pi)
    overlap_L = 2*math.pi*(R_ring_max - R_ring)/N
    sliding_energy = N*calc_sliding_energy(T, X_C, kd, delta, overlap_L)
    wlc_bending_energy = N*calc_wlc_bending_radial_energy(EI, filament_L,
                                                          R_ring)
    total_energy = sliding_energy + wlc_bending_energy

    return total_energy


def calc_energy_minimized_radius(T, X_C, kd, delta, filament_L, EI):
    num = EI*delta*filament_L
    denom = 2*math.pi*T*constants.k*math.log(1 + X_C/kd)

    return (num/denom)**(1/3)


def calc_energy_minimized_concentration(R_ring, T, kd, delta, filament_L, EI):
    return kd*(math.exp(EI*filament_L*delta /
                        (2*math.pi*R_ring**3*constants.k*T)) - 1)
