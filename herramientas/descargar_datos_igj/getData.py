"""
Descarga todos los csv necesario para luego trabajarlos
"""
import sys

import requests
from contextlib import closing


def download_file(url, file_number, total_files):
    """
    Download a big file in chunk

    Tanks to @danodonovan
    http://stackoverflow.com/a/16695277/2134094
    """
    local_filename = url.split('/')[-1]
    file_path = 'datos/' + local_filename
    chunk_size = 1024
    message = "\rBajando archivo {0} {1:.1f}%  {2}/{3} csv."

    with closing(requests.get(url, stream=True)) as response:
        # Total size and total download
        total_size = int(response.headers['Content-Range'].split('/')[-1])
        download = 0

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                download += len(chunk)
                sys.stdout.write(message.format(local_filename,
                                                (download*100)/total_size,
                                                file_number, total_files))
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    return file_path


url_domicilios = "http://datos.jus.gob.ar/dataset/da045e06-35cb-4bdd-9b5e-ddee6712c86c/resource/15e4fb9d-c195-40f1-b0a3-27c0ffe3591a/download/igj-domicilios.csv"
url_autoridades = "http://datos.jus.gob.ar/dataset/da045e06-35cb-4bdd-9b5e-ddee6712c86c/resource/e41edb57-f798-443d-8932-c06d275aca18/download/igj-autoridades.csv"
url_asambleas = "http://datos.jus.gob.ar/dataset/da045e06-35cb-4bdd-9b5e-ddee6712c86c/resource/9f31723c-8569-4dd4-ae7d-fdc46bc7ec8e/download/igj-asambleas.csv"
url_balances = "http://datos.jus.gob.ar/dataset/da045e06-35cb-4bdd-9b5e-ddee6712c86c/resource/6e90dced-64df-4c13-9a22-081bb3b872de/download/igj-balances.csv"
url_entidades = "http://datos.jus.gob.ar/dataset/da045e06-35cb-4bdd-9b5e-ddee6712c86c/resource/1715382e-0c5e-400b-9550-d1c395311cad/download/igj-entidades.csv"


urls = [url_asambleas, url_balances, url_entidades,
        url_domicilios, url_autoridades]

for file_number, url in enumerate(urls):
    download_file(url, file_number+1, len(urls))
