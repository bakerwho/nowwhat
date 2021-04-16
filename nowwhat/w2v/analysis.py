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
