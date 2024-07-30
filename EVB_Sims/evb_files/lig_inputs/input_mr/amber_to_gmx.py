import parmed as pmd

pdb = './mr.inpcrd'
top = './mr.prmtop'

top = pmd.load_file(top, xyz=pdb)
top.save(f'mr_gmx.top')
