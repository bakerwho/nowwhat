import os
from os.path import join
from zipfile import ZipFile
import string
import re

def iterate_over_files(datapath, txtfunc=lambda x: None, verbose=True):
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
                if foldername+'-us' not in txt:
                    print(f"Unexpected filename: {txt}")
                txtpath = join(datapath, foldername, txtpath)
                try:
                    txtfunc(txtpath)
                except:
                    print(f"Processing failed on {txtpath}")
                    fail_ct += 1
            if verbose:
                print(f"{folderpath}: processed {file_ct-fail_ct}/{file_ct} .txt files")
