from shutil import copyfile
import os
from os.path import join
from os import listdir

folder = '/project2/jevans/aabir/NOWwhat'
d_folder = join(folder, 'data', 'text')
s_folder = join(folder, 'data', 'sources')

in_target = join(folder, 'xdata', 'in_data')
us_target = join(folder, 'xdata', 'us_data')
src_target = join(folder, 'xdata', 'src_data')


def copyfiles(d_folder, target, cond=lambda x: True):
    os.makedirs(target, exist_ok=True)
    for f in listdir(d_folder):
        new_f = join(d_folder, f)
        if not os.path.isdir(new_f):
            continue
        files = listdir(new_f)
        cond_files = [i for i in files if cond(i)]
        for i in cond_files:
            src = join(d_folder, new_f, i)
            print(f"\tcopying {src}")
            copyfile(src, join(target, i.lower()))

if __name__ == '__main__':
    copyfiles(d_folder, in_target, cond=lambda x: 'IN' in x.lower() and '.txt' in x)
    copyfiles(d_folder, us_target, cond=lambda x: 'US' in x.lower() and '.txt' in x)
    copyfiles(s_folder, src_target, cond=lambda x: '.txt' in x)
