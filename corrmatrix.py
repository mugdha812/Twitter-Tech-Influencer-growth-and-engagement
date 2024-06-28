#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

likes_df = pd.read_csv('C:/Users/Mugdha Shah/Desktop/mism 6210/mid term/likes.csv')
profile_df = pd.read_csv('C:/Users/Mugdha Shah/Desktop/mism 6210/mid term/profile_snapshots.csv')
tweets_df = pd.read_csv('C:/Users/Mugdha Shah/Desktop/mism 6210/mid term/tweets.csv')

def get_date(x):
     return x[:10]
    
profile_df['date'] = profile_df['checktime'].apply(lambda x: get_date(x))

last_day_df = profile_df[profile_df['date'] == '2022-01-31']
last_day_df = last_day_df[['twitterUserId','followers_count','likes_count']]
last_day_df.drop_duplicates(inplace = True)

fav_count = tweets_df.groupby(['twitterUserId'])['favorite_count'].sum() 
retweet_count = tweets_df.groupby(['twitterUserId'])['retweet_count'].sum()

joined_df = last_day_df.join(retweet_count, on = 'twitterUserId', how = 'inner')
joined_df = joined_df.join(fav_count, on = 'twitterUserId', how = 'inner')


joined_df['info_spread'] = joined_df['followers_count'] * (joined_df['favorite_count'] + joined_df['retweet_count'] + joined_df['likes_count'])
joined_df['epp'] = (joined_df['likes_count'] + joined_df['retweet_count'] + joined_df['favorite_count']) / joined_df['followers_count']

corr = joined_df.corr()

cmap = LinearSegmentedColormap.from_list(
    'custom_red_green', 
    [(0, 'red'), (0.5, 'white'), (1, 'green')],
    N=256
)

sns.heatmap(corr, annot=True, cmap=cmap, center=0, vmin=-1, vmax=1, cbar=False)
plt.show()
#sns.heatmap(corr, annot = True, cmap='RdYlGn')
#plt.show()

