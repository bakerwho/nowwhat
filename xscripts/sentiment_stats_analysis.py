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
ylims = {'polarity': (-1.1, 1.1), 'subjectivity':(-0.1, 1.1)}

ym = data['all']['ym'].apply(lambda x: '/'.join(reversed(x.split('-'))))

def box_plot(data, labels, xyt, savepath):
    plt.figure(figsize=(28, 10))
    plt.boxplot(data, positions=range(len(data)), labels=labels)
    plt.xlabel(xyt[0], fontsize=24)
    plt.xticks(rotation=45, fontsize=18)
    plt.ylabel(xyt[1], fontsize=24)
    plt.title(xyt[2])
    plt.savefig(savepath+'.png', bbox_inches='tight')
    plt.close('all')

def plt_2_trajectories(data, labels, xyt, savepath, usemeans=True, mid=0,
                        plttype='scatter', **kwargs):
    plt.figure(figsize=(28, 10))
    vals = {}
    assert len(data) == len(labels)
    ylims = kwargs.pop('ylims', (0,1))
    if usemeans:
        means = [np.mean(line) for line in data]
    else:
        means = [mid]*len(data)
    vals['up'] = [np.array([x for x in line if x>=means[i]]) for i, line in enumerate(data)]
    vals['down'] = [np.array([x for x in line if x<means[i]]) for i, line in enumerate(data)]
    cols = {'up':'green', 'down':'red'}
    plt.plot(range(len(labels)), means, lw=2, c=cm.Oranges(0.8))
    plt.axhline(y=mid, c=cm.Greys(0.8), alpha=0.4)
    if 'scatter' in plttype:
        for k, v in vals.items():
            ys = [y for line in v for y in line]
            xs = [xval for xval, line in enumerate(v) for y in line]
            plt.scatter(xs, ys, alpha=0.25, c=cols[k], label=k)
    if 'mean' in plttype:
        for k, v in vals.items():
            ys = [np.mean(line) for line in v]
            xs = range(len(v))
            plt.plot(xs, ys, alpha=0.25, c=cols[k], label=k)
    if 'box' in plttype:
        for k, v in vals.items():
            plt.boxplot(v, positions=range(len(data)), label=k
                        boxprops={'c':cols[k]})
    plt.legend()
    plt.xlabel(xyt[0], fontsize=24)
    plt.xticks(ticks=range(len(v)), labels=labels, rotation=45, fontsize=12,
                        ha='center')
    plt.ylabel(xyt[1], fontsize=24)
    plt.title(xyt[2], fontsize=28)
    plt.ylim(*ylims)
    plt.savefig(savepath+'.png', bbox_inches='tight')
    plt.close('all')

if __name__=='__main__':
    for k, v in data.items():
        for col in ['subjectivity', 'polarity']:
            box_plot(v[col], ym, ('year-month', col,f'{k} news {col}'),
                            join(img_folder, f'{k}_{col}_scores_boxplt'))
            for usemeans in [True, False]:
                mt = '_mn' if usemeans else ''
                for plttype in ['_scatter', '_box', '_box_mean', '_mean']:
                    plt_2_trajectories(v[col], ym,
                            ('year-month', col,f'{k} news {col}'),
                            join(img_folder, f'{k}_{col}{mt}_up_down{plttype}'),
                            usemeans=usemeans, mid=mids[col], scatter=sc,
                            ylims=ylims[col])
