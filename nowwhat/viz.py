import os
from os.path import join

import numpy as np
import pandas as pd
import time

import ast

import matplotlib.pyplot as plt

now_folder = '/project2/jevans/aabir/NOWwhat/'
d_folder = '/project2/jevans/aabir/NOWwhat/xdata'
in_folder = join(d_folder, 'in_data')
us_folder = join(d_folder, 'us_data')

corpus_folder = join(d_folder, 'corpus')
result_folder = join(now_folder, 'resultdata')
img_folder = join(now_folder, 'img')

all_subj_pol = pd.read_csv(join(result_folder, "politics_all_subj_pol.csv"))
labelpolarity = pd.read_csv(join(result_folder, "politics_labelpolarity.csv"))
labelsubjectivity = pd.read_csv(join(result_folder, "politics_labelsubjectivity.csv"))

def text_to_list(txt):
    return ast.literal_eval(txt)
