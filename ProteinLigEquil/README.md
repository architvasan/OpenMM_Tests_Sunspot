# AutomateSims

## Create protein-ligand solvated + ionized system

`python create_prot_struct.py -p pdb_file.pdb -l UNL -a ambertools_env -i leapin.in -I leapion.in`

* Created:
    - struct/system1.pdb
    - struct/inprcd1
    - struct/prmtop1

## Warm + equilibrate system

`python equilibrate.py`

## Production for system

`python production.0.py`

