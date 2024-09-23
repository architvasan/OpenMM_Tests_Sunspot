# Protein Ligand Simulations

## Create protein-ligand solvated + ionized system

`python create_prot_struct.py -p pdb_file.pdb -l UNL -a ambertools_env -i leapin.in -I leapion.in`

* Created:
    - struct/system1.pdb
    - struct/inprcd1
    - struct/prmtop1

When running simulations on Sunspot/Aurora, 

`set ZE_FLAT_DEVICE_HIERARY=FLAT`

## Warm + equilibrate system

`python equilibrate.py -h`

Available arguments are:
```
-i, --inpcrd: inpcrd file
-p, --prmtop: prmtop file
-s, --state, output state file
-c, --check, output checkpoint
-dt, --devtype, device type
    options: cuda, xpu, cpu
-cpu, --cputhreads, number cpu threads
-S, --steps, number of steps
-P, --precision, precision: double/mixed
-D, --device, device number
    single: (0-12 (xpu))
    multiple: (eg 0,1)
```

## Production for system

`python production.0.py -h`

Available arguments are:

```
-i, --inpcrd: inpcrd file
-p, --prmtop: prmtop file
-ec, --eqcheck, equil checkpoint
-ps, --prostate, prod state file
-pc, --procheck, prod checkpoint
-pr, --prorst, prod restart
-pd, --prodcd, prod dcd
-pl, --prolog, prod log
-dt, --devtype, device type
    options: cuda, xpu, cpu
-cpu, --cputhreads, number cpu threads
-S, --steps, number of steps
-P, --precision, precision: double/mixed
-D, --device, device number
    single: (0-12 (xpu))
    multiple: (eg 0,1)
```

