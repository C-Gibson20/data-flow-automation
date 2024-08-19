import pandas as pd

read_fname = ''
write_fname = read_fname

dfile = pd.read_excel(read_fname)
dframe = pd.DataFrame(dfile)

for compound in dframe.Compound:
    if '-' in str(compound):
        compound_mod = '-'.join(str(compound).split('-')[:2])
        dframe.Compound.replace(compound, compound_mod, inplace=True)

dframe.to_excel(read_fname, index=False)
