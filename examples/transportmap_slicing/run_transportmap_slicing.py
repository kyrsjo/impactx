#!/usr/bin/env python3
#
# Copyright 2022-2025 ImpactX contributors
# Authors: Axel Huebl, Chad Mitchell, Kyrre Sjobak
# License: BSD-3-Clause-LBNL
#
# -*- coding: utf-8 -*-

from impactx import ImpactX, distribution, elements
import math

sim = ImpactX()

# set numerical parameters and IO control
sim.particle_shape = 2  # B-spline order
sim.space_charge = False
# sim.diagnostics = False  # benchmarking
sim.slice_step_diagnostics = True

# domain decomposition & space charge mesh
sim.init_grids()

#Beam parameters
kin_energy_MeV = 200  # reference energy
bunch_charge_C = 1.0e-9  # used with space charge
npart = 10000  # number of macro particles

betax = 5.8163 #[m]
betay = 5.8163 #[m]

alphax = 0.0 #[-]
alphay = 0.0 #[-]

gammax = (1+alphax**2)/betax #[1/m]
gammay = (1+alphay**2)/betay #[1/m]

emitnx = 10e-6 #[m]
emitny = 10e-6 #[m]

#   reference particle
ref = sim.particle_container().ref_particle()
ref.set_charge_qe(-1.0).set_mass_MeV(0.510998950).set_kin_energy_MeV(kin_energy_MeV)


emitx = emitnx/ref.beta_gamma
emity = emitny/ref.beta_gamma

#   particle bunch
distr = distribution.Waterbag(
    lambdaX=3.9984884770e-5,
    lambdaY=3.9984884770e-5,
    lambdaT=1.0e-3,
    lambdaPx=2.6623538760e-5,
    lambdaPy=2.6623538760e-5,
    lambdaPt=2.0e-3,
    muxpx=-0.846574929020762,
    muypy=0.846574929020762,
    mutpt=0.0,
)
#   particle bunch
distr = distribution.Gaussian(
    lambdaX=math.sqrt(emitx/gammax),
    lambdaY=math.sqrt(emity/gammay),
    lambdaT=1.0e-3,
    lambdaPx=math.sqrt(emitx/betax),
    lambdaPy=math.sqrt(emity/betay),
    lambdaPt=2.0e-3,
    muxpx=alphax/math.sqrt(betax*gammax),
    muypy=alphay/math.sqrt(betay*gammay),
    mutpt=0.0,
)
sim.add_particles(bunch_charge_C, distr, npart)


#el_apl1   = elements.ChrPlasmaLens(ds=0.02, k=100, nslice=ns)


#Elements and lattice - all 3 possibilities for quad polarity
ns = 10  # number of slices per ds in the element
lattice = [
    elements.Drift(ds=1.0, nslice=ns),
    elements.Quad(name="Q1", ds=0.226, k=8.16, nslice=ns),
    elements.Drift(ds=0.224, nslice=ns),
    elements.Quad(name="Q2", ds=0.226, k=-12.01, nslice=ns),
    elements.Drift(ds=0.224, nslice=ns),
    elements.Quad(name="Q3", ds=0.226, k=0, nslice=ns)
]
sim.lattice.extend(lattice)

# run simulation
sim.init_envelope(ref,distr)
sim.track_envelope()

# clean shutdown
sim.finalize()
