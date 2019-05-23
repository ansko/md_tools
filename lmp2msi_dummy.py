'''
A very basic tool to convert lmp datafile into msi format:
  only atoms + bonds
  only orthogonal box
  only 1 molecule(?)
'''


from datafile_content import DatafileContent


unknown_number_by_element = {
    'H': 0,
    'O': 8,
    'C': 6,
    'N': 7
}


def util_atom_element(atom):
    return {
        1: 'Al',
        2: 'Mg',
        3: 'Si',
        4: 'O', 5: 'O', 6: 'O', 7: 'O', 15: 'O',
        8: 'H', 12: 'H', 13: 'H',
        9: 'N', 16: 'N', 17: 'N',
        10: 'C', 11: 'C', 14: 'C'
    }[atom['atom_type_id']]


def util_atom_ff_type(atom):
    return {
        1: 'ao',
        2: 'mgo',
        3: 'st',
        4: 'ob',
        5: 'oh',
        6: 'obts',
        7: 'ohs',
        8: 'ho',
        9: 'n4',
        10: 'c2',
        11: 'c3',
        12: 'h',
        13: 'hn',
        14: "c'",  # Attention! apostrophe in atom type!
        15: "o'",  # Attention! apostrophe in atom type!
        16: 'n2',
        17: 'n'
    }[atom['atom_type_id']]


if __name__ == '__main__':
    lmp_fname = 'modifier.data'
    msi_fname = lmp_fname.split('.')[0] + '.msi'

    dfc = DatafileContent(lmp_fname)
    xlo = dfc.xlo
    ylo = dfc.ylo
    zlo = dfc.zlo

    f = open(msi_fname, 'w')
    tmppr = lambda *x : print(*x, file=f)
    atom_remap = {}

    idx = 1
    tmppr('# MSI CERIUS2 DataModel File Version 4 0')  # comment
    tmppr('(1 Model')
    idx += 1
    msi_id = 0
    tmppr('   (A I PeriodicType 100)')
    tmppr('   (A C SpaceGroup "1 1")')
    tmppr('   (A D A3 ({0} 0.0 0.0))'.format(dfc.xhi - xlo))
    tmppr('   (A D B3 (0.0 {0} 0.0))'.format(dfc.yhi - ylo))
    tmppr('   (A D C3 (0.0 0.0 {0}))'.format(dfc.zhi - zlo))
    tmppr('  (A I Monomer {0})'.format(idx))
    for atom in dfc.atoms:
        atom_remap[atom['atom_id']] = idx
        el = util_atom_element(atom)
        tmppr('      ({0} Atom'.format(idx))
        tmppr('        (A C ACL "{0} {1}")'.format(
            unknown_number_by_element[el], el))
        tmppr('        (A C Label "{0}{1}")'.format(el, idx))
        tmppr('        (A D XYZ ({0} {1} {2}))'.format(
            atom['x'] + xlo, atom['y'] + ylo, atom['z'] + zlo))
        tmppr('        (A I Id {0})'.format(msi_id))
        tmppr('        (A F Charge {0})'.format(atom['q']))
        tmppr('        (A C FFType "{0}")'.format(util_atom_ff_type(atom)))
        tmppr('      )')
        idx += 1
        msi_id += 1
    for bond in dfc.bonds:
        tmppr('      ({0} Bond'.format(idx))
        tmppr('        (A O Atom1 {0})'.format(atom_remap[bond['atom_one_id']]))
        tmppr('        (A O Atom2 {0})'.format(atom_remap[bond['atom_two_id']]))
        tmppr('      )')
        idx += 1
    tmppr(')')
