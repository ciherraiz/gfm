import json
from time import sleep
import pandas as pd
import streamlit as st
from gfm import scrap_center

# Read configuration file
with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())

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

    df = pd.DataFrame.from_records(data)

    df.to_csv('data/cursos.csv')
    st.write('Actualización finalizada')



