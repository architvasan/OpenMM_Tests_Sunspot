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
import pandas as pd
import numpy as np
from parmed import load_file, unit as u
from simulation_funcs import *


if __name__ == "__main__":

    def list_of_strings(arg):
        return arg.split(',')

    import argparse

    parser = argparse.ArgumentParser(description="Arguments to run equilibration",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i',
                        '--inpcrd',
                        type=str,
                        required=False,
                        default = 'struct/inpcrd1',
                        help='inpcrd file')

    parser.add_argument('-p',
                        '--prmtop',
                        type=str,
                        required=False,
                        default='struct/prmtop1',
                        help='prmtop file')


    parser.add_argument('-ec',
                        '--eqcheck',
                        required=False,
                        default='eq/eq.chk',
                        type=str,
                        help='equil checkpoint file')

    parser.add_argument('-ps',
                        '--prostate',
                        required=False,
                        default='prod0/prod0.state',
                        type=str,
                        help='prod out state file')

    parser.add_argument('-pc',
                        '--procheck',
                        required=False,
                        default='prod0/prod0.chk',
                        type=str,
                        help='prod out check file')

    parser.add_argument('-pr',
                        '--prorst',
                        required=False,
                        default='prod0/prod0.rst.chk',
                        type=str,
                        help='prod out restart file')

    parser.add_argument('-pd',
                        '--prodcd',
                        required=False,
                        default='prod0/prod0.dcd',
                        type=str,
                        help='prod out dcd file')
  
    parser.add_argument('-pl',
                        '--prolog',
                        required=False,
                        default='prod0/prod0.csv',
                        type=str,
                        help='prod out log file')

    parser.add_argument('-dt',
                        '--devtype',
                        type=str,
                        help='device type:\
                                \n cuda,\n xpu,\n cpu')

    parser.add_argument('-cpu',
                        '--cputhreads',
                        type=str,
                        required=False,
                        default="5",
                        help='number cpu threads')

    parser.add_argument('-S',
                    '--steps',
                    type=int,
                    required=False,
                    default=100000000,
                    help='number of md steps')

    parser.add_argument('-P',
                    '--precision',
                    type=str,
                    required=False,
                    default='mixed',
                    help='precision:\
                            \n double,\
                            \n mixed')

    parser.add_argument('-D',
                    '--device',
                    type=str,
                    required=False,
                    default='0',
                    help='device index\
                            \n on sunspot\
                            \n options are:\
                            \n single device (num 0-12),\
                            \n or multiple device (e.g. 0,1)')

    args = parser.parse_args()

    system, prmtop, inpcrd = load_amber_files(args.inpcrd,
                                        args.prmtop)

    
    eq_simulation, integrator = setup_sim_nomin(system,
                                            prmtop,
                                            inpcrd,
                                            args.devtype,
                                            d_ind=args.device,
                                            precision=args.precision,
                                            cpu_threads=args.cputhreads,
                                            )


    prod_1_sim = run_prod(eq_simulation, 
                        args.steps,
                        args.eqcheck,
                        args.prodcd,
                        args.prorst,
                        args.procheck,
                        args.prostate,
                        args.prolog)

