import datetime
import hashlib
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

requests.urllib3.disable_warnings()

def scrap_center(id, center):
        data = []
        try:
            response = requests.get(center['url'], verify=False)
            doc = BeautifulSoup(response.content.decode('utf-8', errors='ignore'), "html.parser")
        except:
            print(f'Error downloading {id} courses.')
        for element in doc.find_all('li', class_='ui-carousel-item ui-widget-content ui-corner-all'):
            course = scrap_course(id, center, element)
            if course:
                data.append(course)
        return data

def scrap_course(idcenter, center, item):
    data = {}
    texts = item.find_all('span', class_='colorExplicacion')
    if len(texts) > 1:
        data['id_centro'] = idcenter
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


if __name__ == "__main__":
    import json
    from time import sleep
    with open('conf.json', 'r') as j:
        cfg = json.loads(j.read())
    print(cfg)
    data = []
    for c, v in cfg['servidores'].items():
        data += scrap_center(c, v)
        sleep(cfg['espera'])

    print(data)