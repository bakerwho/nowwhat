import pandas as pd
import numpy

df = pd.read_csv('./xdata/rsf_scores.csv')

rank_df = df[df['Indicator'] == 'Press Freedom Rank']
rank_df = rank_df.reset_index()

countries = rank_df['Country Name']
cols = [str(i) for i in range(2001, 2020) if i not in [2010, 2011]]

rank_data = rank_df[cols]

rank_data = rank_data.interpolate(axis=0)

#rows_with_na = (rank_data.isna().sum(axis=1) > 0).sum()

stdevs = rank_data.apply(lambda x : np.std(x), axis=1)

args = np.argsort(stdevs)[::-1]

countries[args[:10]]
