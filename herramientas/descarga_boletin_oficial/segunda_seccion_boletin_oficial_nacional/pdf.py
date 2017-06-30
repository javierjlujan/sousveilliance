import sys
import os
import urllib
import urllib2
import cookielib
import threading
from Queue import Queue
import datetime

def numero(num):
    if num == 1:
        n = '01'
    elif num == 2:
        n = '02'
    elif num == 3:
        n = '03'
    elif num == 4:
        n = '04'
    elif num == 5:
        n = '05'
    elif num == 6:
        n = '06'
    elif num == 7:
        n = '07'
    elif num == 8:
        n = '08'
    elif num == 9:
        n = '09'
    else:
        n = str(num)
    return str(n)

def nombre_mes(x):
    if x == '01':
        nombre = 'Enero'
    elif x == '02':
        nombre = 'Febrero'
    elif x == '03':
        nombre = 'Marzo'
    elif x == '04':
        nombre = 'Abril'
    elif x == '05':
        nombre = 'Mayo'
    elif x == '06':
        nombre = 'Junio'
    elif x == '07':
        nombre = 'Julio'
    elif x == '08':
        nombre = 'Agosto'
    elif x == '09':
        nombre = 'Septiembre'
    elif x == '10':
        nombre = 'Octubre'
    elif x == '11':
        nombre = 'Noviembre'
    elif x == '12':
        nombre = 'Diciembre'
    
    return nombre

def filename(url):
    nombre = url.split('=')[1].split('&')[0]
    ano = nombre[:4]
    mesdia = nombre[4:]
    dia = mesdia[2:]
    mes = mesdia[:2]
    m_nombre = nombre_mes(mes)

    _filename = ano+'/'+m_nombre+'/'+ano+'-'+mes+'-'+dia+'.pdf'

    return _filename

class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception,e:
                print "__Error: %s"%e
            self.queue.task_done()

    def download_url(self, url):        
        boletin = filename(url)
        print "Descargando %s"%(url)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        request = urllib2.Request(url)
        f = opener.open(request)
        data = f.read()
        f.close()
        opener.close()
        if not os.path.exists(os.path.dirname(boletin)):
            os.makedirs(os.path.dirname(boletin))
        FILE = open(boletin, "w")
        FILE.write(data)
        FILE.close()


def download(destfolder, numthreads=4):
    #2017021602
    queue = Queue()

    for a in range (2015,2017):
        ano = str(a)
        for m in range (1,13):
            mes = numero(m)
            for d in range(1,32): 
                dia = numero(d)
                url = 'https://www.boletinoficial.gob.ar/pdf/pdfPorNombreEmbed/'+ano+mes+dia+'N.pdf/93qZAzNdu3CpJUYb72Ct+C1bLS1JVi1bLScTMWj38XO3MTW55A7NGqw='
                queue.put(url)

    for i in range(numthreads):
        t = DownloadThread(queue, destfolder)
        t.start()

    queue.join()


if __name__ == "__main__":
    download("/tmp")