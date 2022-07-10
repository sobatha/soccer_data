import pip
import streamlit as st
import streamlit.components.v1 as stc
import pickle
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

Barce_shots = pd.read_csv('LaLiga_shots_Barce_data_dummy_drop.csv')
X = Barce_shots.drop('Goal', axis=1)
y = Barce_shots['Goal']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state = 0)

sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

KNN_model = KNeighborsClassifier(n_neighbors=100, weights='distance'),
KNN_model.fit(X_train_std, y_train)

file = 'KNN_model.pkl'
pickle.dump(KNN_model, open(file, 'wb')) 