from datetime import date
from gfm import carga_cursos
import streamlit as st


hoy = date.today().strftime("%d/%m/%Y")
df = carga_cursos()

df_filtrado = df.loc[(df['ins_inicio'] <= hoy ) & (df['ins_fin'] >= hoy)]
st.write(f'Fecha fin de inscripción mayor o igual a {hoy} ({len(df_filtrado)} cursos)')
st.dataframe(df_filtrado[['titulo', 'ins_inicio', 'ins_fin', 'centro', 'provincia']])