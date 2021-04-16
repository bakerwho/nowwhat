import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import join

try:
    folder = sys.argv[1]
except:
    folder = '16-11'

cwd = join(os.getcwd(),folder)

print(os.listdir(cwd))
subfolders = [f for f in os.listdir(cwd) if os.path.isdir(f)]
print(subfolders)

files = {subf : [os.listdir(join(cwd, subf))] for subf in subfolders}
print(files)

