## NOWwhat - a Python package for working with the NOW corpus

This package implements functionality to do the following:
1. Extract NOW data from zip files in the `/project2/jevans/Davies_Corpora/NOW/` location
2. Store extracted files in folders indexed by type: `lexicon`, `db`, `text`, `wlp`, `sources`
    - For `text`, subfolders of the format `f"{y}-{m}"` are used
3. Delete all but the required subset of extracted files
    - For example, automatically delete extracted files that don't meet specified condition (e.g. keep only those files with `us` in the name for US news)
4. Apply analyses on the data by year/month
