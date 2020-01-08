from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import scipy.stats

baseball = pd.read_csv('C:/Users/aleja/downloads/game_logs.csv')
baseball_data = baseball.tail(1000)

#baseball_data = baseball.sample(n=10000)
baseball_data = baseball_data.reset_index().drop(columns='index')

#going to drop them for now
players_list_to_drop = []
fea = ['name', 'def_pos', 'id']
for n in range(1, 10):
    for m in range(3):
        players_list_to_drop.extend(['h_player_'+str(n)+'_'+fea[m], 'v_player_'+str(n)+'_'+fea[m]])

baseball_data.drop(columns=players_list_to_drop, inplace=True)
baseball_data.drop(columns=['winning_rbi_batter_id', 'winning_rbi_batter_id_name', 'additional_info', 'acquisition_info'], inplace=True)
umpires_cols, id_cols = [], []
for col in list(baseball_data.columns):
    if 'umpire' in col:
        umpires_cols.append(col)
    elif 'id' in col:
        id_cols.append(col)
umpires_cols.remove('hp_umpire_name')

baseball_data.drop(columns=umpires_cols, inplace=True)
baseball_data.drop(columns=id_cols, inplace=True)

many_nulls = []
for i in range(len(baseball_data.isnull().sum())):
    if baseball_data.isnull().sum()[i] == 9993 or baseball_data.isnull().sum()[i] == 9988 or baseball_data.isnull().sum()[i] == 10000:
        many_nulls.append(i)

l_many_nulls = [pd.DataFrame(baseball_data.isnull().sum()).reset_index().iloc[i]['index'] for i in many_nulls]
baseball_data.drop(columns=l_many_nulls, inplace=True)
many_nulls2 = []
for i in range(len(baseball_data.isnull().sum())):
    if baseball_data.isnull().sum()[i] == 2 or baseball_data.isnull().sum()[i] == 1:
        many_nulls2.append(i)
many_nulls2
l_many_nulls2 = [pd.DataFrame(baseball_data.isnull().sum()).reset_index().iloc[i]['index'] for i in many_nulls2]
baseball_data.dropna(subset=l_many_nulls2, inplace=True)

plt.figure(figsize=(17.0, 17.0))
sns.heatmap(baseball_data.corr())

#some columns are being dropped due to positive correlations between them
baseball_data.drop(columns='v_game_number', inplace=True)
baseball_data.drop(columns=['v_grounded_into_double', 'v_putouts', 'h_grounded_into_double', 'h_rbi', 'v_grounded_into_double', 'h_sacrifice_hits', 'v_sacrifice_hits'], inplace=True)
baseball_data.drop(columns=['v_team_earned_runs', 'h_team_earned_runs', 'length_outs', 'v_rbi', 'h_putouts'], inplace=True)
baseball_data.drop(columns=['v_at_bats', 'h_at_bats'], inplace=True)

baseball_data['v_caught_stealing'].value_counts()
def setter1(x):
    if x > 0:
        return 'Yes'
    else:
        return 'No'
baseball_data['V_Caught_Stealing'] = baseball_data['v_caught_stealing'].apply(setter1)
baseball_data['H_Caught_Stealing'] = baseball_data['h_caught_stealing'].apply(setter1)
baseball_data.drop(columns=['v_caught_stealing', 'h_caught_stealing'], inplace=True)

baseball_data['saving_pitcher_name'].value_counts()
def setter2(y):
    if y == '(none)':
        return 'No'
    else:
        return 'Yes'
baseball_data['Saved'] = baseball['saving_pitcher_name'].apply(setter2)
baseball_data.drop(columns='saving_pitcher_name', inplace=True)

baseball_data['date'].astype(object)
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
not_large_month = ['February', 'April', 'June', 'September', 'November']
def setter3(z):
    z = str(z)
    if z[4] == '0':
        if z[6:8] == '31' and month[int(z[5])] in not_large_month:
            return np.NaN
        else:
            return month[int(z[5])] + ' ' + z[6:8] + ', ' + z[:4]
    else:
        if z[6:8] == '31' and month[int(z[4:6])] in not_large_month:
            return np.NaN
        else:
            return month[int(z[4:6])] + ' ' + z[6:8] + ', ' + z[:4]
baseball_data['Date'] = baseball_data['date'].apply(setter3)
baseball_data['Date'].value_counts()
baseball_data.dropna(subset = ['Date'], inplace=True)
baseball_data['Date'].astype('datetime64[ns]')
baseball_data.drop(columns='date', inplace=True)