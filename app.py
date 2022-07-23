import json
import streamlit as st
from gfm import scrap_servers

# Read configuration file
with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())

df = scrap_servers(cfg['servidores'], cfg['espera'])

st.title('Listado cursos')
st.write(df)



