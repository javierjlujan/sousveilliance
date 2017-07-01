import sys
import json
import time

import requests
import pandas as pd


df_afip = pd.read_csv('afip.csv')
df_afip.head()
df_sort = df_afip[:20]

activiti_csv = open("actividades.csv", 'a')
line_format = "{0},{1}\n"

# Write head
head = "cuit,actividad\n"
activiti_csv.write(head)

base_url = "https://aws.afip.gov.ar/sr-padron/v2/persona/{cuit}"
session = requests.session()

cuits = df_sort['cuit'].tolist()
cuits_len = len(cuits)
text = "\rCuit {0}/{1}. Cantidad de intentos {2}"

for cnt, cuit in enumerate(cuits):
    # M
    cnt_try = 0
    print(text.format(cnt, cuits_len, cnt_try), end='')
    sys.stdout.flush()

    while True:
        try:
            url = base_url.format(cuit=cuit)
            response = session.get(url)
            break
        except:
            time.sleep(0.5)
            cnt_try += 1
            print(text.format(cnt, cuits_len, cnt_try), end='')
            sys.flush()

    data = json.loads(response.text)

    if 'actividades' in data['data']:
        actividades = data['data']['actividades']

        for acti in actividades:
            activiti_csv.write(line_format.format(cuit, acti))

activiti_csv.close()
