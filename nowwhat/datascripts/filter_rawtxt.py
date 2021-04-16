import os
from os.path import join
from zipfile import ZipFile
import string
import re

from utils import *
from datastructures import Sources

sourcespath = './data/sources/'

sources = Sources(sourcespath)

if __name__=='__main__':
    for y in [2016]:
        for m in [10, 11]:
            sources.load_month(y, m)
