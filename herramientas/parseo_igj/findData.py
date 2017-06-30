#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# A partir del csv, extrae los DNIs del texto del acta según expresión regular,
# y la agrega al final de la fila en el csv
###

import re
import pdb
import html2text
import csv

csvin = open('sample_data.csv')
csvout = open('sample_data_dnis.csv', 'w')
csvreader = csv.reader(csvin, delimiter=',', quotechar='"', escapechar='\\')
csvwriter = csv.writer(csvout, delimiter=',', quotechar='"')
csvwriter.writerow(next(csvreader) + ['dnis'])  # copia los encabezados del csv
for row in csvreader:
    texto_acta = html2text.html2text(row[5])
    dnis = re.findall('D\.?N\.?I\.?\s*(\d{1,2}\.?\d{3}\.?\d{3})', texto_acta)  # sólo identifica 7-8 números juntos si precedido por "DNI"
    # dnis = re.findall('\d{1,2}\.?\d{3}\.?\d{3}', texto_acta)  # suponemos que todo número de 7-8 dígitos es un DNI (conflicto con montos)
    csvwriter.writerow(row + [','.join(dnis).replace('.', '')])  # agrega dnis al final, separados por comas, sin puntos
csvin.close
csvout.close

# ToDo: el título del acta es el nombre de la sociedad
# tambièn se puede obtener del texto precedente (dificil definir donde emopieza) a "S.A."

# encuentra los DNIs presentes en el acta
