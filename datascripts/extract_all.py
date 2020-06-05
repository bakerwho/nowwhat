import os
from os.path import join
from zipfile import ZipFile
import string
import re
from collections import Counter, defaultdict

NOWfolder = '/project2/jevans/Davies_corpora/NOW/'
datafolder = '/project2/jevans/aabir/NOWwhat/data'

files = os.listdir(NOWfolder)
anomalies = [f for f in files if len(re.findall(r'\d+', f))==1]
for an in anomalies:
    files.remove(an)

numfiles = len(files)

def files_by_year(files):
    years = {file: tuple(int(i) for i in re.findall(r'\d+', file)) for file in files}
    return years

years = Counter(list(files_by_year(files).values()))
print(years)

def files_by_datatype(files):
    files_by_dt = defaultdict(list)
    dts = ['lexicon', 'db', 'text', 'wlp', 'sources']
    for file in files:
        for dt in dts:
            if dt in file:
                files_by_dt[dt].append(file)
    return files_by_dt

files_by_dt = files_by_datatype(files)
print({k:len(v) for k, v in files_by_dt.items()})

def unzip_files(filenames, sourcepath, destpath, condition=lambda x: True,
                    del_cond=lambda x: False):
    successes = 0
    tries = 0
    for file in filenames:
        if not condition(file):
            continue
        print(f'unzipping file {file}')
        tries += 1
        try:
            ym = tuple(re.findall(r'\d+', file))
            print(ym)
            assert len(ym) == 2, "no year/month found"
            y, m = ym
            date = f"{y}-{m}"
            dts = ['lexicon', 'db', 'text', 'wlp', 'sources']
            dt = [d for d in dts if d in file][0]
            dpath = join(destpath, dt, date)
            os.makedirs(dpath, exist_ok = True)
        except Exception as e:
            print(f"Exception during folder creation: {e}")
            dpath = destpath
        try:
            spath = join(sourcepath, file)
            with ZipFile(spath, 'r') as zipObj:
                zipObj.extractall(dpath)
            successes += 1
        except Exception as e:
            print(f"Exception while unzipping: {e}")
        try:
            new_files = os.listdir(dpath)
            delete_files = [f for f in new_files if del_cond(f)]
            for file in delete_files:
                fpath = join(dpath, file)
                if os.path.exists(fpath) and os.path.isfile(fpath):
                    os.remove(fpath)
            print(f"removed files: {'; '.join(delete_files)}")
        except Exception as e:
            print(f"Exception while clearing unwanted files: {e}")
    print(f"\n\nOut of {len(filenames)} files: tried {tries} and \
extracted {successes}\n\n")

keep_in_us = lambda x: not ('in' in x.lower() or 'us' in x.lower())

if __name__=="__main__":
    unzip_files(files_by_dt['text'], NOWfolder, datafolder)
    unzip_files(files_by_dt['lexicon'], NOWfolder, datafolder)
    #unzip_files(files_by_dt['sources'], NOWfolder, datafolder)
    #unzip_files(anomalies, NOWfolder, datafolder)






# unzip -o /project2/jevans/Davies_corpora/NOW/db_16-10-ykw.zip -d /project2/jevans/aabir/NOWwhat/data/16-10/
