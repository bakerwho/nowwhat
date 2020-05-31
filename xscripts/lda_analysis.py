import numpy as np
import pandas as pd
from gensim.models import ldaseqmodel
from gensim.corpora import Dictionary, textcorpus, mmcorpus
from gensim.matutils import hellinger
import time

from gensim.models.word2vec import Word2Vec

import os
from os.path import join

d_folder = '/project2/jevans/aabir/NOWwhat/xdata'
in_folder = join(d_folder, 'in_data')
us_folder = join(d_folder, 'us_data')

corpus_folder = join(d_folder, 'corpus')

def load_corpus_from_directory(in_folder):
    t1 = time.time()
    corpus = textcorpus.TextDirectoryCorpus(in_folder, lines_are_documents=True)
    t2 = time.time()
    print(f"# seconds = {int(t2-t1)}")
    return corpus

def save_corpus_to_disk(location, corpus):
    t1 = time.time()
    mmcorpus.MmCorpus.serialize(location, corpus, id2word=corpus.dictionary, progress_cnt=100, metadata=True)
    t2 = time.time()
    print(f"# seconds = {int(t2-t1)}")

# corpus = load_corpus_from_directory(in_folder)
# save_corpus_to_disk(join(corpus_folder, 'in_corpus.mm'), corpus)

def bruteforce_lda_entire_corpus():
    # this does not work
    # reports Bus error on slurm
    # probably requires way too much RAM/compute power
    corpus = mmcorpus.MmCorpus(join(corpus_folder, 'in_corpus.mm'))
    slice_df = pd.read_csv(join(d_folder, '..', 'notes', 'month_linects.txt'),
                            sep=' ', names=['mth', 'ct'], index_col=False)
    slices = list(slice_df.ct)
    slices[-1] += corpus.num_docs-sum(slices)
    dictionary = Dictionary.load(join(corpus_folder, 'in_corpus_dict.dict'))
    print('loaded corpus and dictionary')
    t1 = time.time()
    ldaseqmodel.LdaSeqModel(corpus=corpus, id2word=dictionary,
                                time_slice=slices, num_topics=500)
    t2 = time.time()
    print(f"# seconds = {int(t2-t1)}")

def gentler_lda_entire_corpus(in_folder):
    files = sorted([i for i in os.listdir(in_folder) if os.path.isfile(join(in_folder, i))])
    #print(files)
    months = []
    for file in files:
        month = file.split('.')[-2][-8:-3]
        mcorpus = textcorpus.TextCorpus(join(in_folder, file), lines_are_documents=True)
        ldaseqmodel.LdaSeqModel(corpus=mcorpus, id2word=mcorpus.dictionary, num_topics=100)


if __name__ == '__main__':
