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
eq_simulation = run_eq(inpcrd_fil, prmtop_fil, eq_st, eq_chkpt)

