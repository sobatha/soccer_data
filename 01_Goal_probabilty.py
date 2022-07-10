import pip
import streamlit as st
import streamlit.components.v1 as stc
import base64
import pandas as pd
import numpy as np
import pickle
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from collections import defaultdict

st.set_page_config(layout="wide")
st.image('images/SB - Icon Lockup - Colour positive.png')
st.title('Barcelona 2015-2020 シュート期待値算定')
st.markdown(r"""##### ※データはStatsBombのオープンデータを利用しています。""")


Barce_shots = pd.read_csv('LaLiga_shots_Barce_data_dummy_drop.csv')
Barce_shots = Barce_shots.drop('Goal', axis=1)
columns = Barce_shots.columns.values.tolist()

if st.checkbox("説明変数の詳細を表示"):
    st.markdown(
        r"""
        ### 説明変数
        #### From Corner
        #### From Counter
        #### From Free Kick
        #### From Goal Kick
        #### From Throw In
        #### shot_one_on_one
        #### teammate_minus_enemy
        #### In_PenaltyArea
        #### shot_open_goal
        #### shot_aerial_won
        #### Messi
        """
    )

pram = defaultdict(int)

selected_item = st.selectbox('play pattern　を選んでください',
                                 ['From Corner', 'From Counter', 'From Free Kick',
                                 'From Goal Kick', 'From Throw In'])

for column in columns:
    if column in selected_item:
        pram[column] = 1
    else:
        pram[column] = 0

teammate_minus_enemy = st.slider('プレーに関与する周りの味方の数ー敵チームの数を決めてください', min_value= -5,
                            max_value=5, step = 1, value = 0)
pram['teammate_minus_enemy'] = teammate_minus_enemy

st.write('シュート時の状況を下記から選んでください')

for item in ['shot_one_on_one', 'In_PenaltyArea', 'shot_open_goal',
                'shot_aerial_won', 'Messi']:
    if st.checkbox(item):
        pram[item] = 1
    else:
        pram[item] = 0
pram = pd.DataFrame(pram, index=['i',])

with open('KNN_model.pkl', mode='rb') as f:
    KNN_model = pickle.load(f)

Goal_predict = 1 - KNN_model.predict_proba(pram)

st.markdown(r""" ## シュート結果""")
answer = st.button('結果を表示')

if answer == True:
     st.write("ゴール確率:{:.2%}".format(Goal_predict[0, 0]))


