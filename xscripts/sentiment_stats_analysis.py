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

"""
all_subj_pol['y'] = all_subj_pol.ym.apply(lambda x : int(x[:2]))
all_subj_pol['m'] = all_subj_pol.ym.apply(lambda x : int(x[-2:]))

all_subj_pol['meanpol'] = all_subj_pol.polarity.apply(lambda x : np.mean(x))
all_subj_pol['stdpol'] = all_subj_pol.polarity.apply(lambda x : np.std(x))
all_subj_pol['meansubj'] = all_subj_pol.subjectivity.apply(lambda x : np.mean(x))
all_subj_pol['stdsubj'] = all_subj_pol.subjectivity.apply(lambda x : np.std(x))
"""

#all_subj_pol.to_csv(join(result_folder, "politics_all_subj_pol.csv"), index=False)

for col in ['polarity', 'subjectivity']:
    all_subj_pol[col] = all_subj_pol[col].apply(lambda x : ast.literal_eval(x))

subj = [np.array(i) for i in all_subj_pol.polarity]
pol = [np.array(i) for i in all_subj_pol.subjectivity]
ym = all_subj_pol[ym]
plt.boxplot(subj, labels=ym)
plt.savefig(join())
