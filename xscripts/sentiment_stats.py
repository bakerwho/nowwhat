from textblob import TextBlob
from gensim.parsing.preprocessing import preprocess_string

import os
from os.path import join

import numpy as np
import pandas as pd
import time

now_folder = '/project2/jevans/aabir/NOWwhat'
d_folder = '/project2/jevans/aabir/NOWwhat/xdata'
in_folder = join(d_folder, 'in_data')
us_folder = join(d_folder, 'us_data')

corpus_folder = join(d_folder, 'corpus')

def contains(s, word):
    return word.lower() in s.lower()

class MthSentiment():
    def __init__(self, month):
        self.month = month
        self.polarities = []
        self.subjectivities = []
        self.pollines = []
        self.pols = []
        self.subjlines = []
        self.subjs = []

    def add_data(self, line, pol, subj):
        self.polarities.append(pol)
        self.subjectivities.append(subj)
        if pol > 0.9 or (pol > 0.45 and pol < 0.55) or pol < 0.1:
            self.pollines.append(line)
            self.pols.append(pol)
        if subj > 0.9 or (subj > 0.45 and subj < 0.55) or subj < 0.1:
            self.subjlines.append(line)
            self.subjs.append(subj)

    def mean_pol_subj(self):
        return np.mean(self.polarities), np.mean(self.subjectivities)

    def hilomid(self, x):
        if x > 0.9:
            return 'hi'
        elif x > 0.45 and x < 0.55:
            return 'mid'
        elif x < 0.1:
            return 'lo'

    def pol_subj_dfs(self):
        poldf = pd.DataFrame({'line':self.pollines, 'polarity':self.pols})
        subjdf = pd.DataFrame({'line':self.subjlines, 'subjectivity':self.subjs})
        poldf['label'] = poldf['polarity'].apply(self.hilomid)
        subjdf['label'] = subjdf['subjectivity'].apply(self.hilomid)
        return poldf, subjdf

def directory_sentiment(in_folder, verbose=False, filecond=None, linecond=None,
                        saveprefix=''):
    files = sorted([i for i in os.listdir(in_folder) if os.path.isfile(join(in_folder, i))])
    #print(files)
    months = []
    polmeans, subjmeans = [], []
    pcols, scols = ['y','m','line','polarity','label'], ['y','m','line','subjectivity','label']
    pdf, sdf = pd.DataFrame(None, columns=pcols), pd.DataFrame(None, columns=scols)
    for num, file in enumerate(files):
        if filecond is None or not filecond(file):
            continue
        t1 = time.time()
        print(f'file: {file}')
        month = file.split('.')[-2][-8:-3]
        #print(month)
        months.append(month)
        MS = MthSentiment(month)
        with open(join(in_folder, file), 'r') as f:
            for line in f:
                line = ' '.join(preprocess_string(line))
                if linecond is None or not linecond(line):
                    continue
                tb = TextBlob(line)
                pol, subj = tb.sentiment.polarity, tb.sentiment.subjectivity
                MS.add_data(line, pol, subj)
        #print(f'{line}, {pol}, {subj}')
        polmeans.append(MS.polarities)
        subjmeans.append(MS.subjectivities)
        pdf_, sdf_ = MS.pol_subj_dfs()
        for df in [pdf_, sdf_]:
            df['y']=month.split('-')[1]
            df['m']=month.split('-')[0]
        pdf = pd.concat((pdf, pdf_), ignore_index=True, sort=True)
        sdf = pd.concat((sdf, sdf_), ignore_index=True, sort=True)
        if num == 0 and verbose:
            t2 = time.time()
            print(f"Completed reading first file {file} | time taken = {t2-t1} s")
    pdf.reset_index(drop=True, inplace=True)
    sdf.reset_index(drop=True, inplace=True)
    meansdf = pd.DataFrame({'ym':months, 'polarity':polmeans,
                            'subjectivity':subjmeans})
    pdf.to_csv(join(now_folder, 'resultdata', f'{save_prefix}labelpolarity.csv'), index=False)
    sdf.to_csv(join(now_folder, 'resultdata', f'{save_prefix}labelsubjectivity.csv'), index=False)
    meansdf.to_csv(join(now_folder, 'resultdata', f'{save_prefix}all_subj_pol.csv'), index=False)

def check_wordlist(x, wordlist):
    for w in wordlist:
        if ' '+w+' ' in x.lower():
            return True
    return False

indian_politics_wordlist = ['election', 'politics', 'minister', 'prime minister',
        'congress', 'bjp', 'bharatiya janata party',
        'l k advani', 'lal krishna advani',
        'manmohan singh', 'sonia gandhi', 'pm manmohan singh', 'pm singh',
        'narendra modi', 'pm narendra modi', 'pm modi', 'rahul gandhi']

check_ind_politics = lambda x : check_wordlist(x, indian_politics_wordlist)

if __name__ == '__main__':
    directory_sentiment(in_folder, verbose=True, linecond=check_ind_politics,
                            save_prefix='politics_')
