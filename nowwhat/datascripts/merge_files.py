import os
from os.path import join

d_folder = '/project2/jevans/aabir/NOWwhat/xdata'

in_folder, us_folder = join(d_folder, 'in_data'), join(d_folder, 'us_data')

def cleanup_code(folder):
    files = [i for i in os.listdir(folder) if os.path.isfile(join(
                        folder, i)) and '.txt' in i]
    for f in files:
        if 'text_' in f:
            print(f"renaming {f} to exclude text_")
            os.rename(join(folder, f), join(folder, f[5:]))
    files = [i for i in os.listdir(folder) if os.path.isfile(join(
                        folder, i)) and '.txt' in i]
    print(files)
    for y in range(8, 20):
        for m in range(1, 13):
            ym = str(y).zfill(2)+'-'+str(m).zfill(2)
            subset = [i for i in files if ym in i]
            #print(len(subset))
            if len(subset)>1:
                subset = sorted(subset)
                ofile = subset[0].split('.')[0][:-1] + '.txt'
                print(f"cat {' '.join(subset)} > {ofile}")
                print(f"rm {' '.join(subset)}\n")
    print('\n\n')


cleanup_code(us_folder)
