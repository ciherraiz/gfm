import json
import os
from gfm import elimina_cursos
import streamlit as st

with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())

visor = st.json(cfg)

if st.button('Eliminar histórico'):
     elimina_cursos() 