from collections import Counter, defaultdict
import gensim
from gensim.models import Word2Vec

import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join
import pandas as pd
import re

datafolder = './data'
year = 16

wiki_files = [join(datafolder, 'wikitext-103-raw', x) for x in os.listdir(join(datafolder, 'wikitext-103-raw'))]
wiki_files = dict(zip(['test', 'train', 'val'], sorted(wiki_files)))

folders = [join(datafolder, f) for f in os.listdir(datafolder) if str(year) in f]
files = [join(folderpath, f) for folderpath in folders for f in os.listdir(folderpath)]

def iterate_over_txtfiles(datapath, txtfunc=lambda x: None, verbose=True):
    print(f"{datapath} contains {len(os.listdir(datapath))} files/folders")
    for y in range(10, 22):
        for m in range(1, 13):
            y, m = str(y), str(m).zfill(2)
            foldername = f"{y}-{m}"
            folderpath = join(datapath, foldername)
            if not os.path.exists(folderpath):
                continue
            file_ct, fail_ct = 0, 0
            for txt in os.listdir(folderpath):
                if '.txt' not in txt:
                    continue
                file_ct += 1
                if foldername+'-us' not in txt.lower():
                    print(f"Unexpected filename: {txt}")
                txtpath = join(datapath, foldername, txt)
                try:
                    txtfunc(txtpath)
                except:
                    print(f"Processing failed on {txtpath}")
                    fail_ct += 1
            if verbose:
                print(f"{folderpath}: processed {file_ct-fail_ct}/{file_ct} .txt files")

def explore_sourcespath(sourcespath='./data/sources/'):
    # delete when done with EDA
    print(f'exploring sources in {sourcespath}')
    foldernames = []
    for y in range(10, 22):
        for m in range(1, 13):
            y, m = str(y), str(m).zfill(2)
            foldername = f"{y}-{m}"
            foldernames.append(f"sources-{foldername}.txt")
    yms = []
    print('Files without year-month:')
    for f in os.listdir(sourcespath):
        if f not in foldernames:
            print(f)
        else:
            yms.append(f)


def read_article_txt(filepath):
    data = {}
    with open(filepath, 'r', encoding='latin') as f:
        for line in f:
            splt = line.split(' ')
            ind, sent = splt[0].strip('@'), ' '.join(splt[1:])
            cleansent = re.sub(re.compile('<.*?>'), '', sent)
            data[ind] = cleansent.strip()
    #return pd.DataFrame(data)
    df = pd.DataFrame.from_dict(data, orient='index', columns=['article_txt'])
    return df

def read_sources(filepath):
    cols = ['id', 'num', 'date', 'country', 'source', 'URL', 'text']
    data = dict(zip(cols, [[] for i in range(len(cols))]))
    with open(filepath, 'r', encoding="utf8", errors='ignore') as f:
        for line in f:
            for i, val in enumerate(line.split('\t')):
                data[cols[i]].append(val)
    #return pd.DataFrame(data)
    data = pd.DataFrame(data)
    data.id = data.id.astype('int64')
    data.set_index('id', inplace=True)
    return data

def parse_and_write_sources_once():
    sources1 = read_sources('data/sources/now_sources_pt1.txt')
    sources2 = read_sources('data/sources/now_sources_pt2.txt')
    sources = pd.concat((sources1, sources2))
    sources.loc[:, 'source_lc'] = sources.source.str.lower()
    sources.date = pd.to_datetime(sources.date, format='%y-%m-%d')
    src16 = sources[(sources['date'] > pd.to_datetime('2016/01/01')
                    ) & (sources['date'] < pd.to_datetime('2017/01/01'))]
    src16.head()
    src16.to_csv('./data/sources/now_sources_2016.txt', sep='\t')

def summarize_sources(ideology_map, srcdf):
    for k, terms in ideology_map.items():
        print(k)
        total = 0
        for term in terms:
            df_ = srcdf[srcdf.source_lc.str.contains(term)]
            ct = df_.shape[0]
            source_str = ', '.join(df_.source.unique())
            print(f"\t {term}: {ct} | {source_str}")
            total += ct
        print(f"total = {total}\n")

def get_data_per_source(src_list, source_df, limit=-1, files=files):
    dataframes = {src: None for src in src_list}
    for i, file in enumerate(files):
        if i==limit:
            break
        data = read_article_txt(file)
        for src in src_list:
            inds = source_df[source_df.source_lc.str.contains(src)].index.astype('str')
            new_inds = data.index.intersection(inds)
            #print(inds, data.index)
            #print(inds.shape, new_inds.shape)
            df2 = data.loc[new_inds].join(source_df, how='left')
            if dataframes[src] is None:
                # this is the first month being read
                dataframes[src] = df2
            else:
                dataframes[src] = pd.concat((dataframes[src], df2))
    return dataframes


def wordcounter(txt=None, filename=None, txtprocess_func=lambda x:x,
                stop_words=0, min_count=-1):
    ctr = defaultdict(int)
    if filename is not None:
        with open(filename) as f:
            for line in f:
                for w in txtprocess_func(line.lower()).split():
                    ctr[w.strip()]+=1
    elif txt is not None:
        for line in txt:
                for w in txtprocess_func(line.lower()).split():
                    ctr[w.strip()]+=1
    else:
        raise ValueError('One of txt or filename must not be None')
    df = pd.DataFrame.from_dict(ctr, orient='index', columns=['wordcount'])
    df.sort_values(by='wordcount', ascending=False, inplace=True)
    df = df.iloc[stop_words:]
    df = df[df.wordcount>min_count]
    return df
