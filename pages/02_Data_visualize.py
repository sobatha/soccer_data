
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

st.markdown(r"""## シュート結果別プレイヤー割合""")
selected_result = st.selectbox('シュート結果をえらんでください',
                                 ['Goal', 'Blocked', 'Off T', 'Post', 
                                 'Saved', 'Saved Off Target', 'Saved to Post','Wayward'])
shot_outcome_by_player = pd.DataFrame(Shots_by_player[selected_result]).reset_index()
shot_outcome_by_player = shot_outcome_by_player.sort_values(by=selected_result ,ascending=False)
fig2 = go.Figure()
fig2.add_trace(
    go.Pie(labels = shot_outcome_by_player['player'],
           values = shot_outcome_by_player[selected_result])
)
fig2.update_traces(
                hoverinfo='label+percent', 
                textinfo='percent',          
                textfont_size=20,          
                textposition='inside',
)
fig2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig2, use_container_width=False, sharing="streamlit",)

st.markdown(r"""## プレイヤー別シュート結果割合""")

players = shot_outcome_by_player['player'].tolist()
selected_player = st.selectbox('プレイヤーをえらんでください',
                                 players)
player_by_shot_outcome = pd.DataFrame(Shots_by_player.loc[selected_player]).reset_index()
fig3 = go.Figure()
fig3.add_trace(
    go.Pie(labels = player_by_shot_outcome['shot_outcome'],
           values = player_by_shot_outcome[selected_player])
)
fig3.update_traces(
                hoverinfo='label+percent', 
                textinfo='percent',          
                textfont_size=20,          
                textposition='inside',
)
fig3.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig3, use_container_width=False, sharing="streamlit",)

st.markdown(r"""## シュート本数ランキング""")

show_shot_times = st.checkbox('シュート本数ランキングの表示')
if show_shot_times == True:
    st.write(Shots_by_player.sort_values(by="Goal" ,ascending=False)
    .reindex(columns=['Goal', 'Blocked', 'Off T', 'Post', 'Saved',
                     'Saved Off Target', 'Saved to Post','Wayward'])
    .style.format("{:.0f}"))

st.markdown(r"""## シュート成功率ランキング""")

Shots_by_player['Success rate'] =  Shots_by_player['Goal'].map(lambda x : 0)
for outcome in shot_outcome:
    Shots_by_player['Success rate'] +=  Shots_by_player[outcome]
Shots_by_player['Success rate']  =  Shots_by_player['Goal'] /  Shots_by_player['Success rate']

show_shotrate = st.checkbox('シュート成功率ランキングの表示')
if show_shotrate == True:
    st.write(pd.DataFrame(Shots_by_player['Success rate']).sort_values(by="Success rate" ,ascending=False)
    .style.format("{:.2%}"))
