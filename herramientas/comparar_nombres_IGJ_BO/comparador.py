#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Indica si los nombres de las sociedades que figuran en el Boletín Oficial
# aparecen también en la base de datos provista por la IGJ

import csv
import pdb
import re
sociedades_igj = {}
with open('IGJ/igj-entidades.csv', encoding='latin-1') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        tipo = row[2]
        razon = row[3].lower()
        razon = re.sub(r'\s?\bs\.?a\.?\s?$', '', razon)
        razon = re.sub(r'\s?\bs\.?a\.?\s?$', '', razon)
        if razon in sociedades_igj:
            sociedades_igj[razon].append(tipo)
        else:
            sociedades_igj[razon] = [tipo]

sociedades_bo = {}
with open('../parseo/sample_data.csv') as csv_bolof:
    csvreader = csv.reader(csv_bolof, delimiter=',', quotechar='"', escapechar='\\')
    next(csvreader)
    i = 1
    for row in csvreader:
        # hay encabezados metidos en medio del csv; skippearlos:
        if row[0] == 'anioTramite':
            continue
        rubro = row[4]
        fecha = int(row[7])
        if rubro == 'CONSTITUCION SA' and fecha < 20170101:
            razon = row[1].lower()
            razon = re.sub('\</?p\>', '', razon)
            razon = re.sub(r'\s?\bs\.?a\.?\s?$', '', razon)
            if razon not in sociedades_igj:
                sociedades_bo[razon] = 0
            else:
                sociedades_bo[razon] = 1
        i += 1

no_igj = [razon for razon in sociedades_bo if not sociedades_bo[razon]]
