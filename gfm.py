from bz2 import compress
import datetime
import hashlib
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

requests.urllib3.disable_warnings()

with open('conf.json', 'r') as j:
    cfg = json.loads(j.read())

ruta_datos = cfg['ruta_datos']
nombre_fichero = cfg['nombre_fichero']
ruta_fichero = ruta_datos + nombre_fichero

def scrap_center(id, center):
        data = []
        response = requests.get(center['url'], verify=False)
        if response.status_code == 200:
            doc = BeautifulSoup(response.content.decode('utf-8', errors='ignore'), "html.parser")
            for element in doc.find_all('li', class_='ui-carousel-item ui-widget-content ui-corner-all'):
                course = scrap_course(id, center, element)
                if course:
                    data.append(course)
        else:
            raise Exception(f'Error de conexión en {id}')
        return data

def scrap_course(idcenter, center, item):
    data = {}
    texts = item.find_all('span', class_='colorExplicacion')
    if len(texts) > 1:
        data['id_centro'] = idcenter
        data['centro'] = center['centro']
        data['provincia'] = center['provincia']
        data['titulo'] = texts[0].string
        match = re.findall(r'(\d+/\d+/\d+)', texts[1].string)
        data['inicio'] = match[0]
        data['fin'] = match[1]
        match = re.findall(r'(\d+/\d+/\d+)', texts[2].string)
        data['ins_inicio'] = match[0]
        data['ins_fin'] = match[1]
        match = re.findall(r'(\d+)', texts[3].string)
        data['plazas'] = match[0]
        match = re.findall(r'(\d+)', texts[4].string)
        data['solicitudes'] = match[0]
        data['aula'] = texts[5].string

        id = data['id_centro'] + data['titulo'] + data['inicio']
        id_hash = hashlib.md5(id.encode('utf-8')).hexdigest()
        data['id'] = id_hash
        data['momento'] = datetime.datetime.now()

    return data

def actualiza_cursos(df, nuevo_df):
    df_total = pd.concat([nuevo_df, df])
    df_total.drop_duplicates(subset=['id'], keep='last', inplace=True)
    return df_total

def carga_cursos(ruta=ruta_fichero):
    try:
        df = pd.read_parquet(ruta)
        df['inicio'] = pd.to_datetime(df['inicio'], format='%d/%m/%Y')
        df['fin'] = pd.to_datetime(df['fin'], format='%d/%m/%Y')
        df['ins_inicio'] = pd.to_datetime(df['ins_inicio'], format='%d/%m/%Y')
        df['ins_fin'] = pd.to_datetime(df['ins_fin'], format='%d/%m/%Y')
    except Exception as e:
        #print(e) 
        df = pd.DataFrame()
        
    return df

def almacena_cursos(df, ruta=ruta_fichero):
    df.to_parquet(ruta, compression='gzip', index=False)


if __name__ == "__main__":
    import json
    from time import sleep
    with open('conf.json', 'r') as j:
        cfg = json.loads(j.read())
    
    df = carga_cursos()
    print(df.info())
    print(df.head(10))