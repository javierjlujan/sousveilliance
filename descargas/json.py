#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import requests
from pprint import pprint
import datetime
import os

fname = "data.csv"

csv = open(fname, "r")
csvlines = csv.readlines()
if csvlines:
	lastLine = csvlines[-1]
	maxFecha = lastLine.split(",")[-5].replace("\"","")
else:
	maxFecha = datetime.date.today().strftime("%Y%m%d")

print ("Comenzando desde fecha: " + str(maxFecha))

fechas = []
for anio in range(2017, 1997, -1):
	for mes in range(13, 0, -1):
		for dia in range(31, 0, -1):
			fechaNueva = str(anio) + str(mes).zfill(2) + str(dia).zfill(2)
			if fechaNueva < maxFecha:
				fechas.append(fechaNueva)

primera_vez = True

cnt = 0

csv = open(fname, "a")
for fecha in fechas:
	#print(fecha)
	data = {'nombreSeccion': "segunda", 'subCat': 'all', 'offset': '1', 'itemsPerPage':3000, 'fecha':int(fecha), 'idSesion':''}
	r = requests.post("https://www.boletinoficial.gob.ar/secciones/secciones.json", data=data)

	#print(r.status_code)

	#Decoded
	indiceSegunda = json.loads(r.text)

	if indiceSegunda['dataList']:
		for tramite in indiceSegunda['dataList'][0]:
			cnt += 1

			data = {'id': tramite["id"], 'fechaPublicacion': 'null', 'idSesion': ''}
			t = requests.post("https://www.boletinoficial.gob.ar/norma/detalleSegunda", data=data)
			detalleSegunda = json.loads(t.text)
			sys.stdout.write('\r' + 'Cnt : ' + str(cnt) + ' fecha: ' + fecha + " " + detalleSegunda["dataList"]['rubroDescripcion'])

			# Creo el header
			if primera_vez:
				head = ""
				for key in detalleSegunda["dataList"]:
					head += key + ','
				head = head[:-1]
				head += '\n'
				csv.write(head)
				primera_vez = False

			line = ''

			#El denominacion social viene en null en detalle segunda, lo reemplazamos por el de tramite
			if detalleSegunda["dataList"]["denominacionSocial"] == None:
				detalleSegunda["dataList"]["denominacionSocial"] = tramite["denominacion"]

			for key in detalleSegunda["dataList"]:
				line += "\""+str(detalleSegunda["dataList"][key]).replace(",","\,").replace("\"","\\\"") + "\""+','
			line = line[:-1]
			line += '\n'

			csv.write(line)
			csv.flush()


