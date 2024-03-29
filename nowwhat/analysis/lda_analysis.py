import numpy as np
import pandas as pd
from gensim.models import ldaseqmodel, ldamodel
from gensim.corpora import Dictionary, textcorpus, mmcorpus
from gensim.matutils import hellinger
from gensim.parsing import preprocessing
import time
import pprint

from gensim.models.word2vec import Word2Vec

import os
from os.path import join

now_folder = '/project2/jevans/aabir/NOWwhat/'
d_folder = '/project2/jevans/aabir/NOWwhat/xdata'
in_folder = join(d_folder, 'in_data')
us_folder = join(d_folder, 'us_data')

corpus_folder = join(d_folder, 'corpus')
result_folder = join(now_folder, 'resultdata')

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

indian_politics_wordlist = ['election', 'politics', 'minister',
        'congress', 'bjp', 'advani', 'manmohan', 'singh', 'sonia', 'gandhi',
        'modi', 'narendra', 'rahul']

class conditionalCorpus(textcorpus.TextCorpus):
    wordlist = ['election', 'politics', 'minister',
            'congress', 'bjp', 'advani', 'manmohan', 'singh', 'sonia', 'gandhi',
            'modi', 'narendra', 'rahul']
    def get_texts(self):
        for doc in self.getstream():
            flag = False
            for w in wordlist:
                if w in doc.lower():
                    flag = True
            if flag:
                yield preprocessing.preprocess_string(doc)


def gentler_lda_entire_corpus(in_folder, ofile, wordlist, num_topics=30):
    files = sorted([i for i in os.listdir(in_folder) if os.path.isfile(join(in_folder, i))])
    #print(files)
    months = []
    with open(ofile, 'w') as f:
        f.write(pprint.pformat(locals()))
        for file in files:
            month = file.split('.')[-2][-8:-3]
            f.write(f'\n{"="*40}\n\nmonth {month}')
            mcorpus = textcorpus.conditionalCorpus(join(in_folder, file))#, lines_are_documents=True)
            lda = ldamodel.LdaModel(mcorpus, num_topics=num_topics, id2word=mcorpus.dictionary)
            topics = lda.get_topics()
            f.write(pprint.pformat(lda.show_topics(num_topics, num_words=30))+'\n')
            for w in wordlist:
                try:
                    topics = lda.get_term_topics(w)
                    f.write(f'\t{w}: {pprint.pformat(topics)}\t')
                except:
                    f.write(f'\t{w}: outofvocab\t')
            print(f'month {month} LDA complete')


if __name__ == '__main__':
    gentler_lda_entire_corpus(in_folder, join(result_folder, 'lda_output.txt'),
                                indian_politics_wordlist)
