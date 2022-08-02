import datetime
from gfm import carga_cursos
import pandas as pd
import streamlit as st

d = st.date_input(
     "Selecciona una fecha",
     datetime.date.today())
fecha_i = d.strftime("%Y-%m-%d")
fecha_f = (d + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
df = carga_cursos()
df_filtrado = df.loc[(df['momento'] >= fecha_i) & (df['momento'] <= fecha_f)]
st.write(f'Nuevos cursos descargados el {fecha_i} ({len(df_filtrado)} cursos)')
st.dataframe(df_filtrado[['titulo', 'provincia', 'centro', 'aula', 'ins_inicio', 'ins_fin', 'momento']])