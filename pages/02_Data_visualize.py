
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
import plotly.express as px
import plotly.graph_objects as go

st.title('Barcelona 2015-2020 シュート分析')
st.markdown(r"""## 全体のシュート成功確率""")


#Dataの取り出し、Naを０に
Barce_shots = pd.read_csv('Barcelona_2015_2020_shots_data.csv')
Shots_by_player= Barce_shots.groupby(['player','shot_outcome']).size().unstack()
Shots_by_player = Shots_by_player.fillna(0)
shot_outcome = Shots_by_player.columns.values.tolist()

# 円グラフの作成
shot_outcome_piechart = Shots_by_player.sum().reset_index()
fig = go.Figure()
fig.add_trace(
    go.Pie(labels = shot_outcome_piechart['shot_outcome'],
           values = shot_outcome_piechart[0])
)
fig.update_traces(
                hoverinfo='label+percent', 
                textinfo='percent',          
                textfont_size=20,          
                textposition='inside',
                pull = [0.2 if column == 'Goal' else 0 for column in shot_outcome]
)

st.plotly_chart(fig, use_container_width=False, sharing="streamlit",)

st.markdown(r"""## シュート成功率ランキング""")
Shots_by_player['Success rate'] =  Shots_by_player['Goal'].map(lambda x : 0)

for outcome in shot_outcome:
    Shots_by_player['Success rate'] +=  Shots_by_player[outcome]
Shots_by_player['Success rate']  =  Shots_by_player['Goal'] /  Shots_by_player['Success rate']


