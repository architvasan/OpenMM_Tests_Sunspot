#import MDAnalysis as mda
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

    parser.add_argument('-s',
                        '--state',
                        required=False,
                        default='eq/eq.state',
                        type=str,
                        help='output state file')

    parser.add_argument('-c',
                        '--check',
                        required=False,
                        default='eq/eq.chk',
                        type=str,
                        help='checkpoint file')

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
                    default=500000,
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

    eq_simulation = run_eq(args.inpcrd,
                        args.prmtop,
                        args.state,
                        args.check,
                        args.devtype,
                        mdsteps=args.steps,
                        precision=args.precision,
                        d_ind=args.device,
                        cpu_threads=args.cputhreads)

