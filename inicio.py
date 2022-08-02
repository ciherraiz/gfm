import json
import time
import datetime
import pandas as pd
import streamlit as st
from gfm import scrap_center, actualiza_cursos, carga_cursos, almacena_cursos

st.set_page_config(
     page_title='GFM',
     page_icon=':ledger:',
     layout='wide',
     initial_sidebar_state='expanded',
     menu_items={
         'Get help': 'https://www.formacionsspa.es/gesforma-sspa/',
         'About': "-"
     }
 )

# Read configuration file
with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())

df = carga_cursos()

if st.button('Actualizar'):
    inicio = time.time()
    data = []
    barra_progreso = st.progress(0) 
    total_servidores = len(cfg['servidores'])
    n_servidores = 0

    for c, v in cfg['servidores'].items():
        try:
            data += scrap_center(c, v)
        except Exception as e:
            st.error(e)
        time.sleep(cfg['espera'])
        n_servidores += 1
        barra_progreso.progress(n_servidores/total_servidores)

    df_nuevo = pd.DataFrame.from_records(data)

    df = actualiza_cursos(df, df_nuevo)

    almacena_cursos(df)

    fin = time.time()
    st.write(f'Servidores: {n_servidores}')
    st.write(f'Actualizado en {fin-inicio:.2f} seg.')
    df_tmp = df.loc[df['momento'] >= datetime.date.today().strftime('%Y-%m-%d')]
    st.write(f"Nuevos cursos hoy: {len(df_tmp)}")


    csv = df.to_csv(index=False)
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='cursos.csv',
        mime='text/csv')


