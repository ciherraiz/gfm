import json
import os
from gfm import elimina_cursos
import streamlit as st

with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())
     
st.write("[Servidores Gesforma](https://www.formacionsspa.es/gesforma-sspa/)")
visor = st.json(cfg)

if st.button('Eliminar histórico'):
     elimina_cursos() 