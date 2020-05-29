import numpy as np
import pandas as pd
from gensim.models import ldaseqmodel
from gensim.corpora import Dictionary, textcorpus, mmcorpus
from gensim.matutils import hellinger
import time

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

if __name__ == '__main__':
    corpus = mmcorpus.MmCorpus(join(corpus_folder, 'in_corpus.mm'))

    slice_df = pd.read_csv(join(d_folder, '..', 'notes', 'month_linects.txt'),
                            sep=' ', names=['mth', 'ct'], index_col=False)

    slices = list(slice_df.ct)
    slices[-1] += corpus.num_docs-sum(slices)

    dictionary = Dictionary.load(join(corpus_folder, 'in_corpus_dict.dict'))

    t1 = time.time()
    ldaseqmodel.LdaSeqModel(corpus=corpus, id2word=dictionary,
                                time_slice=slices, num_topics=500)
    t2 = time.time()
    print(f"# seconds = {int(t2-t1)}")
