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

for column in columns:
    pram[column] = 0

selected_item = st.selectbox('play pattern　を選んでください',
                                 ['From Corner', 'From Counter', 'From Free Kick',
                                 'From Goal Kick', 'From Throw In'])

pram[selected_item] = 1

for item in ['shot_one_on_one', 'teammate_minus_enemy', 'In_PenaltyArea', 'shot_open_goal',
                'shot_aerial_won', 'Messi']:
    if st.checkbox(item):
        pram[item] = 1
    else:
        pram[item] = 0
pram = pd.DataFrame(pram, index=['i',])

with open('KNN_model.pkl', mode='rb') as f:
    KNN_model = pickle.load(f)

Goal_predict = KNN_model.predict_proba(pram)

st.markdown(r""" ## シュート結果""")
answer = st.button('結果を表示')

if answer == True:
     st.write("ゴール確率:{:.2%}".format(Goal_predict[0, 0]))


