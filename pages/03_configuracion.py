import json
import streamlit as st

with open('conf.json', 'r') as j:
     cfg = json.loads(j.read())

visor = st.json(cfg)