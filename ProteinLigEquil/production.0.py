import MDAnalysis as mda
import time
from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout, exit, stderr
from parmed import unit as u
from copy import deepcopy
import sys
from sys import stdout
#from openff.toolkit import Molecule
#from openmmforcefields.generators import GAFFTemplateGenerator
import pandas as pd
import numpy as np
from parmed import load_file, unit as u
from simulation_funcs import *

inpcrd_fil = 'struct/inpcrd1'
prmtop_fil = 'struct/prmtop1'
eq_st = 'eq/eq.state'
eq_chkpt = 'eq/eq.chk'
d_ind = 0,1
prod_steps = 100000000
prod_chkpt = 'prod0/prod0.chk'
prod_st = 'prod0/prod0.state'
prod_dcd = 'prod0/prod0.dcd'
prod_rst = 'prod0/prod0.rst.chk'
prod_log = 'prod0/prod0.csv'

system, prmtop, inpcrd = load_amber_files(inpcrd_fil,
                                        prmtop_fil)

eq_simulation, integrator = setup_sim_nomin(system,
                                            prmtop,
                                            inpcrd,
                                            d_ind=d_ind)

eq_simulation.context.setParameter('k', 0)

prod_1_sim = run_prod(eq_simulation, 
                        prod_steps,
                        eq_chkpt,
                        prod_dcd,
                        prod_rst,
                        prod_chkpt,
                        prod_st,
                        prod_log)
