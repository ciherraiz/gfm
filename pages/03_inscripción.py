import datetime
from gfm import carga_cursos
import pandas as pd
import streamlit as st

hoy = datetime.date.today().strftime("%Y-%m-%d")
df = carga_cursos()

df_filtrado = df.loc[(df['ins_inicio'] <= hoy ) & (df['ins_fin'] >= hoy)].copy()

df_filtrado['dias_fin'] = (df_filtrado['ins_fin']-datetime.datetime.now()).dt.days
df_filtrado['rsp'] = df_filtrado['solicitudes'] / df_filtrado['plazas']
df_filtrado['dias_solicitud'] = (datetime.datetime.now() - df_filtrado['ins_inicio']).dt.days
df_filtrado['sol_por_dia'] = df_filtrado['solicitudes'] / df_filtrado['dias_solicitud']
st.write(f'Fecha fin de inscripción mayor o igual a {hoy} ({len(df_filtrado)} cursos)')
cols = ['titulo', 'rsp', 'dias_fin', 'ins_inicio', 'ins_fin', 'centro', 'provincia', 'aula', 'plazas', 'solicitudes', 'sol_por_dia', 'momento']
st.dataframe(df_filtrado[cols].style.format(precision=2).background_gradient(subset=['rsp']))