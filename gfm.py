import re
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import requests

requests.urllib3.disable_warnings()

def scrap_servers(servers, delay):
    data = []
    for c, v in servers.items():
        data += scrap_center(c, v)
        sleep(delay)
    df = pd.DataFrame.from_records(data)
    return df


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
        data['id_center'] = idcenter
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
    return data

if __name__ == "__main__":
    import json
    with open('conf.json', 'r') as j:
        cfg = json.loads(j.read())
    print(cfg)
    scrap_servers(cfg['servidores'], cfg['espera'])
