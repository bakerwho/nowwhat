import os
from os.path import join
from zipfile import ZipFile
import string
import re
from collections import Counter, defaultdict

NOWfolder = '/project2/jevans/Davies_corpora/NOW/'
#NOWfolder = '.'
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
    datatypes = ['lexicon', 'db', 'text', 'wlp', 'sources']
    for file in files:
        for dt in datatypes:
            if dt in file:
                files_by_dt[dt].append(file)
    return files_by_dt

files_by_dt = files_by_datatype(files)
print({k:len(v) for k, v in files_by_dt.items()})

def unzip_files(zipfilenames, sourcepath, destpath, zip_cond=lambda x: True,
                    del_cond=lambda x: False):
    """
        unzips zip files under zipfilenames, deletes unzipped files
    """
    successes = 0
    tries = 0
    for zipfile in zipfilenames:
        if not zip_cond(zipfile):
            continue
        print(f'unzipping zipfile {zipfile}')
        tries += 1
        try:
            ym = tuple(re.findall(r'\d+', zipfile))
            print(ym)
            assert len(ym) == 2, "no year/month found"
            y, m = ym
            date = f"{y}-{m}"
            datatypes = ['lexicon', 'db', 'text', 'wlp', 'sources']
            dt = [d for d in datatypes if d in zipfile][0]
            if dt == 'text':
                dpath = join(destpath, dt, date)
            else:
                dpath = join(destpath, dt)
            os.makedirs(dpath, exist_ok = True)
            print(f"Destination set to {dpath}")
        except Exception as e:
            print(f"Exception raised: {e}")
            dpath = destpath
            print(f"Destination set to {dpath}")
        init_filecount = len(os.listdir(dpath))
        try:
            spath = join(sourcepath, zipfile)
            with ZipFile(spath, 'r') as zipObj:
                zipObj.extractall(dpath)
            successes += 1
            mid_filecount = len(os.listdir(dpath))
            print(f'Extracted {mid_filecount - init_filecount} files')
        except Exception as e:
            print(f"Exception while unzipping: {e}")
        try:
            new_files = os.listdir(dpath)
            delete_files = [f for f in new_files if del_cond(f)]
            for file in delete_files:
                fpath = join(dpath, file)
                if os.path.exists(fpath) and os.path.isfile(fpath):
                    os.remove(fpath)
            final_filecount = len(os.listdir(dpath))
            print(f"removed {len(delete_files)} files: {'; '.join(delete_files)}")
        except Exception as e:
            print(f"Exception while clearing unwanted files: {e}")
    print(f"\n\nOut of {len(zipfilenames)} Zipfiles: tried {tries} and \
    extracted {successes}\n\n")

def check_extraction(folderlist):
    ct = 0
    for y in range(10, 22):
        for m in range(1, 13):
            ym_str = f"{str(y).zfill(2)}-{str(m).zfill(2)}"
            if ym_str not in folderlist:
                ct+=1
                print(ym_str)
    print(f'Total {ct} year-month folders missing')

del_non_in_us = lambda x: not ('in' in x.lower() or 'us' in x.lower())
del_non_us = lambda x: not ('us' in x.lower())


if __name__=="__main__":
    #num_files = 100000
    #num_files = int(input('Enter no. of Zipfiles to extract:\t'))
    unzip_files(files_by_dt['text'], NOWfolder, datafolder,
                del_cond=del_non_us)
    unzip_files(files_by_dt['lexicon'], NOWfolder,
                    datafolder)
    unzip_files(files_by_dt['sources'], NOWfolder,
                    datafolder)
    #unzip_files(anomalies, NOWfolder, datafolder)
    #unzip_files(files_by_dt[k], NOWfolder, datafolder, condition=lambda x: '16' in x)






# unzip -o /project2/jevans/Davies_corpora/NOW/db_16-10-ykw.zip -d /project2/jevans/aabir/NOWwhat/data/16-10/
