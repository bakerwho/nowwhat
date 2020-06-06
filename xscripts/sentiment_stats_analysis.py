import os
from os.path import join

import numpy as np
import pandas as pd
import time

import ast

import matplotlib.pyplot as plt
import matplotlib.cm as cm

now_folder = '/project2/jevans/aabir/NOWwhat/'
d_folder = '/project2/jevans/aabir/NOWwhat/xdata'
in_folder = join(d_folder, 'in_data')
us_folder = join(d_folder, 'us_data')

corpus_folder = join(d_folder, 'corpus')
result_folder = join(now_folder, 'resultdata')
img_folder = join(now_folder, 'img')

data = {}

data['all'] = pd.read_csv(join(result_folder, 'allnews', "all_subj_pol.csv"))
#labelpolarity = pd.read_csv(join(result_folder, 'allnews', "labelpolarity.csv"))
#labelsubjectivity = pd.read_csv(join(result_folder, 'allnews', "labelsubjectivity.csv"))

data['political'] = pd.read_csv(join(result_folder, 'polnews', "all_subj_pol.csv"))

#all_subj_pol.to_csv(join(result_folder, "politics_all_subj_pol.csv"), index=False)

for col in ['polarity', 'subjectivity']:
    data['all'][col] = data['all'][col].apply(lambda x : ast.literal_eval(x))
    data['political'][col] = data['political'][col].apply(lambda x : ast.literal_eval(x))

mids = {'polarity': 0, 'subjectivity':0.5}

ym = all_subj_pol['ym']

def box_plot(data, labels, xyt, savepath):
    plt.figure(figsize=(28, 10))
    plt.boxplot(data, labels=labels)
    plt.xlabel(xyt[0], fontsize=24)
    plt.xticks(rotation=45, fontsize=18)
    plt.ylabel(xyt[1], fontsize=24)
    plt.title(xyt[2])
    plt.savefig(savepath+'.png')
    plt.close('all')

def plt_2_trajectories(data, labels, xyt, savepath, usemeans=True, mid=0,
                        scatter=False):
    plt.figure(figsize=(28, 10))
    vals = {}
    assert len(data) == len(labels)
    if usemeans:
        means = [np.mean(line) for line in data]
    else:
        means = [mid]*len(data)
    vals['up'] = [np.array([x for x in line if x>=means[i]]) for i, line in enumerate(data)]
    vals['down'] = [np.array([x for x in line if x<means[i]]) for i, line in enumerate(data)]
    cols = {'up':'green', 'down':'red'}
    plt.plot(means, range(len(labels)), lw=2, c=cm.Orange(0.8))
    if scatter:
        for k, v in vals.items():
            ys = [y for line in v for y in line]
            xs = [xval for xval, line in enumerate(v) for y in line]
            plt.scatter(xs, ys, alpha=0.4, c=cols[k], label=k)
    else:
        for k, v in vals.items():
            ys = [np.mean(line) for line in v]
            xs = range(len(v))
            plt.scatter(xs, ys, alpha=0.4, c=cols[k], label=k)
    plt.legend()
    plt.xlabel(xyt[0], fontsize=24)
    plt.xticks(ticks=range(len(v)), labels=labels, rotation=45, fontsize=18)
    plt.xticklabels()
    plt.ylabel(xyt[1], fontsize=24)
    plt.title(xyt[2])
    plt.savefig(savepath)
    plt.close('all')

if __name__=='__main__':
    for k, v in data.items():
        for col in ['subjectivity', 'polarity']:
            box_plot(v[col], ym, ('year-month', col,f'{k} news {col}'),
                            join(img_folder, f'{k}_{col}_scores_boxplt'))
            for sc in [True, False]:
                sctxt = '_scatter' if sc else ''
                plt_2_trajectories(v[col], ym, ('year-month', col,f'{k} news {col}'),
                                join(img_folder, f'{k}_{col}_mean_up_down{sctxt}'),
                                scatter=sc)
                plt_2_trajectories(v[col], ym, ('year-month', col,f'{k} news'),
                                join(img_folder, f'{k}_{col}_mid_up_down{sctxt}'),
                                usemeans=False, mid=mids[col],
                                scatter=sc)
