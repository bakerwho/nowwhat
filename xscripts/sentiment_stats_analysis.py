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

#all_subj_pol.to_csv(join(result_folder, "politics_all_subj_pol.csv"), index=False)

for col in ['polarity', 'subjectivity']:
    all_subj_pol[col] = all_subj_pol[col].apply(lambda x : ast.literal_eval(x))

subj = [np.array(i) for i in all_subj_pol.polarity]
pol = [np.array(i) for i in all_subj_pol.subjectivity]
ym = all_subj_pol['ym']

def box_plot(data, labels, xyt, savepath):
    plt.figure(figsize=(30, 10))
    plt.boxplot(subj, labels=ym)
    plt.xlabel(xyt[0])
    plt.xticks(rotation=45)
    plt.ylabel(xyt[1])
    plt.title(xyt[2])
    plt.savefig(savepath)
    plt.close('all')

box_plot(subj, ym, ('year-month', 'subjectivity score',''),
                    join(img_folder, 'subjectivity_scores.png'))
box_plot(pol, ym, ('year-month', 'polarity score',''),
                    join(img_folder, 'polarity_scores.png'))
