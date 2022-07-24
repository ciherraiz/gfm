import json
from time import sleep
import pandas as pd
import streamlit as st
from gfm import scrap_center, actualiza_cursos

RUTA_DATOS = 'data/'
FICHERO = 'cursos.csv'
RUTA = RUTA_DATOS + FICHERO

# Read configuration file
with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())

df = pd.read_csv(RUTA)

col1, col2, col3  = st.columns(3)

with col1:
    if st.button('Actualizar'):
        data = []
        barra_progreso = st.progress(0) 
        total_servidores = len(cfg['servidores'])
        n_servidores = 0

        for c, v in cfg['servidores'].items():
            data += scrap_center(c, v)
            sleep(cfg['espera'])
            n_servidores += 1
            barra_progreso.progress(n_servidores/total_servidores)

        df_nuevo = pd.DataFrame.from_records(data)

        df = actualiza_cursos(df, df_nuevo)

        df.to_csv(RUTA, index=False)
        st.write('Actualización finalizada')

    

with col2:
    csv = df.to_csv()
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='cursos.csv',
        mime='text/csv')

with col3:
    fichero_cargado = st.file_uploader("Selecciona el archivo", type=['csv'])
    if fichero_cargado is not None:
        df_cargado = pd.read_csv(fichero_cargado)
        df_cargado.to_csv(RUTA, index=False)
        st.write('Archivo cargado')


