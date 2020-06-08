import os
from os.path import join

import numpy as np
import pandas as pd
import time

import ast

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import seaborn as sns

sns.set_style('whitegrid')

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

def box_plot(data, labels, xyt, savepath, means=False, toprint=False, **kwargs):
    plt.figure(figsize=(28, 10))
    ylims = kwargs.pop('ylims', (0,1))
    dt = plt.boxplot(data, positions=range(len(data)), labels=labels)
    if means:
        plt.plot(range(len(data)), [np.mean(x) for x in data], label='mean')
    plt.xlabel(xyt[0], fontsize=20)
    plt.xticks(ticks=range(len(v)), labels=labels, rotation=45, fontsize=10,
                        ha='center')
    plt.ylabel(xyt[1], fontsize=20)
    plt.title(xyt[2], fontsize=24)
    plt.ylim(*ylims)
    plt.legend()
    if savepath is not None:
        plt.savefig(savepath+'.png', bbox_inches='tight')
    plt.close('all')
    return dt

def outlier_ct(dt, mid, labels, xyt, savepath):
    outliers = [x.get_xydata() for x in dt['fliers']]
    up_cts, down_cts = [], []
    for line in outliers:
        up_cts.append(0)
        down_cts.append(0)
        for (x,y) in line:
            if y >= mid:
                up_cts[-1] += 1
            else:
                down_cts[-1] += 1
    cols = ['green', 'red']
    labs = ['high outliers', 'low outliers']
    plt.figure(figsize=(28, 10))
    for i, ydata in enumerate([up_cts, down_cts]):
        plt.plot(range(len(ydata)), up_cts, c=cols[i], label=labs[i])
    plt.xlabel(xyt[0], fontsize=20)
    plt.xticks(ticks=range(len(outliers)), labels=labels, rotation=45, fontsize=10,
                        ha='center')
    plt.ylabel(xyt[1], fontsize=20)
    plt.title(xyt[2], fontsize=24)
    plt.ylim(*ylims)
    plt.legend()
    if savepath is not None:
        plt.savefig(savepath+'_outlier_ct.png', bbox_inches='tight')
    plt.close('all')


def plt_2_trajectories(data, labels, xyt, savepath, usemeans=True, mid=0,
                        plttype='scatter', **kwargs):
    plt.figure(figsize=(30, 10))
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
    plt.plot(range(len(labels)), means, lw=4, c=cm.Oranges(0.8))
    plt.axhline(y=mid, c=cm.Greys(0.8), alpha=0.7)
    for x in range(0, len(means), 12):
        plt.axvline(x=x, c=cm.Greys(0.8), alpha=0.7, lw=1.5)
    if 'scatter' in plttype:
        for k, v in vals.items():
            ys = [y for line in v for y in line]
            xs = [xval for xval, line in enumerate(v) for y in line]
            plt.scatter(xs, ys, alpha=0.25, c=cols[k], label=k)
    if 'mean' in plttype:
        for k, v in vals.items():
            ys = [np.mean(line) for line in v]
            xs = range(len(v))
            plt.plot(xs, ys, alpha=0.8, lw=2, c=cols[k], label=k)
    if 'box' in plttype:
        for k, v in vals.items():
            plt.boxplot(v, positions=range(len(data)),
                        boxprops={'c':cols[k]})
    plt.legend()
    plt.xlabel(xyt[0], fontsize=20)
    plt.xticks(ticks=range(len(v)), labels=labels, rotation=45, fontsize=10,
                        ha='center')
    plt.ylabel(xyt[1], fontsize=20)
    plt.title(xyt[2], fontsize=24)
    plt.ylim(*ylims)
    plt.savefig(savepath+'.png', bbox_inches='tight')
    plt.close('all')

if __name__=='__main__':
    for k, v in data.items():
        for col in ['subjectivity', 'polarity']:
            for usemeans in [True, False]:
                dt = box_plot(v[col], ym, ('', col,f'{k} news {col}'),
                            join(img_folder, f'{k}_{col}_scores_boxplot'),
                            means=usemeans, ylims=ylims[col])
                if usemeans:
                    outlier_ct(dt, mids[col], ym,
                            ('', '#',f'{k} news {col} outliers'),
                            join(img_folder, f'{k}_{col}_outliers'))
                mt = '_mn' if usemeans else ''
                for plttype in ['_box', '_box_mean', '_mean']:
                    plt_2_trajectories(v[col], ym,
                            ('', col,f'{k} news {col}'),
                            join(img_folder, f'{k}_{col}{mt}_up_down{plttype}'),
                            usemeans=usemeans, mid=mids[col], plttype=plttype,
                            ylims=ylims[col])

"""
usemeans=False
col='subjectivity'
k = 'political'
v = data[k]
dt = box_plot(v[col], ym, ('year-month', col,f'{k} news {col}'),
            None, means=usemeans, ylims=ylims[col])
"""
