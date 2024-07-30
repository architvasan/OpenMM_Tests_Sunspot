import parmed as pmd

pdb = './mp.inpcrd'
top = './mp.prmtop'

top = pmd.load_file(top, xyz=pdb)
top.save(f'mp_gmx.top')
