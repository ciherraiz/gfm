from datetime import date
from gfm import carga_cursos
import matplotlib.pyplot as plt
import streamlit as st

hoy = date.today().strftime("%d/%m/%Y")
df = carga_cursos()

df_f = df.loc[(df['ins_inicio'] <= hoy) & (df['ins_fin'] >= hoy)]
inscripciones_abiertas = len(df_f)

df_fg = df_f.groupby(['id_centro']).size()

col1, col2 = st.columns(2)

with col1:
    st.metric('Inscripciones abiertas', inscripciones_abiertas)
with col2:
    fig = plt.figure()
    ax = fig.subplots()
    df_fg.plot(kind="bar", ax=ax, title='Inscripciones abiertas por centro')
    ax.set(xlabel='Centro', ylabel='Cursos')

    st.pyplot(fig)