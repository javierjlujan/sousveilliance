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

import requests


# Parser los datos de la cli
parser = argparse.ArgumentParser(description="Descarga de las BO")
parser.add_argument('-i', '--inicio', dest='fechaInicio',
                    default=datetime.date.today().strftime("%Y%m%d"),
                    help='Fecha de la cual comenzar a descargar.\
                    Forma: (yyyymmdd)')
parser.add_argument('-f' '--fin', dest='fechaFinal',
                    default='19970101',
                    help='Fecha hasta la cual descargar..\
                    Forma: (yyyymmdd)')
args = parser.parse_args()


# Archivo de salida
fname = "BO_data.csv"


# Si el archivo de salida existe, retomo desde donde dejo
dirs = os.listdir()
if fname in dirs:
    csv = open(fname, "r")
    csvLines = csv.readlines()
    lastLine = csvLines[-1]
    args.fechaInicio = lastLine.split(",")[-5].replace("\"", "")
    # No necesita un header el csv
    header = False
else:
    header = True


# Lista de fechas que voy a bajar
fechas = []

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

delta = d1 - d2

for i in range(delta.days + 1):
    fecha = d1 - datetime.timedelta(days=i)
    # Sole me quedo con los dias laborables
    if fecha.weekday() in range(0, 5):
        fechas.append(fecha.strftime("%Y%m%d"))


print("Descargar desde: {0} hasta: {1}".format(args.fechaInicio,
                                               args.fechaFinal))
print("Se van a descar: {0} Boletines Oficiales\n".format(len(fechas)))

urlSeciones = "https://www.boletinoficial.gob.ar/secciones/secciones.json"
urlSegunda = "https://www.boletinoficial.gob.ar/norma/detalleSegunda"

csv = open(fname, "a")
totalBajados = 0
text = "\rBO {0}/{1}. Detalles segunda del dia: {2}/{3}. Total bajados : {4}"

for boCnt, fecha in enumerate(fechas):
    data = {'nombreSeccion': "segunda", 'subCat': 'all',
            'offset': '1', 'itemsPerPage': 3000,
            'fecha': int(fecha), 'idSesion': ''}
    r = requests.post(urlSeciones, data=data)

    # Decoded
    indiceSegunda = json.loads(r.text)

    if indiceSegunda['dataList']:
        for segundaCnt, tramite in enumerate(indiceSegunda['dataList'][0]):
            totalBajados += 1
            # Print numero de detalle bajado
            sys.stdout.write(text.format(boCnt + 1, len(fechas),
                                         segundaCnt + 1,
                                         len(indiceSegunda['dataList'][0]),
                                         totalBajados))

            data = {'id': tramite["id"], 'fechaPublicacion': 'null',
                    'idSesion': ''}
            t = requests.post(urlSegunda, data=data)

            # Decoded
            detalleSegunda = json.loads(t.text)

            # Creo el header
            if header:
                line = ""
                for key in detalleSegunda["dataList"]:
                    line += key + ','
                line = line[:-1]
                line += '\n'
                csv.write(line)
                header = False

            # La denominacion social viene en null en detalle segunda,
            # lo reemplazamos por el de tramite
            if detalleSegunda["dataList"]["denominacionSocial"] is None:
                detalleSegunda["dataList"]["denominacionSocial"] = tramite["denominacion"]

            line = ''
            for key in detalleSegunda["dataList"]:
                line += "\""+str(detalleSegunda["dataList"][key]).replace(",","\,").replace("\"", "\\\"") + "\""+','
            line = line[:-1]
            line += '\n'

            csv.write(line)
            csv.flush()

csv.close()
