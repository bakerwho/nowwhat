import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join

cwd = join('/project2/jevans/aabir/NOWwhat/NOWdata','16-11')

subfolders = [f for f in os.listdir(cwd) if os.path.isdir(join(cwd, f))]
print(subfolders)

files = {subf : [f for f in os.listdir(join(cwd, subf)) if os.path.isfile(join(cwd, subf, f))] for subf in subfolders}
print(files)

in_files = {subf : [f for f in os.listdir(join(cwd, subf)) if os.path.isfile(join(cwd, subf, f)) and 'in' in f] for subf in subfolders}
print(in_files)

def file_preview(directory, condition=lambda x: True, num_lines=5):
    subfolders = [subf for subf in os.listdir(directory) if os.path.isdir(join(directory, subf))]
    in_files = {subf : [f for f in os.listdir(join(cwd, subf)) if os.path.isfile(join(cwd, subf, f)) and condition(f)] for subf in subfolders}
    for k, lis in in_files.items():
       print(f"\nsubfolder:\t{k}")
       for li in lis:
           print(f"\tfile:\t{li}")
           with open(join(cwd, k, li), 'r') as f:
               print(f.readlines(num_lines))
    return in_files

file_preview(cwd, lambda x: 'in' in x.lower())
