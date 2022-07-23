import pandas as pd
import streamlit as st

df = pd.read_csv('data/cursos.csv')
st.dataframe(df)
