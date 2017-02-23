#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Descarga de los json del boletin oficial con la creación y modificación
de las empresas
"""

import argparse
import sys
import os
import json
import datetime
import re
from multiprocessing import Manager, Pool

import requests


def cleanHtml(raw_html):
    """
    Elimino todos los tag de html de un texto
    """
    cleanr = re.compile('<.*?>')
    cleanText = re.sub(cleanr, '', raw_html)
    return cleanText


def descargar_detalles_segunda(tramite):
    segundaCnt.value += 1
    totalBajados.value += 1
    # Print numero de detalle bajado
    sys.stdout.write(text.format(cnt + 1, len(fechas),
                                 segundaCnt.value,
                                 len(indiceSegunda['dataList'][0]),
                                 totalBajados.value))

    # Request detalle segunda
    data = {'id': tramite["id"], 'fechaPublicacion': 'null',
            'idSesion': ''}
    t = requests.post(urlSegunda, data=data)

    # Decoded
    detalleSegunda = json.loads(t.text)

    # La denominacion social viene en null en detalle segunda,
    # lo reemplazamos por el de tramite
    if detalleSegunda["dataList"]["denominacionSocial"] is None:
        detalleSegunda["dataList"]["denominacionSocial"] = tramite["denominacion"]
    # El rubro padre no esta en detallesSegunda
    detalleSegunda["dataList"]['rubroPadre'] = tramite['rubroPadre']

    # Escribo el csv de datos
    line = ''
    for key in segunda_data_key:
        value = cleanHtml(str(detalleSegunda["dataList"][key]))
        line += "\"" + value.replace(",", "\,").replace("\"", "\\\"") +\
                "\"" + ','
    line = line[:-1]
    line += '\n'

    # Pongo un lock para escribir de a un proceso al archivo de salida
    lock.acquire()
    file_data.write(line)
    file_data.flush()
    lock.release()

    # Escribo el csv con el texto completo
    line = ''
    for key in segunda_text_key:
        value = cleanHtml(str(detalleSegunda["dataList"][key]))
        line += "\"" + value.replace(",", "\,").replace("\"", "\\\"") +\
                "\"" + ','
    line = line[:-1]
    line += '\n'

    lock.acquire()
    file_text.write(line)
    file_text.flush()
    lock.release()


# Parseo los datos de la cli
parser = argparse.ArgumentParser(description="Descarga de las BO")
parser.add_argument('-i', '--inicio', dest='fechaInicio',
                    default=datetime.date.today().strftime("%Y%m%d"),
                    help='Fecha de la cual comenzar a descargar.\
                    Forma: (yyyymmdd)')
parser.add_argument('-f' '--fin', dest='fechaFinal',
                    default='19970101',
                    help='Fecha hasta la cual descargar..\
                    Forma: (yyyymmdd)')
parser.add_argument('-np' '--numProcesos', dest='numProcesos',
                    default=10, type=int,
                    help='Numero de procesos usados. Default 10')
args = parser.parse_args()


# Url de descargas
urlSeciones = "https://www.boletinoficial.gob.ar/secciones/secciones.json"
urlSegunda = "https://www.boletinoficial.gob.ar/norma/detalleSegunda"

# Key de los json bajados
segunda_data_key = ['fechaPublicacion', 'idTramite', 'numeroTramite',
                    'anioTramite', 'idRubro', 'rubroPadre', 'rubroDescripcion',
                    'denominacionSocial', 'archivoPDF', 'paginaDesde',
                    'paginaHasta', 'suplemento']
segunda_text_key = ['idTramite', 'textoCompleto']


# Archivos de salida
path_data = "BO_data.csv"
path_text = "BO_text.csv"

# Si el archivo de salida existe, retomo desde donde dejo
dirs = os.listdir()
if path_data in dirs:
    file_data = open(path_data, "r")
    csvLines = file_data.readlines()
    lastLine = csvLines[-1]
    file_data.close()
    args.fechaInicio = lastLine.split(",")[0].replace("\"", "")
    # No necesita un header el csv
    header = False
else:
    header = True


# Me fijo que la fechas sean validas
try:
    d1 = datetime.datetime.strptime(args.fechaInicio, "%Y%m%d")
except:
    print("Fecha inicial invalida")
    sys.exit(-1)

try:
    d2 = datetime.datetime.strptime(args.fechaFinal, "%Y%m%d")
except:
    print("Fecha final invalida")
    sys.exit(-1)

# Lista de fechas que voy a bajar
fechas = []
delta = d1 - d2

for i in range(delta.days + 1):
    fecha = d1 - datetime.timedelta(days=i)
    # Sole me quedo con los dias laborables
    if fecha.weekday() in range(0, 5):
        fechas.append(fecha.strftime("%Y%m%d"))


# Abro los archivos de salida
file_data = open(path_data, "a")
file_text = open(path_text, "a")

# Creo el header en los csv
if header:
    # Para el csv de datos
    line = ""
    for key in segunda_data_key:
        line += key + ','
    line = line[:-1]
    line += '\n'
    file_data.write(line)
    file_data.flush()

    # Para el csv de texto completo
    line = ""
    for key in segunda_text_key:
        line += key + ','
    line = line[:-1]
    line += '\n'
    file_text.write(line)
    file_text.flush()

    header += False


print("Descargar desde: {0} hasta: {1}".format(args.fechaInicio,
                                               args.fechaFinal))
print("Se van a descar: {0} Boletines Oficiales\n".format(len(fechas)))

# Mensaje del progeso de descarga
text = "\rBO {0}/{1}. Detalles segunda del dia: {2}/{3}. Total bajados : {4}"


# Manager usado en el multiprocessing
manager = Manager()
lock = manager.Lock()
totalBajados = manager.Value('i', 0)


for cnt, fecha in enumerate(fechas):
    data = {'nombreSeccion': "segunda", 'subCat': 'all',
            'offset': '1', 'itemsPerPage': 3000,
            'fecha': int(fecha), 'idSesion': ''}
    r = requests.post(urlSeciones, data=data)

    # Decoded
    indiceSegunda = json.loads(r.text)

    if indiceSegunda['dataList']:
        segundaCnt = manager.Value('i', 1)
        pool = Pool(processes=args.numProcesos)
        results = pool.map(descargar_detalles_segunda,
                           indiceSegunda['dataList'][0])
        pool.close()
        pool.join()

file_data.close()
file_text.close()
