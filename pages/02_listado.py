from gfm import carga_cursos
import pandas as pd
import streamlit as st

df = carga_cursos()
st.dataframe(df)
