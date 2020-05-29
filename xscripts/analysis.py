import numpy as np
import pandas as pd
from gensim.models import ldaseqmodel
from gensim.corpora import Dictionary, textcorpus, mmcorpus
from gensim.matutils import hellinger
import time

import os
from os.path import join

time_slice = [438, 430, 456]

d_folder = '/project2/jevans/aabir/NOWwhat/xdata'
in_folder = join(d_folder, 'in_data')
us_folder = join(d_folder, 'us_data')

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
# save_corpus_to_disk(join(d_folder, 'in_corpus2.mm'), corpus)

corpus2 = mmcorpus.MmCorpus(join(d_folder, 'in_corpus2.mm'))

def ldaseq_analyze(corpus):
    ldaseqmodel.LdaSeqModel(corpus=corpus, id2word=corpus.dictionary,
                            time_slice=time_slice, num_topics=10e3)
